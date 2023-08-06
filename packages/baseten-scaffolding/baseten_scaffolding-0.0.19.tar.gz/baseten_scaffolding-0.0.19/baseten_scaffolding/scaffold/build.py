from typing import Any, Dict, List

from baseten_scaffolding.constants import SKLEARN, PYTORCH, TENSORFLOW, CUSTOM, KERAS
from baseten_scaffolding.definitions.base import ReadModelScaffoldDefinition
from baseten_scaffolding.definitions.custom import CustomScaffoldDefinition
from baseten_scaffolding.definitions.keras import KerasScaffoldDefinition
from baseten_scaffolding.definitions.pytorch import PyTorchScaffoldDefinition
from baseten_scaffolding.definitions.sklearn import SKLearnScaffoldDefinition
from baseten_scaffolding.model_inference import (
    infer_model_information, infer_python_version, validate_provided_parameters_with_model
)


def scaffold(
    model: Any,
    model_files: List[str] = None,
    data_files: List[str] = None,
    target_directory: str = None,
    requirements_file: str = None,
    model_init_parameters: Dict[str, Any] = None,
):
    """Create a scaffold directory and object with the given model. A scaffold directory is a build context designed to
    be built as a container locally or uploaded into a baseten serving environment.

    Args:
        model (an in-memory model object): A model object to be deployed (e.g. a keras, sklearn, or pytorch model
            object)
        model_files (List[str], optional): Additional files required for model definition, e.g class
            definitions for pytorch models or other python code. Can be a glob that resolves to files for the root
            directory or a directory path. Files and directories here will be on the Python path
        data_files (List[str], optional): Additional files required for model operation. Can be a glob that resolves to
            files for the root directory or a directory path.
        target_directory (str, optional): The local directory target for the scaffold. Otherwise a temporary directory
            will be generated
        requirements_file (str, optional): A file of packages in a PIP requirements format to be installed in the
            container environment.
        model_init_parameters (Dict[str, Any], optional): A dictionary of named parameters to be passed to the model's
            __init__ method. Only used for pytorch and custom models.
    Returns:
        WrittenModelScaffoldDefinition
    """
    model_info = infer_model_information(model)
    python_major_minor = infer_python_version()
    model_type, model_framework = model_info.model_type, model_info.model_framework

    if model_framework == SKLEARN:
        return SKLearnScaffoldDefinition(
            model=model,
            model_type=model_type,
            model_files=model_files,
            data_files=data_files,
            path_to_scaffold=target_directory,
            requirements_file=requirements_file,
            python_major_minor=python_major_minor,
        )
    elif model_framework == PYTORCH:
        validate_provided_parameters_with_model(model.__class__, model_init_parameters)
        return PyTorchScaffoldDefinition(
            model=model,
            model_type=model_type,
            model_files=model_files,
            data_files=data_files,
            path_to_scaffold=target_directory,
            requirements_file=requirements_file,
            python_major_minor=python_major_minor,
            model_init_parameters=model_init_parameters,
        )
    elif model_framework == TENSORFLOW or model_framework == KERAS:
        return KerasScaffoldDefinition(
            model=model,
            model_type=model_type,
            model_files=model_files,
            data_files=data_files,
            path_to_scaffold=target_directory,
            requirements_file=requirements_file,
            python_major_minor=python_major_minor,
        )
    else:
        raise NotImplementedError('The model framework is not supported')


def scaffold_custom(
    model_files: List[str] = None,
    data_files: List[str] = None,
    target_directory: str = None,
    requirements_file: str = None,
    model_class: str = None,
    model_init_parameters: Dict[str, Any] = None,
):
    """Create a scaffold directory and object for a custom model. A scaffold directory is a build context designed to
        be built as a container locally or uploaded into a baseten serving environment.

       Args:
           model_files (List[str], optional): Additional files required for model definition, e.g class
               definitions for pytorch models or other python code. Can be a glob that resolves to files for the root
               directory or a directory path. Files and directories here will be in the Python path in the container
           data_files (List[str], optional): Additional files required for model operation. Can be a glob that resolves to
               files for the root directory or a directory path.
           target_directory (str, optional): The local directory target for the scaffold. Otherwise a temporary directory
               will be generated
           requirements_file (str, optional): A file of packages in a PIP requirements format to be installed in the
               container environment.
            model_class (str, optional): The python class name for a model object that exists in code within
                `model_files`
            model_init_parameters (Dict[str, Any], optional): A dictionary of named parameters to be passed to the model's
                __init__ method. Only used for pytorch and custom models.
       Returns:
           WrittenModelScaffoldDefinition
       """
    python_major_minor = infer_python_version()
    return CustomScaffoldDefinition(
        model=None,
        model_files=model_files,
        data_files=data_files,
        path_to_scaffold=target_directory,
        requirements_file=requirements_file,
        model_class=model_class,
        python_major_minor=python_major_minor,
        model_init_parameters=model_init_parameters
    )


def scaffold_from_directory(
    scaffold_directory: str
):
    """Create a scaffold object for a scaffold directory. A scaffold directory is a build context designed to be built
       as a container locally or uploaded into a baseten serving environment.

       Args:
           scaffold_directory (str): The local directory of an existing scaffold
       Returns:
           ReadModelScaffoldDefinition
       """
    return ReadModelScaffoldDefinition(scaffold_directory)
