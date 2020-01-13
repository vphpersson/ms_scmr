from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Optional
from struct import unpack as struct_unpack, pack as struct_pack, error as struct_error

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response
from msdsalgs.win32_error import Win32ErrorCode, ErrorInsufficientBufferError

from ms_scmr.operations import Operation
from ms_scmr.structures.query_service_config_w import QueryServiceConfigW


@dataclass
class RQueryServiceConfigWRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_QUERY_SERVICE_CONFIG_W

    service_handle: bytes
    buf_size: int = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> RQueryServiceConfigWRequest:
        return cls(
            service_handle=data[:20],
            buf_size=struct_unpack('<I', data[20:24])[0]
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.buf_size)


@dataclass
class RQueryServiceConfigWResponse(ClientProtocolResponseBase):
    service_config: Optional[QueryServiceConfigW]
    bytes_needed: int

    @classmethod
    def from_bytes(cls, data: bytes) -> RQueryServiceConfigWResponse:
        try:
            service_config, offset = QueryServiceConfigW.from_bytes(data=data)
        # TODO: I should figure out a nicer way to deal with cases as these.
        except struct_error:
            service_config = None
            offset = QueryServiceConfigW.STRUCTURE_SIZE

        return cls(
            service_config=service_config,
            bytes_needed=struct_unpack('<I', data[offset:offset+4])[0],
            return_code=Win32ErrorCode(struct_unpack('<I', data[offset+4:offset+8])[0])
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            bytes(self.service_config),
            struct_pack('<I', self.bytes_needed),
            struct_pack('<I', self.return_code.value)
        ])


RQueryServiceConfigWRequest.RESPONSE_CLASS = RQueryServiceConfigWResponse
RQueryServiceConfigWResponse.REQUEST_CLASS = RQueryServiceConfigWRequest


async def r_query_service_config_w(
    rpc_connection: RPCConnection,
    request: RQueryServiceConfigWRequest,
    raise_exception: bool = True,
    retry_buf_size: bool = True
) -> RQueryServiceConfigWResponse:
    """

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :param retry_buf_size:
    :return:
    """

    try:
        return await obtain_response(
            rpc_connection=rpc_connection,
            request=request,
            raise_exception=raise_exception
        )
    except ErrorInsufficientBufferError as e:
        if retry_buf_size:
            request.buf_size = e.response.bytes_needed
            return await r_query_service_config_w(
                rpc_connection=rpc_connection,
                request=request,
                raise_exception=raise_exception,
                retry_buf_size=False
            )
        raise e
