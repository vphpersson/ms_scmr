from ms_scmr.operations.r_start_service_w import RStartServiceWRequest


class TestRequestDeserialization:
    REQUEST = RStartServiceWRequest.from_bytes(
        data=bytes.fromhex(
            '00000000'
            'bbf164bb'
            '282fa049'
            '99d74b1f'
            '8884a96f'
            '03000000'
            '0ee80000'
            '03000000'
            '879a0000'
            '3b1b0000'
            '37680000'
            '06000000'
            '00000000'
            '06000000'
            '68006500'
            '6c006c00'
            '6f000000'
            '06000000'
            '00000000'
            '06000000'
            '74006800'
            '65007200'
            '65000000'
            '04000000'
            '00000000'
            '04000000'
            '62006f00'
            '62000000'
        )
    )

    def test_service_handle(self, request: RStartServiceWRequest = REQUEST):
        assert request.service_handle == bytes.fromhex('00000000bbf164bb282fa04999d74b1f8884a96f')

    def test_argv(self, request: RStartServiceWRequest = REQUEST):
        assert request.argv == ('hello', 'there', 'bob')

    def test_redeserialization(self):
        request = RStartServiceWRequest.from_bytes(data=bytes(self.REQUEST))
        self.test_service_handle(request=request)
        self.test_argv(request=request)
