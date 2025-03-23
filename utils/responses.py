from typing import Optional, Union, List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json


from typing import Optional, Union, List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from datetime import datetime


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


def base_response(
    status_code: int,
    message: str,
    status: ResponseStatus,
    data: Optional[Union[Dict[str, Any], List[Any]]] = None,
    include_timestamp: bool = False
) -> JSONResponse:
    """
    Base response format for both success and error responses.
    
    Args:
        status_code: HTTP status code
        message: Message string
        status: ResponseStatus Enum ("success" or "error")
        data: Optional data payload
        include_timestamp: Whether to include timestamp in response

    Returns:
        JSONResponse
    """
    response_data = {
        "status": status.value,
        "status_code": status_code,
        "message": message
    }

    if data is not None:
        response_data["data"] = data

    if include_timestamp:
        response_data["timestamp"] = datetime.utcnow().isoformat()

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_data)
    )


def success_response(
    status_code: int,
    message: str,
    data: Optional[Union[Dict[str, Any], List[Any]]] = None,
    include_timestamp: bool = False
) -> JSONResponse:
    """
    Success response wrapper.
    """
    return base_response(
        status_code=status_code,
        message=message,
        status=ResponseStatus.SUCCESS,
        data=data,
        include_timestamp=include_timestamp
    )


def error_response(
    status_code: int,
    message: str,
    data: Optional[Union[Dict[str, Any], List[Any], Dict[str, List[Any]]]] = None,
    include_timestamp: bool = False
) -> JSONResponse:
    """
    Error response wrapper with smart error parsing.
    """
    if data is not None:
        if isinstance(data, dict) and "error" in data and isinstance(data["error"], str):
            try:
                # Try to parse error string into JSON if possible
                data["error"] = json.loads(data["error"])
            except json.JSONDecodeError:
                # Keep as string if not JSON
                pass

    return base_response(
        status_code=status_code,
        message=message,
        status=ResponseStatus.ERROR,
        data=data,
        include_timestamp=include_timestamp
    )
