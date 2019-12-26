from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class ROpenSCManagerWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_NAME = 123
    ERROR_DATABASE_DOES_NOT_EXIST = 1065
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class ROpenSCManagerWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[ROpenSCManagerWReturnCode, Type[ROpenSCManagerWError]] = {}


class AccessDeniedError(ROpenSCManagerWError):
    RETURN_CODE = ROpenSCManagerWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The client does not have the required access rights to open the SCM database on the server or the ' \
                  'desired access is not granted to it in the SCM SecurityDescriptor.'


class InvalidNameError(ROpenSCManagerWError):
    RETURN_CODE = ROpenSCManagerWReturnCode.ERROR_INVALID_NAME
    DESCRIPTION = 'The specified service name is invalid.'


class DatabaseDoesNotExistError(ROpenSCManagerWError):
    RETURN_CODE = ROpenSCManagerWReturnCode.ERROR_DATABASE_DOES_NOT_EXIST
    DESCRIPTION = 'The database specified does not exist.'


class ShutdownInProgressError(ROpenSCManagerWError):
    RETURN_CODE = ROpenSCManagerWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


ROpenSCManagerWError.RETURN_CODE_TO_ERROR_CLASS.update({
    ROpenSCManagerWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    ROpenSCManagerWReturnCode.ERROR_INVALID_NAME: InvalidNameError,
    ROpenSCManagerWReturnCode.ERROR_DATABASE_DOES_NOT_EXIST: DatabaseDoesNotExistError,
    ROpenSCManagerWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
