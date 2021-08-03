from ms_scmr.operations.r_change_service_config_w import RChangeServiceConfigWRequest, StartType

# TODO: There are to many "zero-valued" attributes in these test.


class TestRequestDeserialization:
    REQUEST = RChangeServiceConfigWRequest.from_bytes(
        data=bytes.fromhex(
            '0000000084d194e37984074f87217e6adfa2a170ffffffff04000000ffffffffd2b9000009000000000000000900000043003a005c0068006f007200730065000000aaaa741200000400000000000000040000004800410048000000000000000000000000000000fd4d000004000000000000000400000044004f0047000000cfa400000e00000070006c0065006100730065000000bfbf0e000000e64f0000030000000000000003000000550055000000'
        )
    )

    def test_service_handle(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.service_handle == b'\x00\x00\x00\x00\x84\xd1\x94\xe3y\x84\x07O\x87!~j\xdf\xa2\xa1p'

    def test_service_type(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.service_type is None

    def test_start_type(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.start_type is StartType.SERVICE_DISABLED

    def test_error_control(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.error_control is None

    def test_binary_path_name(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.binary_path_name == r'C:\horse'

    def test_load_order_group(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.load_order_group == 'HAH'

    def test_tag_id(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.tag_id == 0

    def test_dependencies(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.dependencies == ()

    def test_service_start_name(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.service_start_name == 'DOG'

    def test_password(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.password == 'please'

    def test_display_name(self, request: RChangeServiceConfigWRequest = REQUEST):
        assert request.display_name == 'UU'

    def test_redeserialization(self):
        request = RChangeServiceConfigWRequest.from_bytes(data=bytes(self.REQUEST))
        self.test_service_handle(request=request)
        self.test_service_type(request=request)
        self.test_start_type(request=request)
        self.test_error_control(request=request)
        self.test_binary_path_name(request=request)
        self.test_load_order_group(request=request)
        self.test_tag_id(request=request)
        self.test_dependencies(request=request)
        self.test_service_start_name(request=request)
        self.test_password(request=request)
        self.test_display_name(request=request)
