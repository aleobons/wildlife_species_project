""" Script para anotar samples do dataset. """
import argparse
import pathlib

from project.dataset.oper_dataset import anota_samples
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
        "--path_ids_txt",
        type=str,
        required=False,
        help="path para o arquivo csv com os ids",
    )
    parser.add_argument(
        "--ids",
        type=str,
        nargs="*",
        required=False,
        help="ids a serem anotados",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8080/",
        help="url do CVAT",
    )
    parser.add_argument(
        "--key_anotacao",
        type=str,
        required=False,
        help="nome para a execução da anotação",
    )
    args = parser.parse_args()

    config = create_and_validate_config(profile=args.profile)

    name_dataset = config.anotacao_config.NOME_DATASET

    if args.ids is not None:
        list_ids = args.ids
    elif args.path_ids_txt is not None:
        path_ids_txt = pathlib.Path(args.path_ids_txt)
        list_ids = path_ids_txt.read_text().splitlines()

    anota_samples(
        nome_dataset=name_dataset,
        list_ids=list_ids,
        url=args.url,
        launch_editor=True,
        anno_key=args.key_anotacao,
    )


if __name__ == "__main__":
    main()
