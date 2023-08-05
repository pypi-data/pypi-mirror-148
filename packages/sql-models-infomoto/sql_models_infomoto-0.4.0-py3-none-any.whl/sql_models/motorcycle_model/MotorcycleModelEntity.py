from sqlalchemy import Column, JSON, Integer, Identity, TEXT
from sqlmodel import Field

from sql_models.SQLCamelModel import SQLCamelModel

from sql_models.shared.visibility.RoleVisibility import RoleVisibility

from sql_models.motorcycle_model.MotorcycleModel import MotorcycleModel


class MotorcycleModelEntity(RoleVisibility, SQLCamelModel, table=True):
    __tablename__ = 'models'

    id: int = Field(
        primary_key=True,
        sa_column=Column(
            Integer,
            Identity(start=1, cycle=True),
            primary_key=True
        ),
    )

    manufacturer_id: int = Field(
        foreign_key='manufacturer.id',
    )

    technical_info: MotorcycleModel | None = Field(
        default=None,
        sa_column=Column(JSON),
    )

