import pytest

from nlu_bf.constants import DOMAIN_SCHEMA_FILE, CONFIG_SCHEMA_FILE

import nlu_bf.utils.validation as validation_utils
import nlu_bf.utils.io as io_utils


@pytest.mark.parametrize(
    "file, schema",
    [
        ("examples/restaurantbot/domain.yml", DOMAIN_SCHEMA_FILE),
        ("data/test_config/config_defaults.yml", CONFIG_SCHEMA_FILE),
        ("data/test_config/config_supervised_embeddings.yml", CONFIG_SCHEMA_FILE),
        ("data/test_config/config_crf_custom_features.yml", CONFIG_SCHEMA_FILE),
    ],
)
def test_validate_yaml_schema(file, schema):
    # should raise no exception
    validation_utils.validate_yaml_schema(io_utils.read_file(file), schema)


@pytest.mark.parametrize(
    "file, schema",
    [
        ("data/test_domains/invalid_format.yml", DOMAIN_SCHEMA_FILE),
        ("examples/restaurantbot/data/nlu.md", DOMAIN_SCHEMA_FILE),
        ("data/test_config/example_config.yaml", CONFIG_SCHEMA_FILE),
    ],
)
def test_validate_yaml_schema_raise_exception(file, schema):
    with pytest.raises(validation_utils.InvalidYamlFileError):
        validation_utils.validate_yaml_schema(io_utils.read_file(file), schema)
