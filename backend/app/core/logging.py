"""Logging configuration for LaudatorAI."""

import logging
import sys
import json
import traceback
import time
from typing import Any, Dict, Optional
from pathlib import Path
from datetime import datetime
import os

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields if they exist
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'duration'):
            log_entry['duration'] = record.duration
        if hasattr(record, 'status_code'):
            log_entry['status_code'] = record.status_code
        if hasattr(record, 'method'):
            log_entry['method'] = record.method
        if hasattr(record, 'path'):
            log_entry['path'] = record.path
        if hasattr(record, 'ip_address'):
            log_entry['ip_address'] = record.ip_address
        if hasattr(record, 'user_agent'):
            log_entry['user_agent'] = record.user_agent
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_entry)


def setup_logging() -> logging.Logger:
    """Setup logging configuration with structured JSON logging."""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with JSON formatting for production
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.ENVIRONMENT == "production":
        console_handler.setFormatter(JSONFormatter())
    else:
        # Human-readable format for development
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
    
    root_logger.addHandler(console_handler)
    
    # File handler for persistent logs (development only)
    if settings.ENVIRONMENT != "production":
        file_handler = logging.FileHandler(logs_dir / "app.log")
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    logging.getLogger("minio").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
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
        extra = self._prepare_extra(kwargs)
        self.logger.info(message, extra=extra)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with structured data."""
        extra = self._prepare_extra(kwargs)
        self.logger.error(message, extra=extra)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with structured data."""
        extra = self._prepare_extra(kwargs)
        self.logger.warning(message, extra=extra)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with structured data."""
        extra = self._prepare_extra(kwargs)
        self.logger.debug(message, extra=extra)
    
    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        extra = self._prepare_extra(kwargs)
        self.logger.exception(message, extra=extra)
    
    def _prepare_extra(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare extra fields for logging."""
        return kwargs


# Initialize logging
logger = setup_logging()


def log_request(request_id: str, method: str, path: str, status_code: int, duration: float, 
                ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> None:
    """Log HTTP request details."""
    extra = {
        'request_id': request_id,
        'method': method,
        'path': path,
        'status_code': status_code,
        'duration': duration,
        'ip_address': ip_address,
        'user_agent': user_agent
    }
    logger.info(f"HTTP Request | {method} {path} | {status_code} | {duration:.3f}s", extra=extra)


def log_api_call(api_name: str, method: str, endpoint: str, status_code: int, duration: float, 
                 request_id: Optional[str] = None, user_id: Optional[str] = None) -> None:
    """Log API call details."""
    extra = {
        'api_name': api_name,
        'method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'duration': duration,
        'request_id': request_id,
        'user_id': user_id
    }
    logger.info(f"API Call | {api_name} | {method} {endpoint} | {status_code} | {duration:.3f}s", extra=extra)


def log_task_start(task_id: str, task_type: str, **kwargs: Any) -> None:
    """Log task start."""
    extra = {'task_id': task_id, 'task_type': task_type, **kwargs}
    logger.info(f"Task Started | {task_type} | {task_id}", extra=extra)


def log_task_complete(task_id: str, task_type: str, duration: float, **kwargs: Any) -> None:
    """Log task completion."""
    extra = {'task_id': task_id, 'task_type': task_type, 'duration': duration, **kwargs}
    logger.info(f"Task Completed | {task_type} | {task_id} | {duration:.3f}s", extra=extra)


def log_task_error(task_id: str, task_type: str, error: str, **kwargs: Any) -> None:
    """Log task error."""
    extra = {'task_id': task_id, 'task_type': task_type, 'error': error, **kwargs}
    logger.error(f"Task Error | {task_type} | {task_id} | {error}", extra=extra)


def log_file_operation(operation: str, file_path: str, success: bool, **kwargs: Any) -> None:
    """Log file operation."""
    extra = {'operation': operation, 'file_path': file_path, 'success': success, **kwargs}
    logger.info(f"File Operation | {operation} | {file_path} | {'SUCCESS' if success else 'FAILED'}", extra=extra)


def log_database_operation(operation: str, table: str, success: bool, duration: float, **kwargs: Any) -> None:
    """Log database operation."""
    extra = {'operation': operation, 'table': table, 'success': success, 'duration': duration, **kwargs}
    logger.info(f"Database | {operation} | {table} | {'SUCCESS' if success else 'FAILED'} | {duration:.3f}s", extra=extra)


def log_external_api_call(service: str, endpoint: str, method: str, status_code: int, duration: float, **kwargs: Any) -> None:
    """Log external API call."""
    extra = {'service': service, 'endpoint': endpoint, 'method': method, 'status_code': status_code, 'duration': duration, **kwargs}
    logger.info(f"External API | {service} | {method} {endpoint} | {status_code} | {duration:.3f}s", extra=extra)


def log_user_action(user_id: str, action: str, resource: str, success: bool, **kwargs: Any) -> None:
    """Log user action."""
    extra = {'user_id': user_id, 'action': action, 'resource': resource, 'success': success, **kwargs}
    logger.info(f"User Action | {user_id} | {action} | {resource} | {'SUCCESS' if success else 'FAILED'}", extra=extra)


def log_performance_metric(metric_name: str, value: float, unit: str, **kwargs: Any) -> None:
    """Log performance metric."""
    extra = {'metric_name': metric_name, 'value': value, 'unit': unit, **kwargs}
    logger.info(f"Performance | {metric_name} | {value} {unit}", extra=extra)


def log_security_event(event_type: str, severity: str, details: str, **kwargs: Any) -> None:
    """Log security event."""
    extra = {'event_type': event_type, 'severity': severity, 'details': details, **kwargs}
    if severity.upper() in ['HIGH', 'CRITICAL']:
        logger.error(f"Security Event | {event_type} | {severity} | {details}", extra=extra)
    else:
        logger.warning(f"Security Event | {event_type} | {severity} | {details}", extra=extra)
