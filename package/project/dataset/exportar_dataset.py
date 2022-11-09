""" Script para exportar o dataset. """
import argparse

from project.dataset.oper_dataset import export_dataset
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
        "--export_dir",
        type=str,
        required=True,
        help="path para o diretório de exportação do dataset",
    )
    parser.add_argument(
        "--only_metadados",
        type=bool,
        required=False,
        help="se True, exporta apenas os metadados",
    )
    args = parser.parse_args()

    config = create_and_validate_config(profile=args.profile)

    name_dataset = config.anotacao_config.NOME_DATASET

    export_dataset(
        name_dataset=name_dataset,
        export_dir=args.export_dir,
        fields_metadados=config.anotacao_config.FIELD_METADADOS,
        only_metadados=args.only_metadados,
    )


if __name__ == "__main__":
    main()
