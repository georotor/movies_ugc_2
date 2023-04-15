from settings import Settings


class TestSettings(Settings):
    service_url: str = 'http://localhost:8000'


test_settings = TestSettings()
