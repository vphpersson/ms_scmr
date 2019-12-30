from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum

from ms_scmr.base import MSSCMRResponseError


class RChangeServiceConfigWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_PARAMETER = 87
    ERROR_INVALID_SERVICE_ACCOUNT = 1057
    ERROR_CIRCULAR_DEPENDENCY = 1059
    ERROR_DUPLICATE_SERVICE_NAME = 1078
    ERROR_SERVICE_MARKED_FOR_DELETE = 1072
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RChangeServiceConfigWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RChangeServiceConfigWReturnCode, Type[RChangeServiceConfigWError]] = {}


class AccessDeniedError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The SERVICE_CHANGE_CONFIG access right had not been granted to the caller when the RPC context handle to the service record was created.'


class InvalidHandleError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class InvalidParamaterError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_INVALID_PARAMETER
    DESCRIPTION = 'A parameter that was specified is invalid.'


class InvalidServiceAccountError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_INVALID_SERVICE_ACCOUNT
    DESCRIPTION = 'The user account name specified in the lpServiceStartName parameter does not exist.'


class CircularDependencyError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_CIRCULAR_DEPENDENCY
    DESCRIPTION = 'A circular service dependency was specified.'


class DuplicateServiceNameError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_DUPLICATE_SERVICE_NAME
    DESCRIPTION = 'The lpDisplayName matches either the ServiceName or the DisplayName of another service record in the service control manager database.'


class ServiceMarkedForDeleteError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE
    DESCRIPTION = 'The RDeleteService has been called for the service record identified by the hService parameter.'


class ShutdownInProgressError(RChangeServiceConfigWError):
    RETURN_CODE = RChangeServiceConfigWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RChangeServiceConfigWError.RETURN_CODE_TO_ERROR_CLASS.update({
    RChangeServiceConfigWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RChangeServiceConfigWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RChangeServiceConfigWReturnCode.ERROR_INVALID_PARAMETER: InvalidParamaterError,
    RChangeServiceConfigWReturnCode.ERROR_INVALID_SERVICE_ACCOUNT: InvalidServiceAccountError,
    RChangeServiceConfigWReturnCode.ERROR_CIRCULAR_DEPENDENCY: CircularDependencyError,
    RChangeServiceConfigWReturnCode.ERROR_DUPLICATE_SERVICE_NAME: DuplicateServiceNameError,
    RChangeServiceConfigWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE: ServiceMarkedForDeleteError,
    RChangeServiceConfigWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
