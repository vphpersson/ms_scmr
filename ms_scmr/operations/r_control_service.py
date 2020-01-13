from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode

from ms_scmr.operations import Operation
from ms_scmr.structures.service_control import ServiceControl
from ms_scmr.structures.service_status import ServiceStatus


@dataclass
class RControlServiceRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_CONTROL_SERVICE

    service_handle: bytes
    request_control_code: ServiceControl

    @classmethod
    def from_bytes(cls, data: bytes) -> RControlServiceRequest:
        return cls(
            service_handle=data[:20],
            request_control_code=ServiceControl(struct_unpack('<I', data[20:24])[0])
        )

    def __bytes__(self) -> bytes:
        return self.service_handle + struct_pack('<I', self.request_control_code.value)


@dataclass
class RControlServiceResponse(ClientProtocolResponseBase):
    service_status: ServiceStatus

    @classmethod
    def from_bytes(cls, data: bytes) -> RControlServiceResponse:
        return cls(
            service_status=ServiceStatus.from_bytes(data=data[:28]),
            return_code=Win32ErrorCode(struct_unpack('<I', data[28:32])[0])
        )

    def __bytes__(self) -> bytes:
        return bytes(self.service_status) + struct_pack('<I', self.return_code.value)


RControlServiceResponse.REQUEST_CLASS = RControlServiceRequest
RControlServiceRequest.RESPONSE_CLASS = RControlServiceResponse


async def r_control_service(
    rpc_connection: RPCConnection,
    request: RControlServiceRequest,
    raise_exception: bool = True
) -> RControlServiceResponse:
    """
    Perform the RControlService operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)