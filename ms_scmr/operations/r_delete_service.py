from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode

from ms_scmr.operations import Operation


@dataclass
class RDeleteServiceRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_DELETE_SERVICE

    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RDeleteServiceRequest:
        return cls(service_handle=data[:20])

    def __bytes__(self) -> bytes:
        return self.service_handle


@dataclass
class RDeleteServiceResponse(ClientProtocolResponseBase):

    @classmethod
    def from_bytes(cls, data: bytes) -> RDeleteServiceResponse:
        return cls(
            return_code=Win32ErrorCode(struct_unpack('<I', data[:4])[0])
        )

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.return_code.value)


RDeleteServiceResponse.REQUEST_CLASS = RDeleteServiceRequest
RDeleteServiceRequest.RESPONSE_CLASS = RDeleteServiceResponse


async def r_delete_service(
    rpc_connection: RPCConnection,
    request: RDeleteServiceRequest,
    raise_exception: bool = True
) -> RDeleteServiceResponse:
    """
    Perform the RDeleteService operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
