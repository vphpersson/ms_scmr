from __future__ import annotations
from abc import ABC

from rpc.utils.client_protocol_message import ClientProtocolResponseError


class MSSCMRResponseError(ClientProtocolResponseError, ABC):
    pass
