from sqlmodel import SQLModel, Field

class ProductSale(SQLModel, table=True):
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    sale_id: int = Field(foreign_key="sale.id", primary_key=True)
    quantity: int = Field(default=1)
