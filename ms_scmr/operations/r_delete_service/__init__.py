from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type
from struct import pack as struct_pack, unpack as struct_unpack

from .exceptions import RDeleteServiceError, RDeleteServiceReturnCode
from ms_scmr.operations import Operation

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response


class RDeleteServiceRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_DELETE_SERVICE


class RDeleteServiceResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[RDeleteServiceError]] = RDeleteServiceError


@dataclass
class RDeleteServiceRequest(RDeleteServiceRequestBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RDeleteServiceRequest:
        return cls(service_handle=data[:20])

    def __bytes__(self) -> bytes:
        return self.service_handle


@dataclass
class RDeleteServiceResponse(RDeleteServiceResponseBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RDeleteServiceResponse:
        return cls(
            service_handle=data[:20],
            return_code=RDeleteServiceReturnCode(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.return_code.value)


RDeleteServiceResponseBase.REQUEST_CLASS = RDeleteServiceRequest
RDeleteServiceRequestBase.RESPONSE_CLASS = RDeleteServiceResponse


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