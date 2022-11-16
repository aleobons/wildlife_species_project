"""
Script to validation the config.yml and return a dictionary with the config values.
"""
import os
from pathlib import Path

from configparser import ConfigParser
from typing import List

from pydantic import BaseModel, validator
from strictyaml import load, YAML


# instantiate
config = ConfigParser()
# parse existing file
config.read("project.ini")

PROFILES_PATH = Path(config.get("profiles", "profiles_path"))


def check_path(value):
    """
    Check if is a valid path
    """

    if os.path.exists(value):
        return value
    raise ValueError(f"Invalid path: {value}")


class DatasetConfig(BaseModel):
    """
    Dataset config.
    """

    WITH_LABEL: bool = True
    IMAGES_PATH: str

    _validator_IMAGES_PATH = validator("IMAGES_PATH", pre=True, allow_reuse=True)(
        check_path
    )


class FiftyoneConfig(BaseModel):
    """
    Configurations to run fiftyone.
    """

    NAME_DATASET: str

    KEY_FIELD_CSV_LABEL: str
    KEY_FIELD_CSV_METADADOS: str

    KEY_DATASET_LABEL: str
    KEY_DATASET_METADADOS: str

    PATH_LABELS: str
    _validator_PATH_LABELS = validator("PATH_LABELS", pre=True, allow_reuse=True)(
        check_path
    )
    PATH_METADADOS: str
    _validator_PATH_METADADOS = validator("PATH_METADADOS", pre=True, allow_reuse=True)(
        check_path
    )

    TYPE_LABEL: str
    FIELD_LABEL: List[str]
    FIELD_METADADOS: List[str]

    @validator("TYPE_LABEL")
    def type_label_options(cls, v):
        if v not in ["labelencoder", "onehotencoder"]:
            raise ValueError('TYPE_LABEL needs to be "labelencoder" or "onehotencoder"')
        return v


class Config(BaseModel):
    """Master config object."""

    dataset_config: DatasetConfig
    fiftyone_config: FiftyoneConfig


def find_config_file(profile: str) -> Path:
    """Locate the configuration file."""
    config_file = PROFILES_PATH / f"{profile}.yml"
    if config_file.is_file():
        return config_file
    raise Exception(f"Config not found at {PROFILES_PATH!r}")


def fetch_config_from_yaml(profile: str) -> YAML:
    """Parse YAML containing the package configuration."""

    cfg_path = find_config_file(profile)

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(profile: str) -> Config:
    """Run validation on config values."""
    # if parsed_config is None:
    parsed_config = fetch_config_from_yaml(profile)

    parsed_config_dict = parsed_config.data

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        dataset_config=DatasetConfig(**parsed_config_dict),
        fiftyone_config=FiftyoneConfig(**parsed_config_dict),
    )
    print(f"configuration: {_config}")

    return _config
