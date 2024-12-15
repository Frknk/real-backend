from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.routes.sales.models import SaleCreate, SaleRead
from src.routes.sales.operations import create_sale, read_sale
from src.database import get_session

router = APIRouter()

@router.post("/")
def create_sale_route(sale: SaleCreate, session: Session = Depends(get_session)):
    return create_sale(sale, session)

@router.get("/{sale_id}", response_model=SaleRead)
def read_sale_route(sale_id: int, session: Session = Depends(get_session)):
    return read_sale(sale_id, session)
