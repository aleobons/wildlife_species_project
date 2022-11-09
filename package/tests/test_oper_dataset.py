import pathlib
import fiftyone as fo
import pytest

from project.dataset.oper_dataset import (
    adiciona_metadados,
    adiciona_labels,
    load_dataset,
    exclui_samples,
    salva_ids_selecionados,
    export_dataset,
)


@pytest.fixture(scope="session", autouse=True)
def dataset(config_test):
    list_datasets = fo.list_datasets()
    name_dataset = config_test.anotacao_config.NOME_DATASET

    if name_dataset in list_datasets:
        fo.delete_dataset(name_dataset)

    dataset = fo.Dataset.from_images_dir(
        config_test.dataset_config.SHAPES_PATH,
        name=name_dataset,
    )

    print(f"tamanho do dataset: {len(dataset)}")
    yield dataset

    print("\n\n[INFO] deleting dataset...")
    fo.delete_dataset(name_dataset)


def test_adicionar_marcamodelo_placa(dataset, config_test):
    # Given
    name_dataset = config_test.anotacao_config.NOME_DATASET
    path_metadados = config_test.anotacao_config.PATH_METADADOS
    key_field = config_test.anotacao_config.KEY_FIELD_CSV_METADADOS
    key_dataset = config_test.anotacao_config.KEY_DATASET_METADADOS
    fields_metadados = config_test.anotacao_config.FIELD_METADADOS

    # When
    adiciona_metadados(
        name_dataset=name_dataset,
        path_metadados=path_metadados,
        key_field=key_field,
        key_dataset=key_dataset,
        fields_metadados=fields_metadados,
    )

    # Then
    sample = dataset.first()
    marca_modelo = sample.marca_modelo
    placa = sample.placa

    assert marca_modelo in ["VW/GOL", "FORD/FIESTA", "HYUNDAI/HB20"]
    assert placa in ["NDP6341", "NHO6534", "ND6534"]


@pytest.mark.dependency(depends=["test_adicionar_marcamodelo_placa"])
def test_adicionar_label(dataset, config_test):
    # Given
    name_dataset = config_test.anotacao_config.NOME_DATASET
    path_labels = config_test.anotacao_config.PATH_LABELS
    key_field = config_test.anotacao_config.KEY_FIELD_CSV_LABEL
    key_dataset = config_test.anotacao_config.KEY_DATASET_LABEL
    field_labels = config_test.anotacao_config.FIELD_LABEL

    # When
    adiciona_labels(
        name_dataset=name_dataset,
        path_labels=path_labels,
        key_field=key_field,
        key_dataset=key_dataset,
        field_labels=field_labels,
    )

    # Then
    sample = dataset.first()
    label = sample.ground_truth.label
    assert label in ["AUTOMOVEL", "MOTOCICLETA", "CAMINHAO"]

    sample = dataset.last()
    label = sample.ground_truth.label
    assert label in ["AUTOMOVEL", "MOTOCICLETA", "CAMINHAO"]


@pytest.mark.dependency(depends=["test_adicionar_label"])
def test_carrega_dataset(config_test):
    # Given
    nome_dataset = config_test.anotacao_config.NOME_DATASET
    novo_dataset = False
    path_dataset = config_test.dataset_config.SHAPES_PATH
    temp_dataset = False
    launch_fiftyone = False
    force_dataset_replacement = False

    # When
    dataset, _ = load_dataset(
        name_dataset=nome_dataset,
        novo_dataset=novo_dataset,
        path_dataset=path_dataset,
        temp_dataset=temp_dataset,
        launch_fiftyone=launch_fiftyone,
        force_dataset_replacement=force_dataset_replacement,
    )

    # Then
    assert dataset
    assert "dataset_test" in fo.list_datasets()
    assert len(dataset) == 3


@pytest.mark.dependency(depends=["test_carrega_dataset"])
def test_salva_ids_selecionados(dataset, tmp_path):
    # Given
    session = fo.Session(dataset)

    session.dataset.select(sample_ids=[dataset.first().id, dataset.last().id])

    path_ids = tmp_path / "ids.txt"

    # When
    salva_ids_selecionados(session=session, path_ids_file=path_ids)

    # Then
    assert pathlib.Path(path_ids).exists()


@pytest.mark.dependency(depends=["test_salva_ids_selecionados"])
def test_export_dir(dataset, tmp_path, config_test):
    # Given
    path_export = tmp_path / "export"
    path_export.mkdir()

    fields_metadados = config_test.anotacao_config.FIELD_METADADOS

    # When
    export_dataset(
        name_dataset=dataset.name,
        export_dir=str(path_export),
        fields_metadados=fields_metadados,
    )

    # Then
    assert pathlib.Path(path_export).exists()
    assert pathlib.Path(path_export / "metadados.csv").exists()
    assert len(list(path_export.glob("*"))) == 4


@pytest.mark.parametrize(
    "source_ids, expected",
    [("command_line", 2), ("file", 1)],
)
@pytest.mark.dependency(depends=["test_export_dir"])
def test_remove_sample(dataset, config_test, source_ids, tmp_path, expected):
    # Given
    first_id = dataset.first().id

    if source_ids == "command_line":
        list_ids = [first_id]
    elif source_ids == "file":
        path_ids_csv = tmp_path / "source_ids.csv"

        with open(path_ids_csv, "w") as f:
            f.write(first_id)

        path_ids_csv = pathlib.Path(path_ids_csv)
        list_ids = path_ids_csv.read_text().splitlines()

    name_dataset = config_test.anotacao_config.NOME_DATASET

    # When
    exclui_samples(nome_dataset=name_dataset, list_ids=list_ids)

    # Then
    assert len(dataset) == expected


@pytest.mark.parametrize("source_dataset", [("dir"), ("csv")])
def test_cria_dataset(config_test, source_dataset):
    # Given
    nome_dataset = "dataset_test2"
    novo_dataset = True
    if source_dataset == "dir":
        path_dataset = config_test.dataset_config.SHAPES_PATH
    elif source_dataset == "csv":
        path_dataset = "/workspaces/projeto_classificador_tipo/package/tests/input_tests/metadados.csv"
    temp_dataset = False
    launch_fiftyone = False
    force_dataset_replacement = False

    # When
    dataset, _ = load_dataset(
        name_dataset=nome_dataset,
        novo_dataset=novo_dataset,
        path_dataset=path_dataset,
        temp_dataset=temp_dataset,
        launch_fiftyone=launch_fiftyone,
        force_dataset_replacement=force_dataset_replacement,
    )

    # Then
    assert dataset
    assert nome_dataset in fo.list_datasets()
    assert len(dataset) == 3

    fo.delete_dataset(nome_dataset)


# def test_cria_dataset_existente(config_test):
#     # Given
#     nome_dataset = config_test.anotacao_config.NOME_DATASET
#     novo_dataset = True
#     path_dataset = config_test.dataset_config.SHAPES_PATH
#     temp_dataset = False
#     launch_fiftyone = False
#     force_dataset_replacement = True

#     # When
#     dataset, _ = load_dataset(
#         name_dataset=nome_dataset,
#         novo_dataset=novo_dataset,
#         path_dataset=path_dataset,
#         temp_dataset=temp_dataset,
#         launch_fiftyone=launch_fiftyone,
#         force_dataset_replacement=force_dataset_replacement,
#     )

#     # Then
#     assert dataset
#     assert "dataset_test" in fo.list_datasets()
#     assert len(dataset) == 3
