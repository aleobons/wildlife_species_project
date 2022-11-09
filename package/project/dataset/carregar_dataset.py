""" Script para carregar um dataset. """
import argparse
import pathlib

from project.dataset.oper_dataset import (
    load_dataset,
    salva_ids_selecionados,
)
from project.core_config import create_and_validate_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        type=str,
        required=True,
        help="nome do arquivo de configuração",
    )
    parser.add_argument(
        "--nome_dataset",
        type=str,
        required=False,
        help="nome do dataset para abrir ou criar",
    )
    parser.add_argument(
        "--novo_dataset",
        type=bool,
        default=False,
        help="indica se o dataset deve ser criado (novo = True) ou aberto",
    )
    parser.add_argument(
        "--path_dataset",
        type=pathlib.Path,
        required=False,
        help="path para o dataset quando for necessário criar um novo",
    )
    parser.add_argument(
        "--temp_dataset",
        type=bool,
        default=False,
        help="indicar se o dataset deve ser criado temporariamente",
    )

    parser.add_argument(
        "--launch_fiftyone",
        type=bool,
        default=False,
        help="indicar se vai subir o app do fiftyone",
    )

    parser.add_argument(
        "--force_dataset_replacement",
        type=bool,
        default=False,
        help="indicar se vai substituir o dataset caso já exista",
    )

    parser.add_argument(
        "--path_ids_selecionados",
        type=str,
        required=False,
        help="path para o arquivo txt com os ids selecionados durante a sessão do fiftyone",
    )

    args = parser.parse_args()
    config = create_and_validate_config(profile=args.profile)

    if args.nome_dataset is None:
        args.nome_dataset = config.anotacao_config.NOME_DATASET

    if args.path_dataset is None:
        args.path_dataset = config.dataset_config.SHAPES_PATH

    _, session = load_dataset(
        name_dataset=args.nome_dataset,
        novo_dataset=args.novo_dataset,
        path_dataset=args.path_dataset,
        temp_dataset=args.temp_dataset,
        launch_fiftyone=args.launch_fiftyone,
        force_dataset_replacement=args.force_dataset_replacement,
    )

    if session:
        input("\nPressione qualquer tecla para salvar os ids selecionados\n")

        if args.path_ids_selecionados is not None:
            salva_ids_selecionados(
                session=session, path_ids_file=args.path_ids_selecionados
            )


if __name__ == "__main__":
    main()
