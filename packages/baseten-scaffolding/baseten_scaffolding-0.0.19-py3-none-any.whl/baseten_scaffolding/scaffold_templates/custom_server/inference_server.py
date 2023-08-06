import os
import pathlib

import kfserving
import yaml
from common.b10server import B10Server
from server.inference_model import CustomBasetenModel

CONFIG_FILE = "config.yaml"
DEFAULT_MODEL_NAME = "model"
DEFAULT_LOCAL_MODEL_DIR = "model"
BUILD_ARGS_KEY = "build_args"
MODEL_CLASS_KEY = "MODEL_CLASS"
MODEL_CLASS_DEFINITION_FILE_KEY = "MODEL_CLASS_DEFINITION_FILE"
MODEL_INIT_PARAMETERS_KEY = "model_init_parameters"
MODEL_CLASS_NAME = os.environ.get("MODEL_CLASS_NAME", "CustomModel")
MODEL_CLASS_FILE = os.environ.get("MODEL_CLASS_FILE", "model.py")


if __name__ == "__main__":
    with open(pathlib.Path(CONFIG_FILE), "r") as config_file:
        model_config = yaml.safe_load(config_file)
    model_class_args = model_config.get(BUILD_ARGS_KEY, {})
    model_class_name = model_class_args.get(MODEL_CLASS_KEY, MODEL_CLASS_NAME)
    model_class_file = model_class_args.get(
        MODEL_CLASS_DEFINITION_FILE_KEY, MODEL_CLASS_FILE
    )
    model_init_parameters = model_config.get(MODEL_INIT_PARAMETERS_KEY, {})
    model = CustomBasetenModel(
        DEFAULT_MODEL_NAME,
        model_class_name,
        model_class_file,
        DEFAULT_LOCAL_MODEL_DIR,
        model_init_parameters,
    )
    model.load()
    B10Server(workers=1).start([model])
