from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type, ClassVar
from enum import Enum
from struct import pack as struct_pack, unpack as struct_unpack

from .exceptions import ROpenSCManagerWError, ROpenSCManagerWReturnCode
from ms_scmr.operations import Operation
from ms_scmr.structures.service_access import ServiceAccessFlagMask

from rpc.connection import Connection as RPCConnection
from rpc.ndr import ConformantVaryingString, Pointer
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response


class ROpenSCManagerWRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_OPEN_SC_MANAGER_W


class ROpenSCManagerWResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[ROpenSCManagerWError]] = ROpenSCManagerWError


class DatabaseName(Enum):
    SERVICES_ACTIVE = 'ServicesActive'
    SERVICES_FAILED = 'ServicesFailed'


@dataclass
class ROpenSCManagerWRequest(ROpenSCManagerWRequestBase):
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


@dataclass
class ROpenSCManagerWResponse(ROpenSCManagerWResponseBase):
    sc_handle: bytes
    return_code: ROpenSCManagerWReturnCode

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenSCManagerWResponse:
        return cls(
            sc_handle=data[:20],
            return_code=ROpenSCManagerWReturnCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.sc_handle + struct_pack('<I', self.return_code.value)


ROpenSCManagerWResponse.REQUEST_CLASS = ROpenSCManagerWRequest
ROpenSCManagerWRequest.RESPONSE_CLASS = ROpenSCManagerWResponse


async def r_open_sc_manager_w(
    rpc_connection: RPCConnection,
    request: ROpenSCManagerWRequest,
    raise_exception: bool = True
) -> ROpenSCManagerWResponse:
    """
    Perform the ROpenSCManagerW operation.

    :param rpc_connection: An RPC connection with which to perform the operation.
    :param request: The operation request.
    :param raise_exception: Whether to raise an exception in case the return code indicates an error has occurred.
    :return: A corresponding response to the request
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
