from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DATABASE_URL:str
    SECRETE_KEY:str
    ALGORITHAM:str
    EXP_TIME:int
settings = Settings()

# print(settings.DATABASE_URL)