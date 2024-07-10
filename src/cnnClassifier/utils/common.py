import os
import json
import yaml
import joblib
import base64

from pathlib import Path
from typing import Any,Union

from box.exceptions import BoxValueError
from box import ConfigBox

from ensure import ensure_annotations
from cnnClassifier import logger



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML configuration file and returns its contents as a ConfigBox.

    This function safely loads a YAML file specified by the `path_to_yaml`. If the file
    exists and is valid, it returns a ConfigBox object for easy access to the configuration data.

    Args:
        path_to_yaml (Path): A Path object representing the location of the YAML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the YAML file is empty or invalid.
        YamlError: If there's a more specific YAML parsing issue. 

    Returns:
        ConfigBox: A ConfigBox object containing the parsed YAML data.
    """
    try:
        with open(path_to_yaml, "r") as yaml_file: 
            content = yaml.safe_load(yaml_file)
        logger.info(f"YAML file: {path_to_yaml} loaded successfully.")
        return ConfigBox(content)

    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found at: {path_to_yaml}")

    except BoxValueError as e:  
        raise ValueError(f"Invalid YAML file: {e}") from e  

    except yaml.YAMLError as e:  
        raise yaml.YAMLError(f"Error parsing YAML: {e}") from e

    except Exception as e:  # Catch any unexpected exceptions
        logger.exception(f"An unexpected error occurred while reading {path_to_yaml}: {e}")
        raise e  

    




@ensure_annotations
def create_directories(paths_to_directories: list, verbose: bool = True) -> None:
    """
    Creates directories specified by a list of paths.

    This function takes a list of directory paths and creates
    them if they do not already exist. It provides an option to log the creation of each
    directory.

    Args:
        paths_to_directories (list): A list of Path objects representing the 
                                          directories to be created.
        verbose (bool, optional): If True (default), log messages will be displayed 
                                 indicating the creation of each directory.

    Returns:
        None
    """
    for path in paths_to_directories:
        try:
            os.makedirs(path, exist_ok=True)  # Create directory, skip if exists
            if verbose:
                logger.info(f"Created directory at: {path}")
        except OSError as e:
            logger.error(f"Error creating directory at {path}: {e}")



@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """
    Saves data to a JSON file.

    This function takes a dictionary of data and writes it to the specified JSON file.

    Args:
        path (Path): The path to the JSON file where the data should be saved.
        data (dict): The dictionary containing the data to be written to the file.

    Raises:
        TypeError: If the input `data` is not a dictionary.
        OSError: If an error occurs while writing to the file (e.g., permissions issue).
        json.JSONDecodeError: If there's an issue encoding the data into JSON format.

    Returns:
        None
    """

    if not isinstance(data, dict):
        raise TypeError("Input data must be a dictionary.")

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except (OSError, json.JSONDecodeError) as e:
        logger.error(f"Error saving JSON file to {path}: {e}")
        raise  e
    
    logger.info(f"JSON file saved at: {path}")



@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads data from a JSON file into a ConfigBox object.

    This function reads data from the specified JSON file and returns it as a
    ConfigBox, allowing easy access to the data using dot notation.

    Args:
        path (Path): The path to the JSON file to be loaded.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.

    Returns:
        ConfigBox: A ConfigBox object containing the loaded JSON data.
    """
    try:
        with open(path, "r") as f:  
            content = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at: {path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file at: {path}", e.doc, e.pos) from e  

    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)



@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """
    Saves data to a binary file using joblib.

    This function serializes the provided data using joblib and saves it to the
    specified binary file.

    Args:
        data (Any): The data to be serialized and saved.
        path (Path): The path to the binary file where the data should be saved.

    Raises:
        joblib.dump: If an error occurs during serialization or saving.

    Returns:
        None
    """
    try:
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.exception(f"Error saving binary file at: {path}. Exception: {e}")
        raise e



@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.

    This function deserializes the data stored in the specified binary file
    using joblib and returns the original Python object.

    Args:
        path (Path): The path to the binary file to be loaded.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        joblib.LoadError: If there is an error during deserialization.

    Returns:
        Any: The deserialized Python object.
    """
    try:
        data = joblib.load(path)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Binary file not found at: {path}")
    except Exception as e: 
        raise Exception(f"Error loading binary file from: {path}. {e}") from e  


@ensure_annotations
def get_size(path: Path, units: str = "KB") -> str:
    """
    Gets the size of a file in the specified units (KB, MB, or GB).

    This function calculates the size of a file and returns it as a human-readable
    string with the appropriate unit (kilobytes, megabytes, or gigabytes).

    Args:
        path (Path): The path to the file.
        units (str, optional): The desired unit for the size. Choose from "KB", 
                               "MB", or "GB". Defaults to "KB".

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If an invalid unit is provided.

    Returns:
        str: The size of the file as a formatted string, e.g., "~ 1.5 MB".
    """
    UNITS_MAPPING = {
        "KB": 1024,
        "MB": 1024**2,  # 1024 * 1024
        "GB": 1024**3   # 1024 * 1024 * 1024
    }

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found at: {path}")

    if units not in UNITS_MAPPING:
        raise ValueError(f"Invalid unit: {units}. Choose from KB, MB, or GB.")

    size_in_bytes = os.path.getsize(path)
    size_in_units = round(size_in_bytes / UNITS_MAPPING[units], 2)
    return f"~ {size_in_units} {units}"



@ensure_annotations
def decode_image(imgstring: str, filename: Union[str, Path]):
    """
    Decodes a base64-encoded image string and saves it to a file.

    This function takes a base64-encoded image string, decodes it, and saves the 
    resulting image data to the specified file.

    Args:
        imgstring (str): The base64-encoded image string.
        filename (Union[str, Path]): The name or path of the file where the 
                                     decoded image should be saved.

    Raises:
        OSError: If an error occurs while writing the file.

    Returns:
        None
    """

    imgdata = base64.b64decode(imgstring)

    filepath = Path(filename)  

    try:
        with open(filepath, "wb") as f:
            f.write(imgdata)
    except OSError as e:
        raise OSError(f"Unable to save image to {filepath}: {e}") from e

    logger.info(f"Decoded image saved at: {filepath}")


    
@ensure_annotations
def encode_image_to_base64(image_path: Union[str, Path]) -> str:
    """
    Encodes an image file into a base64 string.

    Reads an image file from the given path and converts its binary data into a 
    base64-encoded string.

    Args:
        image_path (Union[str, Path]): The path to the image file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If an error occurs while reading the file.
        TypeError: If the image path is not a string or Path object.

    Returns:
        str: The base64-encoded string representation of the image.
    """
    
    filepath = Path(image_path)  

    if not filepath.exists():
        raise FileNotFoundError(f"Image file not found at: {filepath}")

    try:
        with open(filepath, "rb") as f:  
            image_data = f.read()
            base64_string = base64.b64encode(image_data).decode("utf-8")  # Decode to string
            return base64_string
    except OSError as e:
        raise OSError(f"Unable to read image file at: {filepath}. Error: {e}") from e
