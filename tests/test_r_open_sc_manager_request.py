from ms_scmr.operations.r_open_sc_manager_w import ROpenSCManagerWRequest, DatabaseName, ServiceAccessFlagMask


class TestRequestDeserialization:
    REQUEST = ROpenSCManagerWRequest.from_bytes(
        data=bytes.fromhex(
            '7a6d0000060000000000000006000000440055004d004d005900000056e200000f000000000000000f000000530065007200760069006300650073004100630074006900760065000000bfbf3f000000'
        )
    )

    def test_machine_name(self, request: ROpenSCManagerWRequest = REQUEST):
        assert request.machine_name == 'DUMMY'

    def test_database_name(self, request: ROpenSCManagerWRequest = REQUEST):
        assert request.database_name is DatabaseName.SERVICES_ACTIVE

    def test_desired_access(self, request: ROpenSCManagerWRequest = REQUEST):
        expected_service_access_flag = ServiceAccessFlagMask(
            service_start=True,
            service_stop=True,
            service_change_config=True,
            service_query_config=True,
            service_query_status=True,
            service_enumerate_dependents=True
        )

        assert request.desired_access.to_mask() == expected_service_access_flag.to_mask()

    def test_redeserialization(self):
        request = ROpenSCManagerWRequest.from_bytes(data=bytes(self.REQUEST))
        assert self.test_machine_name(request=request) or True
        assert self.test_database_name(request=request) or True
        assert self.test_desired_access(request=request) or True
