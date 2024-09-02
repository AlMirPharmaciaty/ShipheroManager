from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings
    """
    ENV: str = "dev"
    TITLE: str
    DB_URL: str
    SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_TOKEN_DURATION: int = 30
    GITHUB_TOKEN: str
    SHIPHERO_URL: str
    SHIPHERO_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_url(self):
        """
        Retrieve database access URL
        """
        if self.ENV == "dev":
            return "sqlite:///./dev.db"
        return self.DB_URL
