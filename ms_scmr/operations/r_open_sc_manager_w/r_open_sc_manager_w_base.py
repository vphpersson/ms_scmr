from typing import Final, Type
from abc import ABC

from ms_scmr.operations import Operation
from .exceptions import ROpenSCManagerWError

from rpc.utils.client_protocol_message import ClientProtocolRequest, ClientProtocolResponse


class ROpenSCManagerWMessage(ABC):
    pass


class ROpenSCManagerWRequestMessage(ClientProtocolRequest, ROpenSCManagerWMessage, ABC):
    OPERATION: Final[Operation] = Operation.R_OPEN_SC_MANAGER_W


class ROpenSCManagerWResponseMessage(ClientProtocolResponse, ROpenSCManagerWMessage, ABC):
    ERROR_CLASS: Final[Type[ROpenSCManagerWError]] = ROpenSCManagerWError
