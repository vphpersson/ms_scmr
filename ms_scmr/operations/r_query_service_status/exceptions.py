from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RQueryServiceStatusReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_PATH_NOT_FOUND = 3
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RQueryServiceStatusError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RQueryServiceStatusReturnCode, Type[RQueryServiceStatusError]] = {}


class AccessDeniedError(RQueryServiceStatusError):
    RETURN_CODE = RQueryServiceStatusReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The access specified cannot be granted to the caller.'


class InvalidHandleError(RQueryServiceStatusError):
    RETURN_CODE = RQueryServiceStatusReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class PathNotFoundError(RQueryServiceStatusError):
    RETURN_CODE = RQueryServiceStatusReturnCode.ERROR_PATH_NOT_FOUND
    DESCRIPTION = 'The ImagePath of the service record identified by the hService parameter does not exist.'


class ShutdownInProgressError(RQueryServiceStatusError):
    RETURN_CODE = RQueryServiceStatusReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RQueryServiceStatusError.RETURN_CODE_TO_ERROR_CLASS.update({
    RQueryServiceStatusReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RQueryServiceStatusReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RQueryServiceStatusReturnCode.ERROR_PATH_NOT_FOUND: PathNotFoundError,
    RQueryServiceStatusReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
