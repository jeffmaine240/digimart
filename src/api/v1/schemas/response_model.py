from pydantic import BaseModel
from typing import Optional

class ErrorData(BaseModel):
    """Container for error data."""
    error_details: Optional[str] = None
    error_type: Optional[str] = None