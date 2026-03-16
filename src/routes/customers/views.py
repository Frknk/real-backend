from fastapi import APIRouter, Depends
from src.database import get_session
from sqlmodel import Session

from src.routes.customers.models import (
    Customer,
    CustomerRead,
    CustomerCreate,
    CustomerUpdate,
)
from src.routes.customers.operations import (
    get_customers,
    create_customer,
    get_customer_by_dni,
    update_customer,
    delete_customer,
)

router = APIRouter()


@router.get("", response_model=list[CustomerRead])
def read_customers(session: Session = Depends(get_session)):
    return get_customers(session)


@router.get("/{dni}", response_model=CustomerRead)
def read_customer(dni: int, session: Session = Depends(get_session)):
    return get_customer_by_dni(dni, session)


@router.post("", response_model=Customer)
def add_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
    return create_customer(customer, session)


@router.patch("/{customer_id}", response_model=Customer)
def update_customer_by_id(
    customer_id: int, customer: CustomerUpdate, session: Session = Depends(get_session)
):
    return update_customer(customer_id, customer, session)


@router.delete("/{customer_id}")
def remove_customer(customer_id: int, session: Session = Depends(get_session)):
    return delete_customer(customer_id, session)
