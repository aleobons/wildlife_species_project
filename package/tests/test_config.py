from project.core_config import (
    create_and_validate_config,
)

import pytest
from pydantic import ValidationError


def test_fetch_config_structure():
    # Given
    profile = "config"

    # When
    config = create_and_validate_config(profile)

    # Then
    assert config.dataset_config


def test_config_validation_raises_error_for_invalid_config():
    # Given
    profile = "config_invalid"

    # When
    with pytest.raises(ValidationError) as excinfo:
        create_and_validate_config(profile)

    # Then
    assert "Invalid path" in str(excinfo.value)


def test_missing_config_field_raises_validation_error():
    # Given
    profile = "config_incomplete"

    # When
    with pytest.raises(ValidationError) as excinfo:
        create_and_validate_config(profile)

    # Then
    assert "field required" in str(excinfo.value)
    assert "IMAGES_PATH" in str(excinfo.value)
