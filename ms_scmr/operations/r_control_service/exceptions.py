from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum
from ms_scmr.base import MSSCMRResponseError


class RControlServiceReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_DEPENDENT_SERVICES_RUNNING = 1051
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_PARAMETER = 87
    ERROR_INVALID_SERVICE_CONTROL = 1052
    ERROR_SERVICE_REQUEST_TIMEOUT = 1053
    ERROR_SERVICE_CANNOT_ACCEPT_CTRL = 1061
    ERROR_SERVICE_NOT_ACTIVE = 1062
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RControlServiceError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RControlServiceReturnCode, Type[RControlServiceError]] = {}


class AccessDeniedError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The required access right had not been granted to the caller when the RPC context handle to the service record was created.'


class DependentServicesRunningError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_DEPENDENT_SERVICES_RUNNING
    DESCRIPTION = 'The service cannot be stopped because other running services are dependent on it.'


class InvalidHandleError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class InvalidParameterError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_INVALID_PARAMETER
    DESCRIPTION = 'The requested control code is undefined'


class InvalidServiceControlError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_INVALID_SERVICE_CONTROL
    DESCRIPTION = 'The requested control code is not valid, or it is unacceptable to the service.'


class ServiceRequestTimeoutError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_SERVICE_REQUEST_TIMEOUT
    DESCRIPTION = 'The process for the service was started, but it did not respond within an implementation-specific time-out.'


class ServiceCannotAcceptCtrlError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_SERVICE_CANNOT_ACCEPT_CTRL
    DESCRIPTION = 'The requested control code cannot be sent to the service because the ServiceStatus.dwCurrentState in the service record is SERVICE_START_PENDING or SERVICE_STOP_PENDING.'


class ServiceNotActiveError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_SERVICE_NOT_ACTIVE
    DESCRIPTION = 'The service has not been started, or the ServiceStatus.dwCurrentState in the service record is SERVICE_STOPPED.'


class ShutdownInProgressError(RControlServiceError):
    RETURN_CODE = RControlServiceReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RControlServiceError.RETURN_CODE_TO_ERROR_CLASS.update({
    RControlServiceReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RControlServiceReturnCode.ERROR_DEPENDENT_SERVICES_RUNNING: DependentServicesRunningError,
    RControlServiceReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RControlServiceReturnCode.ERROR_INVALID_PARAMETER: InvalidParameterError,
    RControlServiceReturnCode.ERROR_INVALID_SERVICE_CONTROL: InvalidServiceControlError,
    RControlServiceReturnCode.ERROR_SERVICE_REQUEST_TIMEOUT: ServiceRequestTimeoutError,
    RControlServiceReturnCode.ERROR_SERVICE_CANNOT_ACCEPT_CTRL: ServiceCannotAcceptCtrlError,
    RControlServiceReturnCode.ERROR_SERVICE_NOT_ACTIVE: ServiceNotActiveError,
    RControlServiceReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})

