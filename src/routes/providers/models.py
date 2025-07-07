from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.routes.products.models import Product


class Provider(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    ruc: int
    name: str = Field(index=True, unique=True)
    address: str
    phone: str
    email: str
    products: List["Product"] = Relationship(back_populates="provider")


class SimpleProductRead(BaseModel):
    id: int
    name: str
    description: str


class ProviderCreate(BaseModel):
    ruc: int
    name: str
    address: str
    phone: str
    email: str


class ProviderRead(BaseModel):
    id: int
    ruc: int
    name: str
    address: str
    phone: str
    email: str
    products: List["SimpleProductRead"] = []


class ProviderUpdate(BaseModel):
    ruc: int
    name: str
    address: str
    phone: str
    email: str
