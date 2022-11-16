import pathlib
import fiftyone as fo
import pytest

from project.dataset.oper_dataset import (
    add_metadata,
    add_labels,
    load_dataset,
    delete_samples,
    save_selected_ids,
    export_dataset,
)


@pytest.fixture(scope="session", autouse=True)
def dataset(config_test):
    list_datasets = fo.list_datasets()
    name_dataset = config_test.fiftyone_config.NAME_DATASET

    if name_dataset in list_datasets:
        fo.delete_dataset(name_dataset)

    dataset = fo.Dataset.from_images_dir(
        config_test.dataset_config.IMAGES_PATH,
        name=name_dataset,
    )

    print(f"dataset lenght: {len(dataset)}")
    yield dataset

    print("\n\n[INFO] deleting dataset...")
    fo.delete_dataset(name_dataset)


def test_add_metadata(dataset, config_test):
    # Given
    name_dataset = config_test.fiftyone_config.NAME_DATASET
    path_metadados = config_test.fiftyone_config.PATH_METADADOS
    key_field = config_test.fiftyone_config.KEY_FIELD_CSV_METADADOS
    key_dataset = config_test.fiftyone_config.KEY_DATASET_METADADOS
    fields_metadados = config_test.fiftyone_config.FIELD_METADADOS

    # When
    add_metadata(
        name_dataset=name_dataset,
        path_metadados=path_metadados,
        key_field=key_field,
        key_dataset=key_dataset,
        fields_metadados=fields_metadados,
    )

    # Then
    sample = dataset.first()
    site = sample.site

    assert site in ["S0069", "S0009", "S0008"]


@pytest.mark.dependency(depends=["test_add_metadata"])
def test_add_label(dataset, config_test):
    # Given
    name_dataset = config_test.fiftyone_config.NAME_DATASET
    path_labels = config_test.fiftyone_config.PATH_LABELS
    key_field = config_test.fiftyone_config.KEY_FIELD_CSV_LABEL
    key_dataset = config_test.fiftyone_config.KEY_DATASET_LABEL
    field_labels = config_test.fiftyone_config.FIELD_LABEL
    type_label = config_test.fiftyone_config.TYPE_LABEL

    # When
    add_labels(
        name_dataset=name_dataset,
        path_labels=path_labels,
        key_field=key_field,
        key_dataset=key_dataset,
        field_labels=field_labels,
        type_label=type_label,
    )

    # Then
    sample = dataset.first()
    label = sample.ground_truth.label
    assert label in ["monkey_prosimian", "bird"]

    sample = dataset.last()
    label = sample.ground_truth.label
    assert label in ["monkey_prosimian", "bird"]


@pytest.mark.dependency(depends=["test_add_label"])
def test_load_dataset(config_test):
    # Given
    name_dataset = config_test.fiftyone_config.NAME_DATASET
    novo_dataset = False
    path_dataset = config_test.dataset_config.IMAGES_PATH
    temp_dataset = False
    launch_fiftyone = False
    force_dataset_replacement = False

    # When
    dataset, _ = load_dataset(
        name_dataset=name_dataset,
        new_dataset=novo_dataset,
        path_dataset=path_dataset,
        temp_dataset=temp_dataset,
        launch_fiftyone=launch_fiftyone,
        force_dataset_replacement=force_dataset_replacement,
    )

    # Then
    assert dataset
    assert "dataset_test" in fo.list_datasets()
    assert len(dataset) == 3


@pytest.mark.dependency(depends=["test_load_dataset"])
def test_save_selected_ids(dataset, tmp_path):
    # Given
    session = fo.Session(dataset)

    session.dataset.select(sample_ids=[dataset.first().id, dataset.last().id])

    path_ids = tmp_path / "ids.txt"

    # When
    save_selected_ids(session=session, path_ids_file=path_ids)

    # Then
    assert pathlib.Path(path_ids).exists()


@pytest.mark.dependency(depends=["test_save_selected_ids"])
def test_export_dir(dataset, tmp_path, config_test):
    # Given
    # path_export = pathlib.Path(
    #     "/workspaces/wildlife_species_project/package/tests/input_tests/data/export"
    # )
    path_export = tmp_path / "export"
    path_export.mkdir()

    fields_metadados = config_test.fiftyone_config.FIELD_METADADOS

    # When
    export_dataset(
        name_dataset=dataset.name,
        export_dir=str(path_export),
        fields_metadados=fields_metadados,
    )

    # Then
    assert pathlib.Path(path_export).exists()
    assert pathlib.Path(path_export / "metadata.csv").exists()
    print(list(path_export.glob("*")))
    assert len(list(path_export.glob("*"))) == 3


@pytest.mark.parametrize(
    "source_ids, expected",
    [("command_line", 2), ("file", 1)],
)
@pytest.mark.dependency(depends=["test_export_dir"])
def test_remove_sample(dataset, config_test, source_ids, tmp_path, expected):
    # Given
    first_id = dataset.first().id

    if source_ids == "command_line":
        list_ids = [first_id]
    elif source_ids == "file":
        path_ids_csv = tmp_path / "source_ids.csv"

        with open(path_ids_csv, "w") as f:
            f.write(first_id)

        path_ids_csv = pathlib.Path(path_ids_csv)
        list_ids = path_ids_csv.read_text().splitlines()

    name_dataset = config_test.fiftyone_config.NAME_DATASET

    # When
    delete_samples(name_dataset=name_dataset, list_ids=list_ids)

    # Then
    assert len(dataset) == expected


@pytest.mark.parametrize("source_dataset", [("dir"), ("csv")])
def test_create_dataset(config_test, source_dataset):
    # Given
    name_dataset = "dataset_test2"
    novo_dataset = True
    if source_dataset == "dir":
        path_dataset = config_test.dataset_config.IMAGES_PATH
    elif source_dataset == "csv":
        path_dataset = "/workspaces/wildlife_species_project/package/tests/input_tests/data/export/metadata.csv"
    temp_dataset = False
    launch_fiftyone = False
    force_dataset_replacement = False

    # When
    dataset, _ = load_dataset(
        name_dataset=name_dataset,
        new_dataset=novo_dataset,
        path_dataset=path_dataset,
        temp_dataset=temp_dataset,
        launch_fiftyone=launch_fiftyone,
        force_dataset_replacement=force_dataset_replacement,
    )

    # Then
    assert dataset
    assert name_dataset in fo.list_datasets()
    assert len(dataset) == 3

    fo.delete_dataset(name_dataset)
