from ms_scmr.operations.r_create_service_w import RCreateServiceWRequest, ServiceType, StartType, ErrorControl, ServiceAccessFlagMask
from ms_scmr.structures.service_access import ServiceAccessFlag


class TestRequestDeserialization:
    REQUEST = RCreateServiceWRequest.from_bytes(
        data=bytes.fromhex(
            '00000000a159a88204ddd347869c7d27737eb46805000000000000000500000057004800410054000000aaaa074700000a000000000000000a0000004900530047004f0049004e0047004f004e000000ff010f0010000000020000000000000011000000000000001100000043003a005c0077006800650065006c00650064005c0068006f007200730065000000bfbf00000000000000000000000000000000000000000000000000000000'
        )
    )

    def test_sc_manager_handle(self, request: RCreateServiceWRequest = REQUEST):
        assert request.scm_handle == bytes.fromhex('00000000a159a88204ddd347869c7d27737eb468')

    def test_service_name(self, request: RCreateServiceWRequest = REQUEST):
        assert request.service_name == 'WHAT'

    def test_display_name(self, request: RCreateServiceWRequest = REQUEST):
        assert request.display_name == 'ISGOINGON'

    def test_desired_access(self, request: RCreateServiceWRequest = REQUEST):
        assert request.desired_access.to_mask() == ServiceAccessFlagMask.from_mask(ServiceAccessFlag.SERVICE_ALL_ACCESS).to_mask()

    def test_service_type(self, request: RCreateServiceWRequest = REQUEST):
        assert request.service_type is ServiceType.SERVICE_WIN32_OWN_PROCESS

    def test_start_type(self, request: RCreateServiceWRequest = REQUEST):
        assert request.start_type is StartType.SERVICE_AUTO_START

    def test_error_control(self, request: RCreateServiceWRequest = REQUEST):
        assert request.error_control is ErrorControl.SERVICE_ERROR_IGNORE

    def test_binary_path_name(self, request: RCreateServiceWRequest = REQUEST):
        assert request.binary_path_name == r'C:\wheeled\horse'

    def test_load_order_group(self, request: RCreateServiceWRequest = REQUEST):
        assert request.load_order_group is None

    def test_tag_id(self, request: RCreateServiceWRequest = REQUEST):
        assert request.tag_id == 0

    def test_dependencies(self, request: RCreateServiceWRequest = REQUEST):
        assert request.dependencies == tuple()

    def test_service_start_name(self, request: RCreateServiceWRequest = REQUEST):
        assert request.service_start_name is None

    def test_password(self, request: RCreateServiceWRequest = REQUEST):
        assert request.password is None

    def test_redeserialization(self):
        request = RCreateServiceWRequest.from_bytes(data=bytes(self.REQUEST))
        self.test_sc_manager_handle(request=request)
        self.test_service_name(request=request)
        self.test_display_name(request=request)
        self.test_desired_access(request=request)
        self.test_service_type(request=request)
        self.test_start_type(request=request)
        self.test_error_control(request=request)
        self.test_binary_path_name(request=request)
        self.test_load_order_group(request=request)
        self.test_tag_id(request=request)
        self.test_dependencies(request=request)
        self.test_service_start_name(request=request)
        self.test_password(request=request)
