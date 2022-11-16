from project.core_config import create_and_validate_config
import pytest


@pytest.fixture(scope="session", autouse=True)
def profile():
    profile = "config"

    return profile


@pytest.fixture(scope="session", autouse=True)
def config_test(profile):
    config_test = create_and_validate_config(profile=profile)

    return config_test
