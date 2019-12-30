from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type
from struct import unpack as struct_unpack, pack as struct_pack

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response

from .exceptions import RQueryServiceStatusError, RQueryServiceStatusReturnCode
from ms_scmr.operations import Operation
from ms_scmr.structures.service_status import ServiceStatus


class RQueryServiceStatusRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_QUERY_SERVICE_STATUS


class RQueryServiceStatusResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[RQueryServiceStatusError]] = RQueryServiceStatusError


@dataclass
class RQueryServiceStatusRequest(RQueryServiceStatusRequestBase):
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RQueryServiceStatusRequest:
        return cls(
            service_handle=data[:20]
        )

    def __bytes__(self) -> bytes:
        return self.service_handle


@dataclass
class RQueryServiceStatusResponse(RQueryServiceStatusResponseBase):
    service_status: ServiceStatus

    @classmethod
    def from_bytes(cls, data: bytes) -> RQueryServiceStatusResponse:
        return cls(
            service_status=ServiceStatus.from_bytes(data=data[:28]),
            return_code=RQueryServiceStatusReturnCode(struct_unpack('<I', data[28:32])[0])
        )

    def __bytes__(self) -> bytes:
        return bytes(self.service_status) + struct_pack('<I', self.return_code.value)


RQueryServiceStatusRequestBase.RESPONSE_CLASS = RQueryServiceStatusResponse
RQueryServiceStatusResponseBase.REQUEST_CLASS = RQueryServiceStatusRequest


async def r_query_service_status(
    rpc_connection: RPCConnection,
    request: RQueryServiceStatusRequest,
    raise_exception: bool = True
) -> RQueryServiceStatusResponse:
    """

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
