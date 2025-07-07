from src.routes.brands.models import Brand, BrandCreate, BrandUpdate
from fastapi import Depends, HTTPException, status
from src.database import get_session
from sqlmodel import Session, select


def create_brand(new_brand: BrandCreate, session: Session = Depends(get_session)):
    if new_brand.name is None or new_brand.name.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Brand name cannot be empty",
        )
    existing_brand = session.exec(
        select(Brand).where(Brand.name == new_brand.name)
    ).first()
    if existing_brand:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Brand already exists"
        )
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


def get_brand_by_name(brand_name: str, session: Session = Depends(get_session)):
    brand = session.exec(select(Brand).where(Brand.name == brand_name)).first()
    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )
    return brand


def update_brand(
    brand_id: int, brand: BrandUpdate, session: Session = Depends(get_session)
):
    db_brand = session.get(Brand, brand_id)
    db_brand.name = brand.name
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


def update_brand_by_name(
    brand_name: str, brand: BrandUpdate, session: Session = Depends(get_session)
):
    db_brand = session.exec(select(Brand).where(Brand.name == brand_name)).first()
    if db_brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )
    db_brand.name = brand.name
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


def delete_brand_by_name(brand_name: str, session: Session = Depends(get_session)):
    brand = session.exec(select(Brand).where(Brand.name == brand_name)).first()
    if brand is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found"
        )
    session.delete(brand)
    session.commit()
    return brand


def delete_brand(brand_id: int, session: Session = Depends(get_session)):
    brand = session.get(Brand, brand_id)
    session.delete(brand)
    session.commit()
    return brand
