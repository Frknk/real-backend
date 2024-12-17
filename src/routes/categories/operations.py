from src.routes.categories.models import CategoryCreate, Category
from fastapi import Depends, HTTPException, status
from src.database import get_session
from sqlmodel import select

def get_categories(session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories

def get_category(category_id: int, session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

def get_category_by_name(category_name: str, session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.name == category_name)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

def create_category(category: CategoryCreate, session = Depends(get_session)):
    _category = Category.model_validate(category)
    session.add(_category)
    session.commit()
    session.refresh(_category)
    return _category

def update_category_by_name(category_name: str, category: CategoryCreate, session = Depends(get_session)):
    _category = session.exec(select(Category).where(Category.name == category_name)).first()
    if _category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    _category.name = category.name
    session.add(_category)
    session.commit()
    session.refresh(_category)
    return _category

def update_category(category_id: int, category: CategoryCreate, session = Depends(get_session)):
    _category = session.exec(select(Category).where(Category.id == category_id)).first()
    if _category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    _category.name = category.name
    session.add(_category)
    session.commit()
    session.refresh(_category)
    return _category

def delete_category_by_name(category_name: str, session = Depends(get_session)):
    category = session.exec(select(Category).where(Category.name == category_name)).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    session.delete(category)
    session.commit()
    return category

def delete_category(category_id: int, session = Depends(get_session)):
    category = session.get(Category, category_id)
    session.delete(category)
    session.commit()
    return category