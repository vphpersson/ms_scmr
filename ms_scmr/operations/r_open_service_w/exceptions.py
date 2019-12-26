from __future__ import annotations
from abc import ABC
from typing import Dict, Type


from ms_scmr.base import MSSCMRResponseError
from ms_scmr.operations.r_open_service_w.r_open_service_w_response import ROpenServiceWReturnCode


class ROpenServiceWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[ROpenServiceWReturnCode, Type[ROpenServiceWError]] = NotImplemented


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


ROpenServiceWError.RETURN_CODE_TO_ERROR_CLASS = {
    ROpenServiceWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    ROpenServiceWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    ROpenServiceWReturnCode.ERROR_INVALID_NAME: InvalidNameError,
    ROpenServiceWReturnCode.ERROR_SERVICE_DOES_NOT_EXIST: ServiceDoesNotExistError,
    ROpenServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
}
