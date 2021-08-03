from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, AsyncContextManager, ClassVar
from struct import pack as struct_pack, unpack as struct_unpack
from contextlib import asynccontextmanager

from rpc.connection import Connection as RPCConnection
from ndr.structures.pointer import Pointer, NullPointer
from ndr.structures.unidimensional_conformant_array import UnidimensionalConformantArray
from ndr.structures.conformant_varying_string import ConformantVaryingString
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, \
    Win32ErrorCode
from rpc.utils.ndr import pad as ndr_pad, calculate_pad_length

from ms_scmr.operations import Operation
from ms_scmr.operations.r_close_service_handle import r_close_service_handle, RCloseServiceHandleRequest
from ms_scmr.structures.service_type import ServiceType
from ms_scmr.structures.error_control import ErrorControl
from ms_scmr.structures.start_type import StartType
from ms_scmr.structures.service_access import ServiceAccessFlagMask


@dataclass
class RCreateServiceWRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_CREATE_SERVICE_W

    scm_handle: bytes
    service_name: str
    display_name: str
    desired_access: ServiceAccessFlagMask
    service_type: ServiceType
    start_type: StartType
    error_control: ErrorControl
    binary_path_name: str
    load_order_group: Optional[str] = None
    tag_id: int = 0
    dependencies: Tuple[str, ...] = ()
    # TODO: Where are these stored?
    service_start_name: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> RCreateServiceWRequest:

        attribute_name_class_pair = (
            ('service_name', ConformantVaryingString),
            ('display_name', ConformantVaryingString),
            ('desired_access', ServiceAccessFlagMask.from_int),
            ('service_type', ServiceType),
            ('start_type', StartType),
            ('error_control', ErrorControl),
            ('binary_path_name', ConformantVaryingString),
            ('load_order_group', ConformantVaryingString),
            ('tag_id', None),
            ('dependencies', UnidimensionalConformantArray),
            ('_depen_size', None),
            ('service_start_name', ConformantVaryingString),
            ('password', UnidimensionalConformantArray),
            ('_pw_size', None)
        )
        kwargs = {}
        offset = 20
        for attribute_name, attribute_class in attribute_name_class_pair:
            if attribute_name in {'_depen_size', '_pw_size'}:
                offset += 4
                continue
            if attribute_name in {'service_name', 'binary_path_name'}:
                ndr_string = attribute_class.from_bytes(data=data[offset:])
                kwargs[attribute_name] = ndr_string.representation
                offset += calculate_pad_length(length_unpadded=len(ndr_string))
            elif attribute_name in {'service_type', 'start_type', 'error_control', 'desired_access'}:
                kwargs[attribute_name] = attribute_class(struct_unpack('<I', data[offset:offset+4])[0])
                offset += 4
            elif attribute_name == 'tag_id':
                kwargs[attribute_name] = struct_unpack('<I', data[offset:offset+4])[0]
                offset += 4
            else:
                attribute_pointer = Pointer.from_bytes(data=data[offset:])
                attribute_ndr = (
                    attribute_class.from_bytes(data=attribute_pointer.representation)
                    if not isinstance(attribute_pointer, NullPointer) else None
                )
                attribute_len = len(attribute_ndr) if attribute_ndr is not None else 0

                if attribute_name == 'dependencies':
                    kwargs[attribute_name] = tuple(
                        b''.join(attribute_ndr.representation).decode(encoding='utf-16-le').split('\x00')
                    ) if attribute_ndr else tuple()
                elif attribute_name == 'password' and attribute_ndr is not None:
                    kwargs[attribute_name] = b''.join(attribute_ndr.representation).decode(encoding='utf-16-le').rstrip(
                        '\x00')
                else:
                    kwargs[attribute_name] = attribute_ndr.representation if attribute_ndr is not None else None

                offset += calculate_pad_length(length_unpadded=attribute_pointer.structure_size+attribute_len)

        return cls(
            scm_handle=data[:20],
            **kwargs
        )

    def __bytes__(self) -> bytes:
        dependencies_ndr = Pointer(
            representation=UnidimensionalConformantArray(
                representation=tuple(
                    bytes([byte])
                    for byte in '\x00'.join(self.dependencies).encode(encoding='utf-16-le')
                )
            )
        ) if len(self.dependencies) != 0 else NullPointer()

        password_ndr = Pointer(
            representation=UnidimensionalConformantArray(
                representation=tuple(
                    bytes([byte])
                    for byte in (self.password + '\x00').encode(encoding='utf-16-le')
                )
            )
        ) if self.password is not None else NullPointer()

        return b''.join([
            self.scm_handle,
            ndr_pad(data=bytes(ConformantVaryingString(representation=self.service_name))),
            ndr_pad(data=bytes(Pointer(representation=ConformantVaryingString(representation=self.display_name)))),
            struct_pack('<I', int(self.desired_access)),
            struct_pack('<I', self.service_type.value),
            struct_pack('<I', self.start_type.value),
            struct_pack('<I', self.error_control.value),
            ndr_pad(data=bytes(ConformantVaryingString(representation=self.binary_path_name))),
            ndr_pad(
                data=bytes(
                    Pointer(representation=ConformantVaryingString(representation=self.load_order_group))
                    if self.load_order_group is not None else NullPointer()
                )
            ),
            struct_pack('<I', self.tag_id),
            ndr_pad(data=bytes(dependencies_ndr)),
            struct_pack(
                '<I',
                (0 if isinstance(dependencies_ndr, NullPointer) else len(
                    dependencies_ndr.representation) - UnidimensionalConformantArray.STRUCTURE_SIZE)
            ),
            ndr_pad(
                data=bytes(
                    Pointer(representation=ConformantVaryingString(representation=self.service_start_name))
                    if self.service_start_name is not None else NullPointer()
                )
            ),
            ndr_pad(data=bytes(password_ndr)),
            struct_pack(
                '<I',
                (0 if isinstance(password_ndr, NullPointer) else len(
                    password_ndr.representation) - UnidimensionalConformantArray.STRUCTURE_SIZE)
            )
        ])


@dataclass
class RCreateServiceWResponse(ClientProtocolResponseBase):
    tag_id: int
    service_handle: bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> RCreateServiceWResponse:
        return cls(
            tag_id=struct_unpack('<I', data[:4])[0],
            service_handle=data[4:24],
            return_code=Win32ErrorCode(struct_unpack('<I', data[24:28])[0])
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            struct_pack('<I', self.tag_id),
            self.service_handle,
            struct_pack('<I', self.return_code.value)
        ])


RCreateServiceWResponse.REQUEST_CLASS = RCreateServiceWRequest
RCreateServiceWRequest.RESPONSE_CLASS = RCreateServiceWResponse


@asynccontextmanager
async def r_create_service_w(
    rpc_connection: RPCConnection,
    request: RCreateServiceWRequest,
    raise_exception: bool = True
) -> AsyncContextManager[RCreateServiceWResponse]:
    """
    Perform the RCreateServiceW operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    r_create_service_w_response: RCreateServiceWResponse = await obtain_response(
        rpc_connection=rpc_connection,
        request=request,
        raise_exception=raise_exception
    )

    yield r_create_service_w_response

    await r_close_service_handle(
        rpc_connection=rpc_connection,
        request=RCloseServiceHandleRequest(
            service_handle=r_create_service_w_response.service_handle
        )
    )
