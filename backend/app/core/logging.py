"""Logging configuration for LaudatorAI."""

import logging
import sys
from typing import Any, Dict
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    """Setup logging configuration."""
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger - only use stdout for Railway
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    logging.getLogger("minio").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    
    # Create logger for the application
    logger = logging.getLogger("laudatorai")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(f"laudatorai.{name}")


class StructuredLogger:
    """Structured logger for consistent log formatting."""
    
    def __init__(self, name: str):
        self.logger = get_logger(name)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with structured data."""
        self.logger.info(f"{message} | {self._format_kwargs(kwargs)}")
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with structured data."""
        self.logger.error(f"{message} | {self._format_kwargs(kwargs)}")
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with structured data."""
        self.logger.warning(f"{message} | {self._format_kwargs(kwargs)}")
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with structured data."""
        self.logger.debug(f"{message} | {self._format_kwargs(kwargs)}")
    
    def _format_kwargs(self, kwargs: Dict[str, Any]) -> str:
        """Format keyword arguments for logging."""
        if not kwargs:
            return ""
        return " ".join([f"{k}={v}" for k, v in kwargs.items()])


# Initialize logging
logger = setup_logging()


def log_request(request_id: str, method: str, path: str, status_code: int, duration: float) -> None:
    """Log HTTP request details."""
    logger.info(
        f"HTTP Request | request_id={request_id} | method={method} | path={path} | status_code={status_code} | duration={duration:.3f}s"
    )


def log_task_start(task_id: str, task_type: str, **kwargs: Any) -> None:
    """Log task start."""
    kwargs_str = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.info(f"Task Started | task_id={task_id} | task_type={task_type} {kwargs_str}")


def log_task_complete(task_id: str, task_type: str, duration: float, **kwargs: Any) -> None:
    """Log task completion."""
    kwargs_str = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.info(f"Task Completed | task_id={task_id} | task_type={task_type} | duration={duration:.3f}s {kwargs_str}")


def log_task_error(task_id: str, task_type: str, error: str, **kwargs: Any) -> None:
    """Log task error."""
    kwargs_str = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.error(f"Task Error | task_id={task_id} | task_type={task_type} | error={error} {kwargs_str}")


def log_file_operation(operation: str, file_path: str, success: bool, **kwargs: Any) -> None:
    """Log file operation."""
    kwargs_str = " ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
    logger.info(f"File Operation | operation={operation} | file_path={file_path} | success={success} {kwargs_str}")
