# Taken from kfserving: https://github.com/kubeflow/kfserving/blob/master/python/pytorchserver/pytorchserver/model.py

import importlib
import logging
import os
import pathlib
import sys
import traceback
from typing import Any, Dict

import kfserving
import torch

PYTORCH_FILE = "model.pt"


class PyTorchModel(kfserving.KFModel):
    def __init__(
        self,
        name: str,
        model_class_name: str,
        model_class_file: str,
        model_dir: str,
        use_gpu: bool = False,
        model_init_parameters: Dict[str, Any] = None,
    ):
        super().__init__(name)
        self.name = name
        self.model_class_name = model_class_name
        self.model_class_file = model_class_file
        self.model_dir = model_dir
        self.model = None
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() and use_gpu else "cpu"
        )
        self.model_dtype = None
        self.model_init_parameters = model_init_parameters

    def load(self):
        # Load the python class into memory
        model_class_file = pathlib.PurePath(self.model_dir, self.model_class_file)
        sys.path.append(os.path.dirname(model_class_file))
        sys.path.append(self.model_dir)
        modulename = os.path.basename(model_class_file).split(".")[0].replace("-", "_")
        model_class = getattr(
            importlib.import_module(modulename), self.model_class_name
        )

        # Make sure the model weights are transformed to the right device in this machine
        weights_file = pathlib.PurePath(self.model_dir, PYTORCH_FILE).as_posix()
        self.model = model_class(**self.model_init_parameters).to(self.device)
        self.model.load_state_dict(torch.load(weights_file, map_location=self.device))
        self.model.eval()
        self.model_dtype = list(self.model.parameters())[0].dtype
        self.ready = True

    def preprocess(self, request: Dict) -> Dict:
        """
        Incorporate any pre-processing information required by the model here.

        These might be feature transformations that are tightly coupled to the model.
        """
        return request

    def postprocess(self, request: Dict) -> Dict:
        """
        Incorporate any post-processing required by the model here.
        """
        return request

    def predict(self, request: Dict) -> Dict:
        response = {}
        try:
            with torch.no_grad():
                inputs = torch.tensor(
                    request["inputs"], dtype=self.model_dtype, device=self.device
                )
                response = {}
                response["predictions"] = self.model(inputs).tolist()
                return response
        except Exception as e:
            response["error"] = {"traceback": traceback.format_exc()}
            logging.error(traceback.format_exc())
            return response
