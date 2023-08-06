from marshmallow_dataclass import dataclass
from typing import List, Optional

from .enum import CallbackType


@dataclass
class Request:
    """Request base data class"""

    callback_type: Optional[CallbackType]
    callback_location: Optional[str]
    callback_token: Optional[str]
    err_callback_type: Optional[CallbackType]
    err_callback_location: Optional[str]
    err_callback_token: Optional[str]
    job_id: Optional[str]
    op_id: Optional[str]
    job_child_idx_list: Optional[List[int]]


@dataclass
class Response:
    code: int


@dataclass
class ResponseStatus(Response):
    status: str
    message: str


@dataclass
class ResponseError(Response):
    error: str
    code: int


@dataclass
class CallbackCreation:
    type: Optional[CallbackType]
    location: Optional[str]
    token: Optional[str]
