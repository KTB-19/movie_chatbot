from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ParseAI"
    DATABASE_URL: str = "mysql+aiomysql://root:qlalfqjsgh486@localhost:3306/moviedatabase"
    OPEN_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()