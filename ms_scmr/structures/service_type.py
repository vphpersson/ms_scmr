from enum import IntFlag

from msdsalgs.utils import make_mask_class


class ServiceType(IntFlag):
    SERVICE_KERNEL_DRIVER = 0x00000001
    SERVICE_FILE_SYSTEM_DRIVER = 0x00000002
    SERVICE_WIN32_OWN_PROCESS = 0x00000010
    SERVICE_WIN32_SHARE_PROCESS = 0x00000020
    SERVICE_INTERACTIVE_PROCESS = 0x00000100


ServiceTypeMask = make_mask_class(
    int_flag_enum_cls=ServiceType,
    name='ServiceTypeMask',
    prefix='SERVICE_'
)
