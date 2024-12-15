from src.routes.products.models import Product, ProductRead, ProductCreate
from src.routes.products.operations import get_products, create_product, get_product, delete_product, update_product
from fastapi import APIRouter, Depends
from src.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("", response_model=list[ProductRead])
def read_products(session: Session = Depends(get_session)):
    return get_products(session)

@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, session: Session = Depends(get_session)):
    return get_product(product_id, session)

@router.post("", response_model=Product)
def add_product(product: ProductCreate, session: Session = Depends(get_session)):
    return create_product(product, session)

@router.patch("/{product_id}", response_model=Product)
def modify_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session)):
    return update_product(product_id, product, session)

@router.delete("/{product_id}")
def remove_product(product_id: int, session: Session = Depends(get_session)):
    return delete_product(product_id, session)

