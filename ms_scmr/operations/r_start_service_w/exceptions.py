from __future__ import annotations
from abc import ABC
from typing import Dict, Type
from enum import IntEnum
from ms_scmr.base import MSSCMRResponseError


class RStartServiceWReturnCode(IntEnum):
    ERROR_FILE_NOT_FOUND = 2
    ERROR_PATH_NOT_FOUND = 3
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_PARAMETER = 87
    ERROR_SERVICE_REQUEST_TIMEOUT = 1053
    ERROR_SERVICE_NO_THREAD = 1054
    ERROR_SERVICE_DATABASE_LOCKED = 1055
    ERROR_SERVICE_ALREADY_RUNNING = 1056
    ERROR_SERVICE_DISABLED = 1058
    ERROR_SERVICE_DEPENDENCY_FAIL = 1068
    ERROR_SERVICE_LOGON_FAILED = 1069
    ERROR_SERVICE_MARKED_FOR_DELETE = 1072
    ERROR_SERVICE_DEPENDENCY_DELETED = 1075
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


class RStartServiceWError(MSSCMRResponseError, ABC):
    RETURN_CODE_TO_ERROR_CLASS: Dict[RStartServiceWReturnCode, Type[RStartServiceWError]] = {}


class SCMRFileNotFoundError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_FILE_NOT_FOUND
    DESCRIPTION = 'The system cannot find the file specified.'


class PathNotFoundError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_PATH_NOT_FOUND
    DESCRIPTION = 'The system cannot find the path specified.'


class AccessDeniedError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_ACCESS_DENIED
    DESCRIPTION = 'The SERVICE_START access right had not been granted to the caller when the RPC context handle to the service record was created.'


class InvalidHandleError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_INVALID_HANDLE
    DESCRIPTION = 'The handle is no longer valid.'


class InvalidParameterError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_INVALID_PARAMETER
    DESCRIPTION = 'A parameter that was specified is invalid.'


class ServiceRequestTimeoutError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_REQUEST_TIMEOUT
    DESCRIPTION = 'The process for the service was started, but it did not respond within an implementation-specific time-out.'


class ServiceNoThreadError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_NO_THREAD
    DESCRIPTION = 'A thread could not be created for the service.'


class ServiceDatabaseLockedError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_DATABASE_LOCKED
    DESCRIPTION = 'The service database is locked by the call to the BlockServiceDatabase method.'


class ServiceAlreadyRunningError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_ALREADY_RUNNING
    DESCRIPTION = 'The ServiceStatus.dwCurrentState in the service record is not set to SERVICE_STOPPED.'


class ServiceDisabledError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_DISABLED
    DESCRIPTION = 'The service cannot be started because the Start field in the service record is set to SERVICE_DISABLED.'


class ServiceDependencyFailError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_DEPENDENCY_FAIL
    DESCRIPTION = 'The specified service depends on another service that has failed to start.'


class ServiceLogonFailedError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_LOGON_FAILED
    DESCRIPTION = 'The service did not start due to a logon failure.'


class ServiceMarkedForDeleteError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE
    DESCRIPTION = 'The RDeleteService method has been called for the service record identified by the hService parameter.'


class ServiceDependencyDeletedError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SERVICE_DEPENDENCY_DELETED
    DESCRIPTION = 'The specified service depends on a service that does not exist or has been marked for deletion.'


class ShutdownInProgressError(RStartServiceWError):
    RETURN_CODE = RStartServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS
    DESCRIPTION = 'The system is shutting down.'


RStartServiceWError.RETURN_CODE_TO_ERROR_CLASS.update({
    RStartServiceWReturnCode.ERROR_FILE_NOT_FOUND: SCMRFileNotFoundError,
    RStartServiceWReturnCode.ERROR_PATH_NOT_FOUND: PathNotFoundError,
    RStartServiceWReturnCode.ERROR_ACCESS_DENIED: AccessDeniedError,
    RStartServiceWReturnCode.ERROR_INVALID_HANDLE: InvalidHandleError,
    RStartServiceWReturnCode.ERROR_INVALID_PARAMETER: InvalidParameterError,
    RStartServiceWReturnCode.ERROR_SERVICE_REQUEST_TIMEOUT: ServiceRequestTimeoutError,
    RStartServiceWReturnCode.ERROR_SERVICE_NO_THREAD: ServiceNoThreadError,
    RStartServiceWReturnCode.ERROR_SERVICE_DATABASE_LOCKED: ServiceDatabaseLockedError,
    RStartServiceWReturnCode.ERROR_SERVICE_ALREADY_RUNNING: ServiceAlreadyRunningError,
    RStartServiceWReturnCode.ERROR_SERVICE_DISABLED: ServiceDisabledError,
    RStartServiceWReturnCode.ERROR_SERVICE_DEPENDENCY_FAIL: ServiceDependencyFailError,
    RStartServiceWReturnCode.ERROR_SERVICE_LOGON_FAILED: ServiceLogonFailedError,
    RStartServiceWReturnCode.ERROR_SERVICE_MARKED_FOR_DELETE: ServiceMarkedForDeleteError,
    RStartServiceWReturnCode.ERROR_SERVICE_DEPENDENCY_DELETED: ServiceDependencyDeletedError,
    RStartServiceWReturnCode.ERROR_SHUTDOWN_IN_PROGRESS: ShutdownInProgressError
})
