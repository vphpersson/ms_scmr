from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from struct import unpack as struct_unpack, pack as struct_pack

from ms_scmr.structures.service_type import ServiceTypeMask


class CurrrentState(IntEnum):
    SERVICE_CONTINUE_PENDING = 0x00000005
    SERVICE_PAUSE_PENDING = 0x00000006
    SERVICE_PAUSED = 0x00000007
    SERVICE_RUNNING = 0x00000004
    SERVICE_START_PENDING = 0x00000002
    SERVICE_STOP_PENDING = 0x00000003
    SERVICE_STOPPED = 0x00000001


class ControlsAccepted(IntEnum):
    # "A value of zero indicates that no controls are accepted."
    NO_CONTROLS_ACCEPTED = 0x00000000
    SERVICE_ACCEPT_PARAMCHANGE = 0x00000008
    SERVICE_ACCEPT_PAUSE_CONTINUE = 0x00000002
    SERVICE_ACCEPT_SHUTDOWN = 0x00000004
    SERVICE_ACCEPT_STOP = 0x00000001
    SERVICE_ACCEPT_HARDWAREPROFILECHANGE = 0x00000020
    SERVICE_ACCEPT_POWEREVENT = 0x00000040
    SERVICE_ACCEPT_SESSIONCHANGE = 0x00000080
    SERVICE_ACCEPT_PRESHUTDOWN = 0x00000100
    SERVICE_ACCEPT_TIMECHANGE = 0x00000200
    SERVICE_ACCEPT_TRIGGEREVENT = 0x00000400


@dataclass
class ServiceStatus:
    # TODO: Not all values are permitted to be combined.
    service_type: ServiceTypeMask
    current_state: CurrrentState
    controls_accepted: ControlsAccepted
    # TODO: Use massive win32 error code enum
    #   https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes
    win_32_exit_code: int
    service_specific_exit_code: int
    check_point: int
    wait_hint: int

    @classmethod
    def from_bytes(cls, data: bytes) -> ServiceStatus:
        return cls(
            service_type=ServiceTypeMask.from_mask(struct_unpack('<I', data[:4])[0]),
            current_state=CurrrentState(struct_unpack('<I', data[4:8])[0]),
            controls_accepted=ControlsAccepted(struct_unpack('<I', data[8:12])[0]),
            win_32_exit_code=struct_unpack('<I', data[12:16])[0],
            service_specific_exit_code=struct_unpack('<I', data[16:20])[0],
            check_point=struct_unpack('<I', data[20:24])[0],
            wait_hint=struct_unpack('<I', data[24:28])[0]
        )

    def __bytes__(self) -> bytes:
        return b''.join([
            struct_pack('<I', self.service_type.to_mask()),
            struct_pack('<I', self.current_state.value),
            struct_pack('<I', self.controls_accepted.value),
            struct_pack('<I', self.win_32_exit_code),
            struct_pack('<I', self.service_specific_exit_code),
            struct_pack('<I', self.check_point),
            struct_pack('<I', self.wait_hint)
        ])
