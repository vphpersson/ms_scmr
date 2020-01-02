from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RCloseServiceHandleReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_INVALID_HANDLE = 6
    ERROR_SUCCESS_LAST_NOTIFY_STATUS_CHANGE_HANDLE = 0xFFFF75FD
    ERROR_SUCCESS_USED_IN_NOTIFY_STATUS_CHANGE = 0xFFFF75FE


class RCloseServiceHandleError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RCloseServiceHandleReturnCode, Type[RCloseServiceHandleError]] = {}


class InvalidHandleError(RCloseServiceHandleError):
    RETURN_CODE = RCloseServiceHandleReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


RCloseServiceHandleError.RETURN_CODE_TO_ERROR_CLASS.update({
    RCloseServiceHandleReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError
})
