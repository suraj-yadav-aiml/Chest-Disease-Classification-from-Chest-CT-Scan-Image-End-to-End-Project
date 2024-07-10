import os
from pathlib import Path
import logging
from typing import List

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


class TemplateCreator:
    """
    A class responsible for creating template of the project
    """

    def __init__(self, filepaths: List[str]):
        """
        Initializes the TemplateCreator with a list of file paths.

        Args:
            filepaths: A list of file paths to create.
        """
        self.filepaths = filepaths

    def create_files(self) -> None:
        """
        Creates empty files and their parent directories if they don't exist.
        """
        for filepath in self.filepaths:
            filepath = Path(filepath)  

            # Split the path into directory and filename components
            filedir, filename = os.path.split(filepath)

            if filedir != "":  # Check if there are parent directories to create
                os.makedirs(filedir, exist_ok=True)  
                logging.info(f"Creating directory {filedir} for the files {filename}")

            # Check if the file doesn't exist or is empty (0 bytes)
            if not filepath.is_file() or filepath.stat().st_size == 0: 
                filepath.touch()  # Create an empty file
                logging.info(f"Creating empty file : {filepath}")
            else:
                logging.info(f"{filename} is already exists")

if __name__ == "__main__":

    project_name = "cnnClassifier"

    list_of_files = [
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/utils/common.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        "config/config.yaml",
        "dvc.yaml",
        "params.yaml",
        "requirements.txt",
        "setup.py",
        "research/trials.ipynb",
        "templates/index.html"
        "main.py"
        ]

    creator = TemplateCreator(list_of_files)
    creator.create_files()