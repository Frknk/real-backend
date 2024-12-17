from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.routes.products.models import Product


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    products: List["Product"] = Relationship(back_populates="category")


class ProductCategoryRead(BaseModel):
    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryRead(BaseModel):
    id: int
    name: str
    products: list["ProductCategoryRead"] = []


class SimpleCategoryRead(BaseModel):
    id: int
    name: str

class CategoryUpdate(BaseModel):
    name: str