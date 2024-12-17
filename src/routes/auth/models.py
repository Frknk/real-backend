from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str
    hashed_password: str
    role: str = Field(default="user")
    
class UserLogin(SQLModel):
    username: str
    password: str