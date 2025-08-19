"""Frontend logging endpoint."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Any, Dict
import time

from app.core.logging import logger, log_security_event

router = APIRouter()


class FrontendLogData(BaseModel):
    level: str
    name: str
    timestamp: str
    message: str
    url: Optional[str] = None
    userAgent: Optional[str] = None
    sessionId: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    serverTimestamp: Optional[str] = None
    serverEnvironment: Optional[str] = None
    serverRegion: Optional[str] = None
    serverUrl: Optional[str] = None


@router.post("/logs")
async def receive_frontend_logs(log_data: FrontendLogData, request: Request):
    """Receive and process frontend logs."""
    start_time = time.time()
    
    try:
        # Extract client information
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log the frontend log with context
        log_level = log_data.level.upper()
        log_message = f"Frontend Log | {log_data.name} | {log_data.message}"
        
        # Prepare extra data for structured logging
        extra_data = {
            'frontend_logger': log_data.name,
            'frontend_timestamp': log_data.timestamp,
            'session_id': log_data.sessionId,
            'client_url': log_data.url,
            'client_user_agent': log_data.userAgent,
            'server_timestamp': log_data.serverTimestamp,
            'server_environment': log_data.serverEnvironment,
            'server_region': log_data.serverRegion,
            'server_url': log_data.serverUrl,
            'client_ip': client_ip,
            'request_user_agent': user_agent,
        }
        
        if log_data.data:
            extra_data['frontend_data'] = log_data.data
        
        # Log based on level
        if log_level == "ERROR":
            logger.error(log_message, extra=extra_data)
        elif log_level == "WARN":
            logger.warning(log_message, extra=extra_data)
        elif log_level == "DEBUG":
            logger.debug(log_message, extra=extra_data)
        else:  # INFO or default
            logger.info(log_message, extra=extra_data)
        
        # Check for security-related events
        if log_data.data and isinstance(log_data.data, dict):
            if 'security_event' in log_data.data or 'security' in log_data.message.lower():
                log_security_event(
                    event_type="frontend_security",
                    severity="medium",
                    details=f"Frontend security event: {log_data.message}",
                    **extra_data
                )
        
        # Calculate processing time
        duration = time.time() - start_time
        
        # Log the API call itself
        logger.info(
            f"Frontend Log API Call | POST /api/v1/logs | 200 | {duration:.3f}s",
            extra={
                'api_name': 'frontend_logs',
                'method': 'POST',
                'endpoint': '/api/v1/logs',
                'status_code': 200,
                'duration': duration,
                'session_id': log_data.sessionId,
            }
        )
        
        return {"success": True, "processed": True}
        
    except Exception as e:
        duration = time.time() - start_time
        logger.exception(
            f"Failed to process frontend log | {duration:.3f}s",
            extra={
                'api_name': 'frontend_logs',
                'method': 'POST',
                'endpoint': '/api/v1/logs',
                'status_code': 500,
                'duration': duration,
                'session_id': log_data.sessionId if log_data else None,
                'error': str(e),
            }
        )
        raise HTTPException(status_code=500, detail="Failed to process log")
