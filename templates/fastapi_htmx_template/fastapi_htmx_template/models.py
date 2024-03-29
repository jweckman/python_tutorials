from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    birth_year: int
    join_date: datetime
