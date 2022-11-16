""" Script to add metadata to dataset. """
import argparse

from project.core_config import create_and_validate_config

from project.dataset.oper_dataset import add_metadata


parser = argparse.ArgumentParser()
parser.add_argument(
    "--profile",
    type=str,
    required=True,
    help="configuration filename",
)

args = parser.parse_args()
config = create_and_validate_config(profile=args.profile)

name_dataset = config.fiftyone_config.NAME_DATASET
path_metadados = config.fiftyone_config.PATH_METADADOS
key_field = config.fiftyone_config.KEY_FIELD_CSV_METADADOS
key_dataset = config.fiftyone_config.KEY_DATASET_METADADOS
fields_metadados = config.fiftyone_config.FIELD_METADADOS

add_metadata(
    name_dataset=name_dataset,
    path_metadados=path_metadados,
    key_field=key_field,
    key_dataset=key_dataset,
    fields_metadados=fields_metadados,
)
