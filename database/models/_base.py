import re

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=config.db.naming_convention)


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
