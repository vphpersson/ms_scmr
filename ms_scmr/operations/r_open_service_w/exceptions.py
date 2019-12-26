from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class ROpenServiceWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_NAME = 123
    ERROR_SERVICE_DOES_NOT_EXIST = 1060
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class ROpenServiceWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[ROpenServiceWReturnCode, Type[ROpenServiceWError]] = {}


class AccessDeniedError(ROpenServiceWError):
    RETURN_CODE = ROpenServiceWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The access specified cannot be granted to the caller.'


class InvalidHandleError(ROpenServiceWError):
    RETURN_CODE = ROpenServiceWReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class InvalidNameError(ROpenServiceWError):
    RETURN_CODE = ROpenServiceWReturnCode.ERROR_INVALID_NAME
    DESCRIPTION = 'The specified service name is invalid.'


class ServiceDoesNotExistError(ROpenServiceWError):
    RETURN_CODE = ROpenServiceWReturnCode.ERROR_SERVICE_DOES_NOT_EXIST
    DESCRIPTION = 'The service record with a specified DisplayName does not exist in the SCM database.'


class ShutdownInProgressError(ROpenServiceWError):
    RETURN_CODE = ROpenServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


ROpenServiceWError.RETURN_CODE_TO_ERROR_CLASS.update({
    ROpenServiceWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    ROpenServiceWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    ROpenServiceWReturnCode.ERROR_INVALID_NAME: InvalidNameError,
    ROpenServiceWReturnCode.ERROR_SERVICE_DOES_NOT_EXIST: ServiceDoesNotExistError,
    ROpenServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
