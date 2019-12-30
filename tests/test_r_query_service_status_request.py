from ms_scmr.operations.r_query_service_status import RQueryServiceStatusRequest


class TestRQueryServiceStatusResponse:
    REQUEST = RQueryServiceStatusRequest.from_bytes(
        data=bytes.fromhex('00000000c4a2e35f0231ea458930cd1abbf00a7f')
    )

    def test_service_handle(self, request: RQueryServiceStatusRequest = REQUEST):
        assert request.service_handle == bytes.fromhex('00000000c4a2e35f0231ea458930cd1abbf00a7f')

    def test_redeserialization(self):
        request = RQueryServiceStatusRequest.from_bytes(data=bytes(self.REQUEST))
        self.test_service_handle(request=request)
