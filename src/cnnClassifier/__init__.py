import os
import sys
import logging
from typing import List

class LoggerConfig:
    """
    A class for configuring and managing logging settings.
    """

    def __init__(self, log_dir: str = "logs", log_filename: str = "running_logs.log"):
        """
        Initializes the LoggerConfig object.

        Args:
            log_dir: The directory to store the log file.
            log_filename: The name of the log file.
        """
        self.log_dir = log_dir
        self.log_filename = log_filename
        self.logging_format = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

    def configure_logger(self, logger_name: str = "cnnClassifierLogger") -> logging.Logger:
        """
        Configures a logger with the specified name.

        Args:
            logger_name: The name of the logger to configure.

        Returns:
            The configured logger instance.
        """

        log_filepath = os.path.join(self.log_dir, self.log_filename)
        os.makedirs(self.log_dir, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format=self.logging_format,
            handlers=[
                logging.FileHandler(log_filepath),
                logging.StreamHandler(sys.stdout)
            ]
        )

        logger = logging.getLogger(logger_name)
        return logger
    

logger = LoggerConfig().configure_logger()  
 
