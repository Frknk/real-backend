from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.routes.products.models import Product


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    products: List["Product"] = Relationship(back_populates="category")


class ProductCategoryRead(BaseModel):
    id: int
    name: str
    description: str


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryRead(BaseModel):
    id: int
    name: str
    description: str
    products: list["ProductCategoryRead"] = []


class SimpleCategoryRead(BaseModel):
    id: int
    name: str
    description: str

class CategoryUpdate(BaseModel):
    name: str
    description: str