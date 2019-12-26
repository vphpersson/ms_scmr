from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from struct import pack as struct_pack, unpack as struct_unpack

from ms_scmr.operations.r_open_sc_manager_w.r_open_sc_manager_w_base import ROpenSCManagerWRequestMessage, \
    ROpenSCManagerWResponseMessage
from ms_scmr.structures.service_access import ServiceAccessFlagMask

from rpc.ndr import Pointer, ConformantVaryingString


class DatabaseName(Enum):
    SERVICES_ACTIVE = 'ServicesActive'
    SERVICES_FAILED = 'ServicesFailed'


@dataclass
class ROpenSCManagerWRequest(ROpenSCManagerWRequestMessage):
    desired_access: ServiceAccessFlagMask = ServiceAccessFlagMask()
    # It appears that the machine name can be set to any string.
    machine_name: str = ''
    database_name: DatabaseName = DatabaseName.SERVICES_ACTIVE

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenSCManagerWRequest:
        machine_name = ConformantVaryingString.from_bytes(data=Pointer.from_bytes(data=data).representation)
        machine_name_len: int = len(machine_name)
        offset = Pointer.structure_size + machine_name_len + ((4 - (machine_name_len % 4)) % 4)

        database_name = ConformantVaryingString.from_bytes(data=Pointer.from_bytes(data=data[offset:]).representation)
        database_name_len: int = len(database_name)
        offset += Pointer.structure_size + database_name_len + ((4 - (database_name_len % 4)) % 4)

        return cls(
            machine_name=machine_name.representation,
            desired_access=ServiceAccessFlagMask.from_mask(struct_unpack('<I', data[offset:offset + 4])[0]),
            database_name=DatabaseName(database_name.representation) if database_name else None
        )

    def __bytes__(self) -> bytes:

        machine_name_bytes = bytes(
            Pointer(representation=ConformantVaryingString(representation=self.machine_name or ''))
        )

        database_name_bytes = bytes(
            Pointer(
                representation=ConformantVaryingString(
                    representation=self.database_name.value if self.database_name else ''
                )
            )
        )

        return b''.join([
            machine_name_bytes,
            ((4 - (len(machine_name_bytes) % 4)) % 4) * b'\x00',
            database_name_bytes,
            ((4 - (len(database_name_bytes) % 4)) % 4) * b'\x00',
            struct_pack('<I', self.desired_access.to_mask().value)
        ])


ROpenSCManagerWResponseMessage.REQUEST_CLASS = ROpenSCManagerWRequest
