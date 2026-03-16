from src.routes.customers.models import Customer, CustomerCreate, CustomerUpdate
from fastapi import Depends, HTTPException, status
from src.database import get_session
from sqlmodel import select


def get_customers(session=Depends(get_session)):
    customers = session.exec(select(Customer)).all()
    return customers


def get_customer(customer_id: int, session=Depends(get_session)):
    customer = session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


def get_customer_by_dni(dni: int, session=Depends(get_session)):
    customer = session.exec(select(Customer).where(Customer.dni == dni)).first()
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


def create_customer(customer: CustomerCreate, session=Depends(get_session)):
    _customer = Customer.model_validate(customer)
    session.add(_customer)
    session.commit()
    session.refresh(_customer)
    return _customer


def update_customer(
    customer_id: int, customer: CustomerUpdate, session=Depends(get_session)
):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    customer_data = customer.model_dump(exclude_unset=True)
    for key, value in customer_data.items():
        setattr(db_customer, key, value)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer


def delete_customer(customer_id: int, session=Depends(get_session)):
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer)
    session.commit()
    return customer
