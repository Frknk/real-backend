from src.routes.brands.models import Brand, BrandCreate, BrandUpdate
from fastapi import Depends
from src.database import get_session
from sqlmodel import Session, select

def create_brand(new_brand: BrandCreate, session: Session = Depends(get_session)):
    brand = Brand.model_validate(new_brand)
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand

def get_brands(session: Session = Depends(get_session)):
    brands = session.exec(select(Brand)).all()
    return brands

def get_brand_by_id(brand_id: int, session: Session = Depends(get_session)):
    brand = session.get(Brand, brand_id)
    return brand

def update_brand(brand_id: int, brand: BrandUpdate, session: Session = Depends(get_session)):
    db_brand = session.get(Brand, brand_id)
    db_brand.name = brand.name
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand

def delete_brand(brand_id: int, session: Session = Depends(get_session)):
    brand = session.get(Brand, brand_id)
    session.delete(brand)
    session.commit()
    return brand