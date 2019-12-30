from ms_scmr.operations.r_change_service_config_w import RChangeServiceConfigWResponse, RChangeServiceConfigWReturnCode


class TestResponseDeserialization:
    RESPONSE = RChangeServiceConfigWResponse.from_bytes(data=bytes.fromhex('0000000000000000'))

    def test_tag_id(self, response: RChangeServiceConfigWResponse = RESPONSE):
        assert response.tag_id == 0

    def test_return_code(self, response: RChangeServiceConfigWResponse = RESPONSE):
        assert response.return_code is RChangeServiceConfigWReturnCode.ERROR_SUCCESS
