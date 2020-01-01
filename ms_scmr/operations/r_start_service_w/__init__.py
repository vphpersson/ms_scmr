from __future__ import annotations
from dataclasses import dataclass
from abc import ABC
from typing import Final, Type, Tuple, List
from struct import pack as struct_pack, unpack as struct_unpack

from rpc.connection import Connection as RPCConnection
from rpc.ndr import ConformantVaryingString, Pointer, NullPointer
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response
from rpc.utils.ndr import calculate_pad_length, pad as ndr_pad

from .exceptions import RStartServiceWError, RStartServiceWReturnCode
from ms_scmr.operations import Operation


class RStartServiceWRequestBase(ClientProtocolRequestBase, ABC):
    OPERATION: Final[Operation] = Operation.R_START_SERVICE_W


class RStartServiceWResponseBase(ClientProtocolResponseBase, ABC):
    ERROR_CLASS: Final[Type[RStartServiceWError]] = RStartServiceWError


@dataclass
class RStartServiceWRequest(RStartServiceWRequestBase):
    service_handle: bytes
    argv: Tuple[str, ...]

    @property
    def argc(self) -> int:
        return len(self.argv)

    @classmethod
    def from_bytes(cls, data: bytes) -> RStartServiceWRequest:

        argc = struct_unpack('<I', data[20:24])
        argv_ndr_representation = Pointer.from_bytes(data=data[24:]).representation

        num_argv: int = struct_unpack('<I', argv_ndr_representation[:4])[0]
        offset = 4 + num_argv * Pointer.structure_size

        argv_list: List[str] = []
        for _ in range(num_argv):
            argv_ndr_string = ConformantVaryingString.from_bytes(data=argv_ndr_representation[offset:])
            argv_list.append(argv_ndr_string.representation)
            offset += calculate_pad_length(
                length_unpadded=len(argv_ndr_string),
                multiple=4
            )

        return cls(
            service_handle=data[:20],
            argv=tuple(argv_list)
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            self.service_handle,
            struct_pack('<I', self.argc),
            bytes(
                Pointer(
                    representation=b''.join([
                        struct_pack('<I', len(self.argv)),
                        b''.join(
                            struct_pack('<I', Pointer(representation=b'').referent_id)
                            for _ in self.argv
                        ),
                        b''.join(
                            ndr_pad(data=bytes(ConformantVaryingString(representation=argument_string)))
                            for argument_string in self.argv
                        )
                    ])
                )
                if self.argv else NullPointer()
            )
        ])


@dataclass
class RStartServiceWResponse(RStartServiceWResponseBase):

    @classmethod
    def from_bytes(cls, data: bytes) -> RStartServiceWResponse:
        return cls(return_code=RStartServiceWReturnCode(struct_unpack('<I', data[:4])[0]))

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.return_code)


RStartServiceWResponseBase.REQUEST_CLASS = RStartServiceWRequest
RStartServiceWRequestBase.RESPONSE_CLASS = RStartServiceWResponse


async def r_start_service_w(
    rpc_connection: RPCConnection,
    request: RStartServiceWRequest,
    raise_exception: bool = True
) -> RStartServiceWResponse:
    """
    Perform the RStartServiceW operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)