from ms_scmr.operations.r_open_service_w import ROpenServiceWRequest, ServiceAccessFlagMask


class TestRequestDeserialization:
    REQUEST = ROpenServiceWRequest.from_bytes(
        data=bytes.fromhex(
            '000000001bbd651ba6076942866436f4a486985f0f000000000000000f000000520065006d006f0074006500520065006700690073007400720079000000000004000000'
        )
    )

    def test_sc_manager_handle(self, request: ROpenServiceWRequest = REQUEST):
        assert request.sc_manager_handle == bytes.fromhex('000000001bbd651ba6076942866436f4a486985f')

    def test_service_name(self, request: ROpenServiceWRequest = REQUEST):
        assert request.service_name == 'RemoteRegistry'

    def test_desired_access(self, request: ROpenServiceWRequest = REQUEST):
        assert request.desired_access == ServiceAccessFlagMask(service_query_status=True)

    def test_redeserialization(self):
        request = ROpenServiceWRequest.from_bytes(data=bytes(self.REQUEST))
        self.test_sc_manager_handle(request=request)
        self.test_service_name(request=request)
        self.test_desired_access(request=request)
