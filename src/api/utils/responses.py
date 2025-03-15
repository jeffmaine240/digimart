from typing import Optional, Union, List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json


def success_response(status_code: int, 
                     message: str, 
                     data: Optional[Union[Dict[str, Any], List[Any]]] = None, 
                     status: str = "success"):
\
    response_data = {
        "status": status,
        "status_code": status_code,
        "message": message
    }

    if data is not None:
        response_data["data"] = data

    return JSONResponse(status_code=status_code,
                        content=jsonable_encoder(response_data))



def error_response(status_code: int,
                   message: str,
                   data: Optional[Union[Dict[str, Any],
                                        List[Dict[str, Any]]]] = None,
                   status: str = "error"):
    '''
    Returns a JSON response for error responses
    
    Args:
        status_code: HTTP status code
        message: Error message
        data: Error details
        status: Response status string
        
    Returns:
        JSONResponse with standardized error format
    '''

    response_data = {
        "status": status,
        "status_code": status_code,
        "message": message
    }

    if data is not None:
        if isinstance(data, dict) and "error" in data and isinstance(
                data["error"], str):
            try:
                data["error"] = json.loads(data["error"])
            except json.JSONDecodeError:
                # If it's not a valid JSON string, keep it as is
                pass
        response_data["data"] = data

    return JSONResponse(status_code=status_code,
                        content=jsonable_encoder(response_data))
