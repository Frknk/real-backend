from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.routes.products.models import Product


class Brand(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    products : List["Product"] = Relationship(back_populates="brand")


class SimpleProductRead(BaseModel):
    id: int
    name: str
    description: str


class BrandCreate(BaseModel):
    name: str


class BrandRead(BaseModel):
    id: int
    name: str
    products: List["SimpleProductRead"] = []
    
class BrandUpdate(BaseModel):
    name: str
