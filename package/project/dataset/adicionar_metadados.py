""" Script para adicionar metadados no dataset. """
import argparse

from project.core_config import create_and_validate_config

from project.dataset.oper_dataset import adiciona_metadados


parser = argparse.ArgumentParser()
parser.add_argument(
    "--profile",
    type=str,
    required=True,
    help="nome do arquivo de configuração",
)

args = parser.parse_args()
config = create_and_validate_config(profile=args.profile)

name_dataset = config.anotacao_config.NOME_DATASET
path_metadados = config.anotacao_config.PATH_METADADOS
key_field = config.anotacao_config.KEY_FIELD_CSV_METADADOS
key_dataset = config.anotacao_config.KEY_DATASET_METADADOS
fields_metadados = config.anotacao_config.FIELD_METADADOS

adiciona_metadados(
    name_dataset=name_dataset,
    path_metadados=path_metadados,
    key_field=key_field,
    key_dataset=key_dataset,
    fields_metadados=fields_metadados,
)
