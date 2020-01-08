from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RCreateServiceWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_DATA = 13
    ERROR_INVALID_PARAMETER = 87
    ERROR_INVALID_NAME = 123
    ERROR_INVALID_SERVICE_ACCOUNT = 1057
    ERROR_CIRCULAR_DEPENDENCY = 1059
    ERROR_SERVICE_MARKED_FOR_DELETE = 1072
    ERROR_SERVICE_EXISTS = 1073
    ERROR_DUPLICATE_SERVICE_NAME = 1078
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RCreateServiceWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RCreateServiceWReturnCode, Type[RCreateServiceWError]] = {}


class AccessDeniedError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The SC_MANAGER_CREATE_SERVICE access right had not been granted to the caller when the RPC context handle was created.'


class InvalidHandleError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle specified is invalid.'


class InvalidDataError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_INVALID_DATA
    DESCRIPTION = 'The data is invalid.'


class InvalidParameterError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_INVALID_PARAMETER
    DESCRIPTION = 'A parameter that was specified is invalid.'


class InvalidNameError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_INVALID_NAME
    DESCRIPTION = 'The specified service name is invalid.'


class InvalidServiceAccountError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_INVALID_SERVICE_ACCOUNT
    DESCRIPTION = 'The user account name specified in the lpServiceStartName parameter does not exist.'


class CircularDependencyError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_CIRCULAR_DEPENDENCY
    DESCRIPTION = 'A circular service dependency was specified.'


class ServiceMarkedForDeleteError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE
    DESCRIPTION = 'The service record with a specified name already exists and RDeleteService has been called for it.'


class ServiceExistsError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_SERVICE_EXISTS
    DESCRIPTION = 'The service record with the ServiceName matching the specified lpServiceName already exists.'


class DuplicateServiceNameError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_DUPLICATE_SERVICE_NAME
    DESCRIPTION = 'The service record with the same DisplayName or the same ServiceName as the passed in lpDisplayName already exists in the service control manager database.'


class ShutdownInProgressError(RCreateServiceWError):
    RETURN_CODE = RCreateServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RCreateServiceWError.RETURN_CODE_TO_ERROR_CLASS.update({
    RCreateServiceWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RCreateServiceWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RCreateServiceWReturnCode.ERROR_INVALID_DATA: InvalidDataError,
    RCreateServiceWReturnCode.ERROR_INVALID_PARAMETER: InvalidParameterError,
    RCreateServiceWReturnCode.ERROR_INVALID_NAME: InvalidNameError,
    RCreateServiceWReturnCode.ERROR_INVALID_SERVICE_ACCOUNT: InvalidServiceAccountError,
    RCreateServiceWReturnCode.ERROR_CIRCULAR_DEPENDENCY: CircularDependencyError,
    RCreateServiceWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE: ServiceMarkedForDeleteError,
    RCreateServiceWReturnCode.ERROR_SERVICE_EXISTS: ServiceExistsError,
    RCreateServiceWReturnCode.ERROR_DUPLICATE_SERVICE_NAME: DuplicateServiceNameError,
    RCreateServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
