from pydantic_settings import BaseSettings, SettingsConfigDict
from groq import Groq
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    DATABASE_URL:str
    SECRETE_KEY:str
    ALGORITHAM:str
    EXP_TIME:int
    GROQ_API_KEY: str
settings = Settings()

groq_client = Groq(
    api_key=settings.GROQ_API_KEY
)


GROQ_MODEL = "openai/gpt-oss-120b"
# print(settings.DATABASE_URL)