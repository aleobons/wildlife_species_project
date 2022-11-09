from project.core_config import create_and_validate_config
import pytest
import tensorflow as tf


# @pytest.fixture(scope="session", autouse=True)
# def features_spec():
#     features_spec = {
#         "image_raw": tf.io.FixedLenFeature([], tf.string),
#         "label": tf.io.FixedLenFeature([], tf.int64),
#     }

#     return features_spec


@pytest.fixture(scope="session", autouse=True)
def profile():
    profile = "config"

    return profile


@pytest.fixture(scope="session", autouse=True)
def config_test(profile):
    config_test = create_and_validate_config(profile=profile)

    return config_test


# @pytest.fixture(scope="session", autouse=True)
# def model_path():
#     model_path = "tests/input_tests/model_output"

#     return model_path


# @pytest.fixture(scope="session", autouse=True)
# def profile_pipeline():
#     profile_pipeline = {
#         "image_key": "image_raw",
#         "file_image_key": "filename",
#         "label_key": "label",
#         "input_shape": (64, 64, 3),
#         "feature_spec": {
#             "filename": "string",
#             "marca_modelo": "string",
#             "placa": "string",
#         },
#         "file_pattern": "*.tfrecords",
#         "batch_size": 4,
#         "feature_x_metadados": {
#             "filename": "filename",
#             "marca_modelo": "marcaModelo",
#             "placa": "placa",
#         },
#         "filename_column": "filename",
#         "train_dev_split": 0.2,
#         "tfrecord_size": 100,
#         "label_metadados": "label",
#         "metadados_filename": "metadados.csv",
#         "azure_config_path": "tests/.azureml/config.json",
#         "managed_identity_client_id": "6135bbfa-2272-4324-8310-7c0f5de00c5a",
#         "model_name": "type_classification_traseira_model",
#         "model_description": "modelo que classifica o tipo de veiculo de imagens traseiras",
#         "endpoint_name": "type-classification-traseira",
#         "endpoint_description": "Serviço de classificação de tipos de veículos em imagens traseiras",
#         "deployment_name": "blue",
#         "deployment_environment": "cpu-tensorflow-27-inference:7",
#         "deployment_traffic": 100,
#         "deployment_code_path": "tests/input_tests/code",
#         "deployment_scoring_script": "score.py",
#         "deployment_instance_type": "Standard_F2s_v2",
#         "deployment_instances": 1,
#         "classes": 7,
#         "augmentation_strategy": "none",
#         "tensorboard_logdir": "/workspaces/type_classification/package/tests/output_tests",
#         "epochs": 1,
#         "learning_rate": 0.001,
#         "optimizer": "adam",
#         "dense_size": 128,
#         "dropout_dense": 0.5,
#         "metrics_to_pass": [
#             {"name": "accuracy", "direction": "upper", "threshold": 0.9}
#         ],
#         "metrics_to_compare": [
#             {"name": "accuracy", "direction": "higger_is_better", "threshold": 1e-10}
#         ],
#         "labels_names": [
#             "CAMIONETA",
#             "CAMINHAO",
#             "CAMINHONETE",
#             "ONIBUS",
#             "MOTOCICLETA",
#             "AUTOMOVEL",
#             "FURGAO",
#         ],
#     }

#     return profile_pipeline
