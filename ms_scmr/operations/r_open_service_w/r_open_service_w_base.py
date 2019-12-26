from typing import Final, Type
from abc import ABC

from ms_scmr.operations import Operation
from .exceptions import ROpenServiceWError

from rpc.utils.client_protocol_message import ClientProtocolRequest, ClientProtocolResponse


class ROpenServiceWMessage(ABC):
    pass


class ROpenServiceWRequestMessage(ClientProtocolRequest, ROpenServiceWMessage, ABC):
    OPERATION: Final[Operation] = Operation.R_OPEN_SERVICE_W


class ROpenServiceWResponseMessage(ClientProtocolResponse, ROpenServiceWMessage, ABC):
    ERROR_CLASS: Final[Type[ROpenServiceWError]] = ROpenServiceWError
