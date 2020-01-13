from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RDeleteServiceReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_SERVICE_MARKED_FOR_DELETE = 1072
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RDeleteServiceError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RDeleteServiceReturnCode, Type[RDeleteServiceError]] = {}


class AccessDeniedError(RDeleteServiceError):
    RETURN_CODE = RDeleteServiceReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The DELETE access right had not been granted to the caller when the RPC context handle to the service record was created.'


class InvalidHandleError(RDeleteServiceError):
    RETURN_CODE = RDeleteServiceReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class ServiceMarkedForDeleteError(RDeleteServiceError):
    RETURN_CODE = RDeleteServiceReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE
    DESCRIPTION = 'The RDeleteService has already been called for the service record identified by the hService parameter.'


class ShutdownInProgressError(RDeleteServiceError):
    RETURN_CODE = RDeleteServiceReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RDeleteServiceError.RETURN_CODE_TO_ERROR_CLASS.update({
    RDeleteServiceReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RDeleteServiceReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RDeleteServiceReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE: ServiceMarkedForDeleteError,
    RDeleteServiceReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
