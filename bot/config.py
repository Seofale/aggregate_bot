from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    mongo_host: SecretStr
    mongo_port: int
    mongo_db: SecretStr
    mongo_db_col: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
