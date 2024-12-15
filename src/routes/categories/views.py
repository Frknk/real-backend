from src.routes.categories.models import CategoryRead, CategoryUpdate
from src.routes.categories.operations import get_categories, create_category, get_category, update_category, delete_category
from fastapi import APIRouter, Depends
from src.database import get_session
from sqlmodel import Session

router = APIRouter()

@router.get("", response_model=list[CategoryRead])
def read_categories(session: Session = Depends(get_session)):
    return get_categories(session)

@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, session: Session = Depends(get_session)):
    return get_category(category_id, session)

@router.post("", response_model=CategoryUpdate)
def add_category(category: CategoryUpdate, session: Session = Depends(get_session)):
    return create_category(category, session)

@router.patch("/{category_id}", response_model=CategoryUpdate)
def update_category_by_id(category_id: int, category: CategoryUpdate, session: Session = Depends(get_session)):
    return update_category(category_id, category, session)

@router.delete("/{category_id}")
def remove_category(category_id: int, session: Session = Depends(get_session)):
    return delete_category(category_id, session)
    
