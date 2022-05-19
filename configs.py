from pydantic import BaseSettings


class Configs(BaseSettings):
    redis_host: str
    postgres_host: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


configs = Configs()
