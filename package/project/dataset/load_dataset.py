""" Script to load a dataset. """
import argparse
import pathlib

from project.dataset.oper_dataset import (
    load_dataset,
    save_selected_ids,
)
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
        "--name_dataset",
        type=str,
        required=False,
        help="dataset name to load or create",
    )
    parser.add_argument(
        "--new_dataset",
        type=bool,
        default=False,
        help="whether a dataset will be created (new = True) or loaded (new = False)",
    )
    parser.add_argument(
        "--path_dataset",
        type=pathlib.Path,
        required=False,
        help="path to dataset when it'll created from csv metadata",
    )
    parser.add_argument(
        "--temp_dataset",
        type=bool,
        default=False,
        help="whether the dataset will be created temporarily",
    )

    parser.add_argument(
        "--launch_fiftyone",
        type=bool,
        default=False,
        help="whether the fiftyone app will be launched",
    )

    parser.add_argument(
        "--force_dataset_replacement",
        type=bool,
        default=False,
        help="whether the dataset will be replaced, if it already exists",
    )

    parser.add_argument(
        "--path_selectd_ids",
        type=str,
        required=False,
        help="path to txt file with the selected ids through fiftyone season",
    )

    args = parser.parse_args()
    config = create_and_validate_config(profile=args.profile)

    if args.name_dataset is None:
        args.nome_dataset = config.fiftyone_config.NAME_DATASET

    if args.path_dataset is None:
        args.path_dataset = config.dataset_config.SHAPES_PATH

    _, session = load_dataset(
        name_dataset=args.name_dataset,
        new_dataset=args.new_dataset,
        path_dataset=args.path_dataset,
        temp_dataset=args.temp_dataset,
        launch_fiftyone=args.launch_fiftyone,
        force_dataset_replacement=args.force_dataset_replacement,
    )

    if session:
        input("\nTap any key to save the selected ids\n")

        if args.path_selectd_ids is not None:
            save_selected_ids(session=session, path_ids_file=args.path_selectd_ids)


if __name__ == "__main__":
    main()
