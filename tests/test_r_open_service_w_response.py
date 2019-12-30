from ms_scmr.operations.r_open_service_w import ROpenServiceWResponse, ROpenServiceWReturnCode


class TestResponseDeserialization:
    RESPONSE = ROpenServiceWResponse.from_bytes(
        data=bytes.fromhex(
            '0000000007d4db68e435494aa633267065a4afc000000000'
        )
    )

    def test_service_handle(self, response: ROpenServiceWResponse = RESPONSE):
        assert response.service_handle == bytes.fromhex('0000000007d4db68e435494aa633267065a4afc0')

    def test_return_code(self, response: ROpenServiceWResponse = RESPONSE):
        assert response.return_code is ROpenServiceWReturnCode.ERROR_SUCCESS

    def test_redeserialization(self):
        response = ROpenServiceWResponse.from_bytes(data=bytes(self.RESPONSE))
        self.test_service_handle(response=response)
        self.test_return_code(response=response)
