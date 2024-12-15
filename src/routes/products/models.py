from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import TYPE_CHECKING, Optional, List

import datetime

from src.routes.sales.link_models import ProductSale

if TYPE_CHECKING:
    from src.routes.categories.models import Category
    from src.routes.providers.models import Provider
    from src.routes.brands.models import Brand
    from src.routes.sales.models import Sale

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    stock: int = Field(default=0)
    price : float = Field(default=0)
    provider_id: int | None = Field(default=None, foreign_key="provider.id")
    provider: Optional["Provider"] = Relationship(back_populates="products")
    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="products")
    brand_id: int = Field(default=None, foreign_key="brand.id")
    brand: Optional["Brand"] = Relationship(back_populates="products")
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    sales : List["Sale"] = Relationship(back_populates="products", link_model=ProductSale)

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    stock: Optional[int]
    provider_id: Optional[int]
    category_id: Optional[int]
    brand_id: Optional[int]

class ProductCreate(BaseModel):
    name: str
    description: str
    stock: int
    provider_id: int
    category_id: int
    brand_id: int

class SimpleCategoryRead(BaseModel):
    id: int
    name: str
    description: str

class SimpleBrandRead(BaseModel):
    id: int
    name: str
    
class SimpleProviderRead(BaseModel):
    id: int
    ruc: int
    name: str
    address: str
    phone: str
    email: str

class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    stock: int
    category: Optional["SimpleCategoryRead"] = None
    brand: Optional["SimpleBrandRead"] = None
    provider: Optional["SimpleProviderRead"] = None
    

    
