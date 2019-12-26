from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from struct import unpack as struct_unpack, pack as struct_pack

from ms_scmr.operations.r_open_sc_manager_w.r_open_sc_manager_w_base import ROpenSCManagerWRequestMessage, \
    ROpenSCManagerWResponseMessage


class ROpenSCManagerWReturnCode(IntEnum):
    ERROR_SUCCESS = 0
    ERROR_ACCESS_DENIED = 5
    ERROR_INVALID_NAME = 123
    ERROR_DATABASE_DOES_NOT_EXIST = 1065
    ERROR_SHUTDOWN_IN_PROGRESS = 1115


@dataclass
class ROpenSCManagerWResponse(ROpenSCManagerWResponseMessage):
    sc_handle: bytes
    # TODO: This could be part of some base response class, because is probably present in all responses.
    return_code: ROpenSCManagerWReturnCode

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenSCManagerWResponse:
        return cls(
            sc_handle=data[:20],
            return_code=ROpenSCManagerWReturnCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.sc_handle + struct_pack('<I', self.return_code.value)


ROpenSCManagerWRequestMessage.RESPONSE_CLASS = ROpenSCManagerWResponse
