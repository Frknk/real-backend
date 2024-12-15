import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

from src.routes.sales.link_models import ProductSale


if TYPE_CHECKING:
    from src.routes.products.models import Product


class CustomerRead(BaseModel):
    dni: int
    name: str
    last_name: str
    email: str

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total: float
    products: List["Product"] = Relationship(back_populates="sales", link_model=ProductSale)
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    customer_dni : int = Field(foreign_key="customer.dni")


class ProductSaleInput(BaseModel):
    product_id: int
    quantity: int = 1


class SaleCreate(BaseModel):
    products: List[ProductSaleInput]
    customer_dni: int


class ProductSaleRead(BaseModel):
    name: str
    price: float
    quantity: int | None = None


class SaleRead(SQLModel):
    id: int
    products: List[ProductSaleRead] = []
    total: float
    created_at: datetime.datetime
    customer: Optional[CustomerRead] = None
