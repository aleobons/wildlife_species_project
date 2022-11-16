""" Script to add labels to dataset. """
import argparse

from project.core_config import create_and_validate_config

from project.dataset.oper_dataset import add_labels

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
path_labels = config.fiftyone_config.PATH_LABELS
key_field = config.fiftyone_config.KEY_FIELD_CSV_LABEL
key_dataset = config.fiftyone_config.KEY_DATASET_LABEL
field_labels = config.fiftyone_config.FIELD_LABEL
type_label = config.fiftyone_config.TYPE_LABEL

add_labels(
    name_dataset=name_dataset,
    path_labels=path_labels,
    key_field=key_field,
    key_dataset=key_dataset,
    field_labels=field_labels,
    type_label=type_label,
)
