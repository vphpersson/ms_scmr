from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RQueryServiceConfigWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INSUFFICIENT_BUFFER = 122
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RQueryServiceConfigErrorW(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RQueryServiceConfigWReturnCode, Type[RQueryServiceConfigErrorW]] = {}


class AccessDeniedError(RQueryServiceConfigErrorW):
    RETURN_CODE = RQueryServiceConfigWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The access specified cannot be granted to the caller.'


class InvalidHandleError(RQueryServiceConfigErrorW):
    RETURN_CODE = RQueryServiceConfigWReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class InsufficientBufferError(RQueryServiceConfigErrorW):
    DESCRIPTION = 'The data area passed to a system call is too small.'


class ShutdownInProgressError(RQueryServiceConfigErrorW):
    RETURN_CODE = RQueryServiceConfigWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RQueryServiceConfigErrorW.RETURN_CODE_TO_ERROR_CLASS.update({
    RQueryServiceConfigWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RQueryServiceConfigWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RQueryServiceConfigWReturnCode.ERROR_INSUFFICIENT_BUFFER: InsufficientBufferError,
    RQueryServiceConfigWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
