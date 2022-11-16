# Project guidelines and settings

## Goal
Project to a test competition on Driven Data site (Conser-vision Practice Area: Image Classification - https://www.drivendata.org/)

Competition link: https://www.drivendata.org/competitions/87/competition-image-classification-wildlife-conservation/

## Project Structure
The project structure will be based on MLFlow Pipelines: https://mlflow.org/docs/latest/pipelines.html

## Dataset
The dataset is available on the competition page.

## Explorer Data Analysis
The data analysis will be done using the Fiftyone library (https://voxel51.com/docs/fiftyone/user_guide/)

### Load dataset

To create or load a dataset, run the command below:

    python -m project.dataset.load_dataset --profile <filename-config> --new_dataset <true> --launch_fiftyone <true> --force_dataset_replacement <true> --path_selected_ids <path_to_file_with_selected_ids> --path_dataset <path/to/metadata.csv>

*new_dataset*: if `true`, create a new dataset.

*path_selected_ids*: txt file with the ids of the images that will be selected through Fiftyone app run. If empty all selected images will be discarded.

*path_dataset*: path to metadata file if you want to load the dataset from it.

### Add labels and metadata

Run the command below to add the metadata to dataset:

```bash
python -m project.dataset.add_metadata --profile <filename-config>
```

Run the command below to add labels to dataset:

**NOTE: check if any required metadata has already been added**

```bash
python -m project.dataset.add_labels --profile <filename-config>
```

### Remove selected images

Run the command below to remove the images from an IDs file:

```bash
python -m project.dataset.remove_images --profile <filename-config> --path_ids_txt <path/to>/<filename-ids>.txt
```

### Annotate or re-annotate the selected images

**NOTE:** `CVAT installation is required: https://opencv.github.io/cvat/docs/administration/basics/installation/`

Run the command below to annotate or re-annotate the images from an IDs file:

```bash
python -m project.dataset.annotation_images --profile <filename-config> --path_ids_txt <path/to/filename-ids>.txt --url <cvat_url> --key_annotation <annotation_run_name>
```
