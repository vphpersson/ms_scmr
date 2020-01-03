from ms_scmr.operations.r_open_sc_manager_w import ROpenSCManagerWResponse, ROpenSCManagerWReturnCode


class TestResponseDeserialization:
    RESPONSE = ROpenSCManagerWResponse.from_bytes(
        data=bytes.fromhex(
            '000000001bbd651ba6076942866436f4a486985f00000000'
        )
    )

    def test_sc_handle(self, response: ROpenSCManagerWResponse = RESPONSE):
        assert response.scm_handle == bytes.fromhex('000000001bbd651ba6076942866436f4a486985f')

    def test_return_code(self, response: ROpenSCManagerWResponse = RESPONSE):
        assert response.return_code is ROpenSCManagerWReturnCode.ERROR_SUCCESS

    def test_redeserialization(self):
        response = ROpenSCManagerWResponse.from_bytes(data=bytes(self.RESPONSE))
        self.test_sc_handle(response=response)
        self.test_return_code(response=response)
