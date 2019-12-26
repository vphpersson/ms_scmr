from __future__ import annotations
from dataclasses import dataclass
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.ndr import ConformantVaryingString

from ms_scmr.operations.r_open_service_w.r_open_service_w_base import ROpenServiceWRequestMessage, \
    ROpenServiceWResponseMessage
from ms_scmr.structures.service_access import ServiceAccessFlagMask


@dataclass
class ROpenServiceWRequest(ROpenServiceWRequestMessage):
    sc_manager_handle: bytes
    service_name: str
    desired_access: ServiceAccessFlagMask

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenServiceWRequest:

        sc_manager_handle = data[:20]
        offset = 20

        service_name = ConformantVaryingString.from_bytes(data=data[offset:])
        service_name_len: int = len(service_name)
        offset += service_name_len + ((4 - (service_name_len % 4)) % 4)

        desired_access = ServiceAccessFlagMask.from_mask(struct_unpack('<I', data[offset:offset+4])[0])

        return cls(
            sc_manager_handle=sc_manager_handle,
            service_name=service_name.representation,
            desired_access=desired_access
        )

    def __bytes__(self) -> bytes:

        service_name_bytes = bytes(ConformantVaryingString(representation=self.service_name))

        return b''.join([
            self.sc_manager_handle,
            service_name_bytes,
            ((4 - (len(service_name_bytes) % 4)) % 4) * b'\x00',
            struct_pack('<I', self.desired_access.to_mask())
        ])


ROpenServiceWResponseMessage.REQUEST_CLASS = ROpenServiceWRequest
