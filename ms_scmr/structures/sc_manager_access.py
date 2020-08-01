from enum import IntFlag

from msdsalgs.utils import Mask


class SCManagerAccessFlag(IntFlag):
    SC_MANAGER_LOCK = 0x00000008
    SC_MANAGER_CREATE_SERVICE = 0x00000002
    SC_MANAGER_ENUMERATE_SERVICE = 0x00000004
    SC_MANAGER_CONNECT = 0x00000001
    SC_MANAGER_QUERY_LOCK_STATUS = 0x00000010
    SC_MANAGER_MODIFY_BOOT_CONFIG = 0x0020
    DELETE = 0x00010000
    READ_CONTROL = 0x00020000
    WRITE_DAC = 0x00040000
    WRITE_OWNER = 0x00080000


SCManagerAccessFlagMask = Mask.make_class(
    int_flag_class=SCManagerAccessFlag,
    prefix='SC_MANAGER_'
)
