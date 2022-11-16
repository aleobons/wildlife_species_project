""" Script to remove samples from dataset. """
import argparse
import pathlib

from project.dataset.oper_dataset import delete_samples
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
        "--path_ids_txt",
        type=str,
        required=False,
        help="path to csv file with ids",
    )
    parser.add_argument(
        "--ids",
        type=str,
        nargs="*",
        required=False,
        help="ids to delete",
    )
    args = parser.parse_args()

    config = create_and_validate_config(profile=args.profile)

    name_dataset = config.fiftyone_config.NOME_DATASET

    if args.ids is not None:
        list_ids = args.ids
    elif args.path_ids_txt is not None:
        path_ids_txt = pathlib.Path(args.path_ids_txt)
        list_ids = path_ids_txt.read_text().splitlines()

    delete_samples(name_dataset=name_dataset, list_ids=list_ids)


if __name__ == "__main__":
    main()
