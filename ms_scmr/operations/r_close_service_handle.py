from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode

from ms_scmr.operations import Operation


@dataclass
class RCloseServiceHandleRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_CLOSE_SERVICE_HANDLE
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RCloseServiceHandleRequest:
        return cls(service_handle=data[:20])

    def __bytes__(self) -> bytes:
        return self.service_handle


@dataclass
class RCloseServiceHandleResponse(ClientProtocolResponseBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RCloseServiceHandleResponse:
        return cls(
            service_handle=data[:20],
            return_code=Win32ErrorCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.return_code.value)


RCloseServiceHandleResponse.REQUEST_CLASS = RCloseServiceHandleRequest
RCloseServiceHandleRequest.RESPONSE_CLASS = RCloseServiceHandleResponse


async def r_close_service_handle(
    rpc_connection: RPCConnection,
    request: RCloseServiceHandleRequest,
    raise_exception: bool = True
) -> RCloseServiceHandleResponse:
    """
    Perform the RCloseServiceHandle operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
