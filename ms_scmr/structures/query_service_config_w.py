from __future__ import annotations
from dataclasses import dataclass
from typing import Union, ClassVar
from struct import pack as struct_pack, unpack as struct_unpack

from ndr.structures.pointer import Pointer
from ndr.structures.conformant_varying_string import ConformantVaryingString

from ms_scmr.structures.service_type import ServiceType
from ms_scmr.structures.start_type import StartType
from ms_scmr.structures.error_control import ErrorControl


@dataclass
class QueryServiceConfigW:
    STRUCTURE_SIZE: ClassVar[int] = 36

    service_type: ServiceType
    start_type: StartType
    error_control: ErrorControl
    binary_path_name: str
    load_order_group: str
    tag_id: int
    dependencies: tuple[str, ...]
    service_start_name: str
    display_name: str

    @classmethod
    def from_bytes(cls, data: bytes) -> tuple[QueryServiceConfigW, int]:

        string_names = ('binary_path_name', 'load_order_group', 'dependencies', 'service_start_name', 'display_name')
        kwargs: dict[str, Union[str, dict[str, ...]]] = {}
        offset_variable = cls.STRUCTURE_SIZE
        for string_name in string_names:
            ndr_string = ConformantVaryingString.from_bytes(data=data[offset_variable:])
            kwargs[string_name] = (
                tuple(ndr_string.representation.split('\x00')) if string_name == 'dependencies'
                else ndr_string.representation
            )
            ndr_string_len = len(ndr_string)
            offset_variable += ndr_string_len + ((4 - (ndr_string_len % 4)) % 4)

        return (
            cls(
                service_type=ServiceType.from_bytes(bytes=data[:4], byteorder='little'),
                start_type=StartType.from_bytes(bytes=data[4:8], byteorder='little'),
                error_control=ErrorControl.from_bytes(bytes=data[8:12], byteorder='little'),
                tag_id=struct_unpack('<I', data[20:24])[0],
                **kwargs
            ),
            offset_variable
        )

    def __bytes__(self) -> bytes:
        variable_chunk = b''

        binary_path_name_ndr = ConformantVaryingString(representation=self.binary_path_name)
        load_order_group_ndr = ConformantVaryingString(representation=self.load_order_group)
        dependencies_ndr = ConformantVaryingString(representation='\x00'.join(self.dependencies))
        service_start_name_ndr = ConformantVaryingString(representation=self.service_start_name)
        display_name_ndr = ConformantVaryingString(representation=self.display_name)

        ndr_strings = (
            binary_path_name_ndr, load_order_group_ndr, dependencies_ndr, service_start_name_ndr, display_name_ndr
        )

        for ndr_string in ndr_strings:
            variable_chunk += bytes(ndr_string)
            variable_chunk += ((4 - (len(variable_chunk) % 4)) % 4) * b'\x00'

        return b''.join([
            struct_pack('<I', self.service_type.value),
            struct_pack('<I', self.start_type.value),
            struct_pack('<I', self.error_control.value),
            struct_pack('<I', Pointer(representation=b'').referent_id),
            struct_pack('<I', Pointer(representation=b'').referent_id),
            struct_pack('<I', self.tag_id),
            struct_pack('<I', Pointer(representation=b'').referent_id),
            struct_pack('<I', Pointer(representation=b'').referent_id),
            struct_pack('<I', Pointer(representation=b'').referent_id),
            variable_chunk
        ])

