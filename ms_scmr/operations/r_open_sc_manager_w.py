from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from enum import Enum
from struct import pack as struct_pack, unpack as struct_unpack
from contextlib import asynccontextmanager

from rpc.connection import Connection as RPCConnection
from ndr.structures.conformant_varying_string import ConformantVaryingString
from ndr.structures.pointer import Pointer
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode
from ndr.utils import pad as ndr_pad

from ms_scmr.operations import Operation
from ms_scmr.operations.r_close_service_handle import r_close_service_handle, RCloseServiceHandleRequest
from ms_scmr.structures.sc_manager_access import SCManagerAccessFlagMask


class DatabaseName(Enum):
    SERVICES_ACTIVE = 'ServicesActive'
    SERVICES_FAILED = 'ServicesFailed'


@dataclass
class ROpenSCManagerWRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_OPEN_SC_MANAGER_W

    desired_access: SCManagerAccessFlagMask = SCManagerAccessFlagMask(connect=True)
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
            desired_access=SCManagerAccessFlagMask.from_int(struct_unpack('<I', data[offset:offset + 4])[0]),
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
            ndr_pad(machine_name_bytes),
            ndr_pad(database_name_bytes),
            struct_pack('<I', int(self.desired_access))
        ])


@dataclass
class ROpenSCManagerWResponse(ClientProtocolResponseBase):
    scm_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenSCManagerWResponse:
        return cls(
            scm_handle=data[:20],
            return_code=Win32ErrorCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.scm_handle + struct_pack('<I', self.return_code.value)


ROpenSCManagerWResponse.REQUEST_CLASS = ROpenSCManagerWRequest
ROpenSCManagerWRequest.RESPONSE_CLASS = ROpenSCManagerWResponse


@asynccontextmanager
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
    :return: A response corresponding to the request.
    """

    r_open_sc_manager_w_response: ROpenSCManagerWResponse = await obtain_response(
        rpc_connection=rpc_connection,
        request=request,
        raise_exception=raise_exception
    )

    yield r_open_sc_manager_w_response

    await r_close_service_handle(
        rpc_connection=rpc_connection,
        request=RCloseServiceHandleRequest(
            service_handle=r_open_sc_manager_w_response.scm_handle
        )
    )
