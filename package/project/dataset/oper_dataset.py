"""script com operações comuns para os datasets"""
import os
import glob
import csv
from typing import List, Callable
import fiftyone as fo
import pandas as pd
from tqdm import tqdm
import numpy as np


def carrega_samples(nome_dataset: str, images_path: List) -> fo.Dataset:

    samples = [fo.Sample(filepath=filepath) for filepath in images_path]

    # Create dataset
    dataset = fo.Dataset(nome_dataset)
    dataset.add_samples(samples)

    return dataset


def get_filepaths_in_csv(path_csv: str) -> List[str]:
    with open(path_csv, mode="r") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        filepath = []
        for row in csv_reader:
            filepath.append(row["filepath"])

    return filepath


def load_dataset(
    name_dataset: str,
    novo_dataset: bool,
    path_dataset: str,
    force_dataset_replacement: bool = False,
    temp_dataset: bool = False,
    launch_fiftyone: bool = False,
) -> fo.Dataset:
    list_datasets = fo.list_datasets()
    print(f"[INFO] lista de datasets disponíveis: {list_datasets}\n")

    if novo_dataset:
        if path_dataset is None:
            raise ValueError(
                "path_dataset não pode ser nulo quando novo_dataset = True"
            )

        if name_dataset in list_datasets:
            if not force_dataset_replacement:
                raise ValueError(
                    f"dataset {name_dataset} não pode ser criado pois já existe. Altere o argumento "
                    f"novo_dataset para False ou force_dataset_replacement para True."
                )

            print(f"[INFO] substituindo dataset {name_dataset}...")
            fo.delete_dataset(name_dataset)

        if str(path_dataset).lower().endswith((".csv")):
            filepaths = get_filepaths_in_csv(path_dataset)
            dataset = carrega_samples(nome_dataset=name_dataset, images_path=filepaths)
        else:
            dataset = fo.Dataset.from_images_dir(path_dataset, name=name_dataset)

        dataset.compute_metadata(overwrite=True)

        if not temp_dataset:
            dataset.persistent = True

    elif name_dataset not in list_datasets:
        raise ValueError(
            f"dataset {name_dataset} não existe. Altere o argumento "
            f"novo_dataset para True para criar um novo dataset"
        )
    else:
        dataset = fo.load_dataset(name_dataset)

    session = None
    if launch_fiftyone:
        session = fo.launch_app(dataset, port=5151)

        print(f"[INFO] dataset {name_dataset} carregado na porta 5151")

    return dataset, session


def load_csv(path: str) -> pd.DataFrame:
    """Carrega os metadados."""
    if not os.path.exists(path):
        raise ValueError(f"O caminho {path} não existe.")

    if os.path.isdir(path):
        path = os.path.join(path, "*.csv")
        files = glob.glob(path)
    else:
        files = [path]

    if len(files) > 1:
        df = pd.concat(
            [pd.read_csv(f, encoding="latin-1") for f in files], ignore_index=True
        )
    else:
        df = pd.read_csv(files[0], encoding="latin-1")

    return df


def atualizacao_fields(
    dataset: fo.Dataset,
    df: pd.DataFrame,
    df_key: str,
    dataset_key: str,
    fields_to_refresh: List[str],
    func_refresh: Callable,
    func_convert_key: Callable = None,
    **kwargs,
) -> None:
    """atualiza os samples com informações adicionais."""
    for sample in tqdm(dataset, desc="atualizando samples"):
        key = sample[dataset_key]
        if func_convert_key is not None:
            key = func_convert_key(key)

        df_sample = df[df[df_key] == key]

        if df_sample.shape[0] == 0:
            resposta = ""
            while resposta not in ["s", "n", "c"]:
                resposta = input(
                    f"{key} não encontrado nos CSVs. Deseja deletar exemplo do dataset? (s/n)."
                    f"Digite c para cancelar a atualização do dataset.\n"
                )
            if resposta == "c":
                break
            if resposta == "s":
                dataset.delete_samples(sample.id)

            continue

        for field in fields_to_refresh:
            if field not in ["nan", None, np.nan]:
                func_refresh(sample, df_sample, field, kwargs=kwargs)

        sample.save()


def inclusao_field(
    sample: fo.Sample, df: pd.DataFrame, name_field: str, **kwargs
) -> None:
    """Inclui um campo no sample."""
    sample[name_field] = df[name_field].values[0]


def inclusao_label_classificacao(
    sample: fo.Sample, df: pd.DataFrame, name_field: str = "ground_truth", **kwargs
) -> None:
    """Inclui um label de classificacao no sample."""
    sample["ground_truth"] = fo.Classification(label=df[name_field].values[0])


def extract_filename(path_image: str) -> str:
    """Extrai o nome do arquivo do path completo."""
    return path_image.split(os.path.sep)[-1]


def adiciona_metadados(
    name_dataset: str,
    path_metadados: str,
    key_field: str,
    key_dataset: str,
    fields_metadados: List[str],
) -> None:

    dataset, _ = load_dataset(
        name_dataset=name_dataset,
        novo_dataset=False,
        path_dataset="",
        temp_dataset=False,
        launch_fiftyone=False,
    )

    df_metadados = load_csv(path_metadados)

    if df_metadados is None:
        raise ValueError("Não foi possível carregar os metadados.")

    atualizacao_fields(
        dataset=dataset,
        df=df_metadados,
        df_key=key_field,
        dataset_key=key_dataset,
        fields_to_refresh=fields_metadados,
        func_refresh=inclusao_field,
        func_convert_key=extract_filename,
    )


def adiciona_labels(
    name_dataset: str,
    path_labels: str,
    key_field: str,
    key_dataset: str,
    field_labels: str,
) -> None:

    dataset, _ = load_dataset(
        name_dataset=name_dataset,
        novo_dataset=False,
        path_dataset="",
        temp_dataset=False,
        launch_fiftyone=False,
    )

    df_labels = load_csv(path_labels)

    if df_labels is None:
        raise ValueError("Não foi possível carregar os labels.")

    atualizacao_fields(
        dataset=dataset,
        df=df_labels,
        df_key=key_field,
        dataset_key=key_dataset,
        fields_to_refresh=[field_labels],
        func_refresh=inclusao_label_classificacao,
    )


def exclui_samples(nome_dataset: str, list_ids: List[str]) -> None:

    dataset, _ = load_dataset(
        name_dataset=nome_dataset,
        novo_dataset=False,
        path_dataset="",
        temp_dataset=False,
        launch_fiftyone=False,
    )

    dataset_com_ids = dataset.select(list_ids)

    for sample in dataset_com_ids:
        print(f"deletando sample {sample.id}")
        dataset.delete_samples(sample.id)


def salva_ids_selecionados(
    session: fo.Session, path_ids_file: str = "ids_selecionados.txt"
) -> None:
    ids = session.selected

    with open(path_ids_file, "w") as f:
        for id in ids:
            f.write(f"{id}\n")


def anota_samples(
    nome_dataset: str,
    list_ids: List[str],
    anno_key: str = "new_annotation_run",
    label_field: str = "ground_truth",
    url: str = "http://localhost:8080/",
    launch_editor: bool = True,
) -> None:

    dataset, _ = load_dataset(
        name_dataset=nome_dataset,
        novo_dataset=False,
        path_dataset="",
        temp_dataset=False,
        launch_fiftyone=False,
    )

    if dataset.has_annotation_run(anno_key):
        dataset.delete_annotation_run(anno_key)

    dataset_com_ids = dataset.select(list_ids)

    dataset_com_ids.annotate(
        anno_key,
        label_field=label_field,
        url=url,
        launch_editor=launch_editor,
    )

    resposta = input(
        "Pressione qualquer tecla para carregar as anotações ou C para cancelar"
    )

    if resposta not in ["c", "C"]:
        dataset.load_annotations(anno_key, url=url)


def export_dataset(
    name_dataset: str,
    export_dir: str,
    label_field: str = "ground_truth",
    fields_metadados: List[str] = None,
    only_metadados: bool = False,
) -> None:

    dataset, _ = load_dataset(
        name_dataset=name_dataset,
        novo_dataset=False,
        path_dataset="",
        temp_dataset=False,
        launch_fiftyone=False,
    )

    if not only_metadados:
        dataset.export(
            export_dir=export_dir,
            dataset_type=fo.types.ImageClassificationDirectoryTree,
            label_field=label_field,
        )

    if fields_metadados:
        dict = {"filepath": [], "filename": [], "label": []}

        for sample in dataset:
            if sample["ground_truth"] is not None:
                label = sample["ground_truth"].label
            else:
                label = "None"

            dict["filename"].append(
                os.path.join(
                    label,
                    sample["filepath"].split(os.path.sep)[-1],
                )
            )

            dict["filepath"].append(sample["filepath"])
            dict["label"].append(label)

            for field in fields_metadados:
                if dict.get(field, None) is None:
                    dict[field] = []

                dict[field].append(sample[field])

        pd.DataFrame(dict).to_csv(
            os.path.join(export_dir, "metadados.csv"), index=False
        )
