from ms_scmr.structures.query_service_config_w import QueryServiceConfigW, ServiceType, StartType, ErrorControl


class TestQueryServiceConfigW:
    QUERY_SERVICE_CONFIG_W, _ = QueryServiceConfigW.from_bytes(
        data=bytes.fromhex('200000000400000001000000000002000400020000000000080002000c0002001000020033000000000000003300000043003a005c00570069006e0064006f00770073005c00730079007300740065006d00330032005c0073007600630068006f00730074002e0065007800650020002d006b0020006c006f00630061006c00530065007200760069006300650020002d0070000000000001000000000000000100000000000000070000000000000007000000520050004300530053002f00000000001a000000000000001a0000004e005400200041005500540048004f0052004900540059005c004c006f00630061006c0053006500720076006900630065000000100000000000000010000000520065006d006f00740065002000520065006700690073007400720079000000')
    )

    def test_service_type(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.service_type is ServiceType.SERVICE_WIN32_SHARE_PROCESS

    def test_start_type(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.start_type is StartType.SERVICE_DISABLED

    def test_error_control(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.error_control is ErrorControl.SERVICE_ERROR_NORMAL

    def test_binary_path_name(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.binary_path_name == r'C:\Windows\system32\svchost.exe -k localService -p'
        
    def test_load_order_group(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.load_order_group == ''
        
    def test_tag_id(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.tag_id == 0
        
    def test_dependencies(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.dependencies == ('RPCSS/',)
        
    def test_service_start_name(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.service_start_name == r'NT AUTHORITY\LocalService'
        
    def test_display_name(self, query_service_config_w: QueryServiceConfigW = QUERY_SERVICE_CONFIG_W):
        assert query_service_config_w.display_name == 'Remote Registry'
        
    def test_redeserialization(self):
        query_service_config_w, _ = QueryServiceConfigW.from_bytes(data=bytes(self.QUERY_SERVICE_CONFIG_W))
        self.test_service_type(query_service_config_w=query_service_config_w)
        self.test_start_type(query_service_config_w=query_service_config_w)
        self.test_error_control(query_service_config_w=query_service_config_w)
        self.test_binary_path_name(query_service_config_w=query_service_config_w)
        self.test_load_order_group(query_service_config_w=query_service_config_w)
        self.test_tag_id(query_service_config_w=query_service_config_w)
        self.test_dependencies(query_service_config_w=query_service_config_w)
        self.test_service_start_name(query_service_config_w=query_service_config_w)
        self.test_display_name(query_service_config_w=query_service_config_w)
