from src.routes.brands.models import BrandRead, BrandCreate, Brand, BrandUpdate
from fastapi import Depends, APIRouter, HTTPException, status
from src.routes.brands.operations import get_brands, create_brand, get_brand_by_id, update_brand, delete_brand
from src.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("", response_model=list[BrandRead])
def read_brands(session: Session = Depends(get_session)):
    return get_brands(session)

@router.get("/{brand_id}", response_model=BrandRead)
def read_brand(brand_id: int, session: Session = Depends(get_session)):
    brand = get_brand_by_id(brand_id, session)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand

@router.post("", response_model=Brand)
def add_brand(brand: BrandCreate, session: Session = Depends(get_session)):
    return create_brand(brand, session)

@router.patch("/{brand_id}", response_model=Brand)
def update_brand_by_id(brand_id: int, brand: BrandUpdate, session: Session = Depends(get_session)):
    return update_brand(brand_id, brand, session)

@router.delete("/{brand_id}")
def remove_brand(brand_id: int, session: Session = Depends(get_session)):
    return delete_brand(brand_id, session)