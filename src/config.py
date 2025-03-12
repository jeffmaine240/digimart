from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):
    APP_NAME: str
    DESCRIPTION: str
    VERSION: str

    # Database settings 
    DB_TYPE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_URL: str

    #google settings
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CONF_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


config = Config()