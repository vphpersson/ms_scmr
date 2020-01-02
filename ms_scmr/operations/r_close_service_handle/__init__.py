from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type
from struct import pack as struct_pack, unpack as struct_unpack

from .exceptions import RCloseServiceHandleError, RCloseServiceHandleReturnCode
from ms_scmr.operations import Operation

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response


class RCloseServiceHandleRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_CLOSE_SERVICE_HANDLE


class RCloseServiceHandleResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[RCloseServiceHandleError]] = RCloseServiceHandleError


@dataclass
class RCloseServiceHandleRequest(RCloseServiceHandleRequestBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RCloseServiceHandleRequest:
        return cls(service_handle=data[:20])

    def __bytes__(self) -> bytes:
        return self.service_handle


@dataclass
class RCloseServiceHandleResponse(RCloseServiceHandleResponseBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RCloseServiceHandleResponse:
        return cls(
            service_handle=data[:20],
            return_code=RCloseServiceHandleReturnCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.return_code.value)


RCloseServiceHandleResponseBase.REQUEST_CLASS = RCloseServiceHandleRequest
RCloseServiceHandleRequestBase.RESPONSE_CLASS = RCloseServiceHandleResponse


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