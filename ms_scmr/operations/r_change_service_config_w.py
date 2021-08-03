from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, ClassVar
from struct import unpack as struct_unpack, pack as struct_pack

from rpc.connection import Connection as RPCConnection
from ndr.structures.pointer import Pointer, NullPointer
from ndr.structures.conformant_varying_string import ConformantVaryingString
from ndr.structures.unidimensional_conformant_array import UnidimensionalConformantArray
from rpc.utils.client_protocol_message import ClientProtocolRequestBase, ClientProtocolResponseBase, obtain_response, Win32ErrorCode
from rpc.utils.ndr import calculate_pad_length, pad as ndr_pad

from ms_scmr.operations import Operation
from ms_scmr.structures.service_type import ServiceType
from ms_scmr.structures.start_type import StartType
from ms_scmr.structures.error_control import ErrorControl

# TODO: Move?
SERVICE_NO_CHANGE = 0xFFFFFFFF


@dataclass
class RChangeServiceConfigWRequest(ClientProtocolRequestBase):
    OPERATION: ClassVar[Operation] = Operation.R_CHANGE_SERVICE_CONFIG_W
    STRUCTURE_SIZE: ClassVar[int] = 32

    service_handle: bytes
    service_type: Optional[ServiceType] = None
    start_type: Optional[StartType] = None
    error_control: Optional[ErrorControl] = None
    binary_path_name: Optional[str] = None
    load_order_group: Optional[str] = None
    tag_id: int = 0
    dependencies: Tuple[str, ...] = tuple()
    service_start_name: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_bytes(cls, data: bytes) -> RChangeServiceConfigWRequest:

        offset = cls.STRUCTURE_SIZE
        attribute_name_class_pair = (
            ('binary_path_name', ConformantVaryingString),
            ('load_order_group', ConformantVaryingString),
            ('dependencies', UnidimensionalConformantArray),
            ('service_start_name', ConformantVaryingString),
            ('password', UnidimensionalConformantArray),
            ('display_name', ConformantVaryingString)
        )
        kwargs = {}
        for attribute_name, attribute_class in attribute_name_class_pair:
            # Skip attributes in between variable ones.
            if attribute_name in {'dependencies', 'service_start_name', 'display_name'}:
                offset += 4

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
            elif attribute_name == 'password':
                kwargs[attribute_name] = b''.join(attribute_ndr.representation).decode(encoding='utf-16-le').rstrip('\x00')
            else:
                kwargs[attribute_name] = attribute_ndr.representation if attribute_ndr is not None else None

            offset += calculate_pad_length(length_unpadded=attribute_pointer.structure_size+attribute_len, multiple=4)

        service_type_int_val: int = struct_unpack('<I', data[20:24])[0]
        start_type_int_val: int = struct_unpack('<I', data[24:28])[0]
        error_control_int_val: int = struct_unpack('<I', data[28:32])[0]

        return cls(
            service_handle=data[:20],
            service_type=ServiceType(service_type_int_val) if service_type_int_val != SERVICE_NO_CHANGE else None,
            start_type=StartType(start_type_int_val) if start_type_int_val != SERVICE_NO_CHANGE else None,
            error_control=ErrorControl(error_control_int_val) if error_control_int_val != SERVICE_NO_CHANGE else None,
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
            self.service_handle,
            struct_pack('<I', self.service_type.value if self.service_type is not None else SERVICE_NO_CHANGE),
            struct_pack('<I', self.start_type.value if self.start_type is not None else SERVICE_NO_CHANGE),
            struct_pack('<I', self.error_control.value if self.error_control is not None else SERVICE_NO_CHANGE),
            ndr_pad(
                data=bytes(
                    Pointer(representation=ConformantVaryingString(representation=self.binary_path_name))
                    if self.binary_path_name is not None else NullPointer()
                )
            ),
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
                (0 if isinstance(dependencies_ndr, NullPointer) else len(dependencies_ndr.representation) - UnidimensionalConformantArray.STRUCTURE_SIZE)
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
                (0 if isinstance(password_ndr, NullPointer) else len(password_ndr.representation) - UnidimensionalConformantArray.STRUCTURE_SIZE)
            ),
            bytes(
                Pointer(representation=ConformantVaryingString(representation=self.display_name))
                if self.display_name is not None else NullPointer()
            )
        ])


@dataclass
class RChangeServiceConfigWResponse(ClientProtocolResponseBase):
    tag_id: int = 0

    @classmethod
    def from_bytes(cls, data: bytes) -> RChangeServiceConfigWResponse:
        return cls(
            tag_id=struct_unpack('<I', data[:4])[0],
            return_code=Win32ErrorCode(struct_unpack('<I', data[4:8])[0])
        )

    def __bytes__(self) -> bytes:
        return struct_pack('<I', self.tag_id) + struct_pack('<I', self.return_code.value)


RChangeServiceConfigWRequest.RESPONSE_CLASS = RChangeServiceConfigWResponse
RChangeServiceConfigWResponse.REQUEST_CLASS = RChangeServiceConfigWRequest


async def r_change_service_config_w(
    rpc_connection: RPCConnection,
    request: RChangeServiceConfigWRequest,
    raise_exception: bool = True
) -> RChangeServiceConfigWResponse:
    """

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
