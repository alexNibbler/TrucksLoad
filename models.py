from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import Integer, Boolean, ForeignKey

class BaseDB(DeclarativeBase):
    def __repr__(self):
        attributes = ', '.join(f"{key}={value!r}" for key, value in vars(self).items() if not key.startswith("_"))
        return f"<{self.__class__.__name__}({attributes})>"


class Truck(BaseDB):
    __tablename__ = "trucks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    length: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    available: Mapped[bool] = mapped_column(Boolean, default=True)


class Package(BaseDB):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    length: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    truck_id: Mapped[int | None] = mapped_column(ForeignKey("trucks.id"), nullable=True)
