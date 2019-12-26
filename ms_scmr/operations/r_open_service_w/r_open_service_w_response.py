from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from struct import unpack as struct_unpack, pack as struct_pack

from ms_scmr.operations.r_open_service_w.r_open_service_w_base import ROpenServiceWRequestMessage, \
    ROpenServiceWResponseMessage


class ROpenServiceWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_HANDLE = 6
    ERROR_INVALID_NAME = 123
    ERROR_SERVICE_DOES_NOT_EXIST = 1060
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


@dataclass
class ROpenServiceWResponse(ROpenServiceWResponseMessage):
    service_handle: bytes
    return_code: ROpenServiceWReturnCode

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenServiceWResponse:
        return cls(
            service_handle=data[:20],
            return_code=ROpenServiceWReturnCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.return_code.value)


ROpenServiceWRequestMessage.RESPONSE_CLASS = ROpenServiceWResponseMessage
