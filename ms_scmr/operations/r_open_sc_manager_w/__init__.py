from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import obtain_response

from .r_open_sc_manager_w_request import *
from .r_open_sc_manager_w_response import *


async def r_open_sc_manager_w(
    rpc_connection: RPCConnection,
    request: ROpenSCManagerWRequest,
    raise_exception: bool = True
) -> ROpenSCManagerWResponse:
    """
    Perform the ROpenSCManagerW operation.

    :param rpc_connection: An RPC connection with which to perform the operation.
    :param request: The operation request.
    :param raise_exception: Whether to raise an exception in case the return code indicates an error has occurred.
    :return: A corresponding response to the request
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
