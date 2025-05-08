from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class Base(BaseModel):
    model_config = ConfigDict(from_attributes = True)

class TruckCreate(Base):
    length: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class TruckResponse(Base):
    id: int
    length: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    available: bool


class PackageCreate(Base):
    length: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)


class PackageResponse(Base):
    id: int
    length: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    truck_id: Optional[int] = None


class AssignRequest(Base):
    package_ids: List[int]