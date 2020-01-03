from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type, AsyncContextManager
from struct import unpack as struct_unpack, pack as struct_pack
from contextlib import asynccontextmanager

from rpc.connection import Connection as RPCConnection
from rpc.ndr import ConformantVaryingString
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response

from .exceptions import ROpenServiceWError, ROpenServiceWReturnCode
from ms_scmr.operations import Operation
from ms_scmr.operations.r_close_service_handle import r_close_service_handle, RCloseServiceHandleRequest
from ms_scmr.structures.service_access import ServiceAccessFlagMask


class ROpenServiceWRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_OPEN_SERVICE_W


class ROpenServiceWResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[ROpenServiceWError]] = ROpenServiceWError


@dataclass
class ROpenServiceWRequest(ROpenServiceWRequestBase):
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

        desired_access = ServiceAccessFlagMask.from_mask(struct_unpack('<I', data[offset:offset+4])[0])

        return cls(
            sc_manager_handle=sc_manager_handle,
            service_name=service_name.representation,
            desired_access=desired_access
        )

    def __bytes__(self) -> bytes:

        service_name_bytes = bytes(ConformantVaryingString(representation=self.service_name))

        return b''.join([
            self.sc_manager_handle,
            service_name_bytes,
            ((4 - (len(service_name_bytes) % 4)) % 4) * b'\x00',
            struct_pack('<I', self.desired_access.to_mask())
        ])


@dataclass
class ROpenServiceWResponse(ROpenServiceWResponseBase):
    service_handle: bytes
    return_code: ROpenServiceWReturnCode

    @classmethod
    def from_bytes(cls, data: bytes) -> ROpenServiceWResponse:
        return cls(
            service_handle=data[:20],
            return_code=ROpenServiceWReturnCode(struct_unpack('<I', data[20:24])[0])
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
