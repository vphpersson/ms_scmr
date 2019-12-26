from rpc.connection import Connection as RPCConnection
from rpc.utils.client_protocol_message import obtain_response


from .r_open_service_w_request import *
from .r_open_service_w_response import *


async def r_open_service_w(
    rpc_connection: RPCConnection,
    request: ROpenServiceWRequest,
    raise_exception: bool = True
) -> ROpenServiceWResponse:
    """
    Perform the ROpenServiceW operation.

    :param rpc_connection:
    :param request:
    :param raise_exception:
    :return:
    """

    return await obtain_response(rpc_connection=rpc_connection, request=request, raise_exception=raise_exception)
