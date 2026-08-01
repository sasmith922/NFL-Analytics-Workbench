from app.core.settings import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.environment == "development"
    assert settings.backend_port == 8000
