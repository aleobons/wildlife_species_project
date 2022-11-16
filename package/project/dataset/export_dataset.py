""" Script to export the dataset. """
import argparse

from project.dataset.oper_dataset import export_dataset
from project.core_config import create_and_validate_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        type=str,
        required=True,
        help="configuration filename",
    )
    parser.add_argument(
        "--export_dir",
        type=str,
        required=True,
        help="path to export folder of the dataset",
    )
    parser.add_argument(
        "--only_metadados",
        type=bool,
        required=False,
        help="whether True, export only the metadata",
    )
    args = parser.parse_args()

    config = create_and_validate_config(profile=args.profile)

    name_dataset = config.fiftyone_config.NOME_DATASET

    export_dataset(
        name_dataset=name_dataset,
        export_dir=args.export_dir,
        fields_metadados=config.fiftyone_config.FIELD_METADADOS,
        only_metadados=args.only_metadados,
    )


if __name__ == "__main__":
    main()
