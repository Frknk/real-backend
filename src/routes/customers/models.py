from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel, field_validator

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dni : int = Field(index=True)
    name: str
    last_name: str
    email: str
    
    @field_validator("dni")
    @classmethod
    def dni_must_eight_digits(cls, v):
        dni_str = str(v)
        if len(dni_str) != 8:
            raise ValueError("DNI must be 8 digits")
        return v
    
class CustomerCreate(BaseModel):
    dni : int
    name: str
    last_name: str
    email: str
    
class CustomerRead(BaseModel):
    id: int
    dni : int
    name: str
    last_name: str
    email: str