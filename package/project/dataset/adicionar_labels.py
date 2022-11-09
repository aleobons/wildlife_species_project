""" Script para adicionar metadados no dataset. """
import argparse

from project.core_config import create_and_validate_config

from project.dataset.oper_dataset import adiciona_labels

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
path_labels = config.anotacao_config.PATH_LABELS
key_field = config.anotacao_config.KEY_FIELD_CSV_LABEL
key_dataset = config.anotacao_config.KEY_DATASET_LABEL
field_labels = config.anotacao_config.FIELD_LABEL

adiciona_labels(
    name_dataset=name_dataset,
    path_labels=path_labels,
    key_field=key_field,
    key_dataset=key_dataset,
    field_labels=field_labels,
)
