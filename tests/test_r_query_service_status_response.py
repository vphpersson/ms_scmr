from ms_scmr.operations.r_query_service_status import RQueryServiceStatusResponse, RQueryServiceStatusReturnCode
from ms_scmr.structures.service_status import ServiceStatus, ServiceTypeMask, CurrrentState, ControlsAccepted


class TestResponseDeserialization:
    RESPONSE = RQueryServiceStatusResponse.from_bytes(
        data=bytes.fromhex(
            '2000000001000000000000003504000000000000000000000000000000000000'
        )
    )

    def test_service_status(self, response: RQueryServiceStatusResponse = RESPONSE):

        expected_service_status = ServiceStatus(
            service_type=ServiceTypeMask(win32_share_process=True),
            current_state=CurrrentState.SERVICE_STOPPED,
            controls_accepted=ControlsAccepted.NO_CONTROLS_ACCEPTED,
            win_32_exit_code=1077,
            service_specific_exit_code=0,
            check_point=0,
            wait_hint=0
        )

        assert response.service_status == expected_service_status

    def test_return_code(self, response: RQueryServiceStatusResponse = RESPONSE):
        assert response.return_code is RQueryServiceStatusReturnCode.ERROR_SUCCESS

    def test_redeserialization(self):
        response = RQueryServiceStatusResponse.from_bytes(data=bytes(self.RESPONSE))
        self.test_service_status(response=response)
        self.test_return_code(response=response)
