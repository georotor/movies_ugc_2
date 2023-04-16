from settings import Settings


class TestSettings(Settings):
    service_url: str = 'http://api:8000'
    request_id = False


test_settings = TestSettings()
