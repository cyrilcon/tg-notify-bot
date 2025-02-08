from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"


class ApiTags(BaseModel):
    notification: str = "Notification"


class ApiConfig(BaseModel):
    prefix: str = "/api"
    access_token: str = "access_token"

    run: RunConfig = RunConfig()
    v1: ApiV1Prefix = ApiV1Prefix()
    tags: ApiTags = ApiTags()


class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str
    database: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    def construct_url(self, driver="asyncpg", host=None, port=5432) -> str:
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class TgBotConfig(BaseModel):
    token: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    api: ApiConfig = ApiConfig()
    db: Optional[DatabaseConfig] = None
    tg_bot: Optional[TgBotConfig] = None


config = Config()
