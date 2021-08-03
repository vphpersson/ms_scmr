from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, AsyncContextManager
from struct import unpack as struct_unpack, pack as struct_pack
from contextlib import asynccontextmanager

from rpc.connection import Connection as RPCConnection
from ndr.structures.conformant_varying_string import ConformantVaryingString
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode
from rpc.utils.ndr import pad as ndr_pad

from ms_scmr.operations import Operation
from ms_scmr.operations.r_close_service_handle import r_close_service_handle, RCloseServiceHandleRequest
from ms_scmr.structures.service_access import ServiceAccessFlagMask


@dataclass
class ROpenServiceWRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_OPEN_SERVICE_W

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

        desired_access = ServiceAccessFlagMask.from_int(struct_unpack('<I', data[offset:offset+4])[0])

        return cls(
            sc_manager_handle=sc_manager_handle,
            service_name=service_name.representation,
            desired_access=desired_access
        )

    def __bytes__(self) -> bytes:

        service_name_bytes = bytes(ConformantVaryingString(representation=self.service_name))

        return b''.join([
            self.sc_manager_handle,
            ndr_pad(service_name_bytes),
            struct_pack('<I', int(self.desired_access))
        ])


@dataclass
class ROpenServiceWResponse(ClientProtocolResponseBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenServiceWResponse:
        return cls(
            service_handle=data[:20],
            return_code=Win32ErrorCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.return_code.value)


ROpenServiceWResponse.REQUEST_CLASS = ROpenServiceWRequest
ROpenServiceWRequest.RESPONSE_CLASS = ROpenServiceWResponse


@asynccontextmanager
async def r_open_service_w(
    rpc_connection: RPCConnection,
    request: ROpenServiceWRequest,
    raise_exception: bool = True
) -> AsyncContextManager[ROpenServiceWResponse]:
    """
    Perform the ROpenServiceW operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    r_open_service_w_response: ROpenServiceWResponse = await obtain_response(
        rpc_connection=rpc_connection,
        request=request,
        raise_exception=raise_exception
    )

    yield r_open_service_w_response

    await r_close_service_handle(
        rpc_connection=rpc_connection,
        request=RCloseServiceHandleRequest(
            service_handle=r_open_service_w_response.service_handle
        )
    )
