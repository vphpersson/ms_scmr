from enum import IntFlag
from itertools import chain

from msdsalgs.security_types.access_mask import AccessMask
from msdsalgs.utils import make_mask_class


class ServiceAccessFlag(IntFlag):
    SERVICE_ALL_ACCESS = 0x000F01FF
    SERVICE_CHANGE_CONFIG = 0x00000002
    SERVICE_ENUMERATE_DEPENDENTS = 0x00000008
    SERVICE_INTERROGATE = 0x00000080
    SERVICE_PAUSE_CONTINUE = 0x00000040
    SERVICE_QUERY_CONFIG = 0x00000001
    SERVICE_QUERY_STATUS = 0x00000004
    SERVICE_START = 0x00000010
    SERVICE_STOP = 0x00000020
    SERVICE_USER_DEFINED_CONTROL = 0x00000100
    SERVICE_SET_STATUS = 0x00008000


ServiceAccessFlagMask = make_mask_class(
    int_flag_enum_cls=IntFlag(
        'ServiceAccessFlag',
        ((enum_entry.name, enum_entry.value) for enum_entry in chain(AccessMask, ServiceAccessFlag))
    ),
    name='ServiceAccessFlagMask'
)
