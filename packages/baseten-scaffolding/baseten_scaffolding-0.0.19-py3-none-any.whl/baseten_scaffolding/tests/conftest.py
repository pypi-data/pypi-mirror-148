import contextlib
import importlib
import os
import sys

import pytest

PYTORCH_MODEL_FILE_CONTENTS = """
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.main = torch.nn.Sequential(
            torch.nn.Linear(3, 1),
            torch.nn.Flatten(0, 1)
        )

    def forward(self, input):
        return self.main(input)

"""


PYTORCH_WITH_INIT_ARGS_MODEL_FILE_CONTENTS = """
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self, arg1, arg2, kwarg1=1, kwarg2=2):
        super(MyModel, self).__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.kwarg1 = kwarg1
        self.kwarg2 = kwarg2

    def forward(self, input):
        return input

"""


CUSTOM_MODEL_CODE = """
class MyModel:
    def load(self):
        pass

    def predict(self, inputs):
        return 1
"""


# Doesn't implement load
NO_LOAD_CUSTOM_MODEL_CODE = """
class MyModel:
    def predict(self, inputs):
        return 1
"""


# Doesn't implement predict
NO_PREDICT_CUSTOM_MODEL_CODE = """
class MyModel:
    def load(self):
        pass
"""


@pytest.fixture
def pytorch_model(tmp_path):
    f = tmp_path / 'my_model.py'
    f.write_text(PYTORCH_MODEL_FILE_CONTENTS)

    sys.path.append(str(tmp_path))
    model_class = getattr(importlib.import_module('my_model'), 'MyModel')
    return model_class(), f


@pytest.fixture
def pytorch_model_init_args():
    return {'arg1': 1, 'arg2': 2, 'kwarg1': 3, 'kwarg2': 4}


@pytest.fixture
def pytorch_model_with_init_args(tmp_path, pytorch_model_init_args):
    f = tmp_path / 'my_model_with_init.py'
    f.write_text(PYTORCH_WITH_INIT_ARGS_MODEL_FILE_CONTENTS)

    sys.path.append(str(tmp_path))
    model_class = getattr(importlib.import_module('my_model_with_init'), 'MyModel')
    return model_class(**pytorch_model_init_args), f


@pytest.fixture
def custom_model(tmp_path):
    f = tmp_path / 'my_custom_model.py'
    f.write_text(CUSTOM_MODEL_CODE)
    return 'MyModel', f


@pytest.fixture
def no_load_custom_model(tmp_path):
    f = tmp_path / 'my_no_load_model.py'
    f.write_text(NO_LOAD_CUSTOM_MODEL_CODE)
    return 'MyModel', f


@pytest.fixture
def no_predict_custom_model(tmp_path):
    f = tmp_path / 'my_no_predict_model.py'
    f.write_text(NO_PREDICT_CUSTOM_MODEL_CODE)
    return 'MyModel', f


@pytest.fixture
def useless_file(tmp_path):
    f = tmp_path / 'useless.py'
    f.write_text('')
    sys.path.append(str(tmp_path))
    return f


@contextlib.contextmanager
def temp_dir(directory):
    """A context to allow user to drop into the temporary
    directory created by the tmp_path fixture"""
    current_dir = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(current_dir)
