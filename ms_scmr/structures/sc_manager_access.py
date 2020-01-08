from enum import IntFlag

from msdsalgs.utils import make_mask_class


class SCManagerAccessFlag(IntFlag):
    SC_MANAGER_LOCK = 0x00000008
    SC_MANAGER_CREATE_SERVICE = 0x00000002
    SC_MANAGER_ENUMERATE_SERVICE = 0x00000004
    SC_MANAGER_CONNECT = 0x00000001
    SC_MANAGER_QUERY_LOCK_STATUS = 0x00000010
    SC_MANAGER_MODIFY_BOOT_CONFIG = 0x0020


SCManagerAccessFlagMask = make_mask_class(
    int_flag_enum_cls=SCManagerAccessFlag,
    prefix='SC_MANAGER_'
)
