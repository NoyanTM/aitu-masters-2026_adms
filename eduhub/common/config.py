import os
import dataclasses
from typing import Self

from sqlalchemy import URL


@dataclasses.dataclass
class Config:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @classmethod
    def load_from_env(cls) -> Self:
        """Load configuration from environment variables"""
        config_fields = [field.name for field in dataclasses.fields(Config)]
        fields = {}
        for key in os.environ.keys():
            if key in config_fields:
                # @TODO: set value to found key, otherwise by default or empty for not found fields
                # @TODO: gather all keys beforehand to reduce calls 
                # @TODO: raises warning or exception if not found not optional/necessary fields
                fields[key] = os.environ.get(key)
        return cls(**fields)

    def postgres_url(self) -> str:
        url = URL.create(
            drivername="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )
        return url.render_as_string(hide_password=False)
