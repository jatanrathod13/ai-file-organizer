import logging
import sys
from pathlib import Path
from config import LOG_FILE, LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_file_operation(logger: logging.Logger, operation: str, file_path: Path, 
                      success: bool, error: Exception = None) -> None:
    """
    Log file operations with consistent formatting.
    
    Args:
        logger (logging.Logger): Logger instance
        operation (str): Type of operation (e.g., "move", "copy", "delete")
        file_path (Path): Path to the file
        success (bool): Whether the operation was successful
        error (Exception, optional): Exception if operation failed
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"File {operation.upper()} - {status} - {file_path}"
    
    if success:
        logger.info(message)
    else:
        logger.error(f"{message} - Error: {str(error)}") 