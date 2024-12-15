from src.database import get_session
from src.routes.products.models import Product, ProductCreate, ProductUpdate
from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session

def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    _product = Product.model_validate(product)
    session.add(_product)
    session.commit()
    session.refresh(_product)
    return _product

def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    session.delete(product)
    session.commit()
    return product

def update_product(product_id: int, product: ProductUpdate, session: Session = Depends(get_session)):
    _product = session.exec(select(Product).where(Product.id == product_id)).first()
    if _product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    _product.name = product.name
    _product.description = product.description
    _product.stock = product.stock
    _product.provider_id = product.provider_id
    _product.category_id = product.category_id
    _product.brand_id = product.brand_id
    session.add(_product)
    session.commit()
    session.refresh(_product)
    return _product