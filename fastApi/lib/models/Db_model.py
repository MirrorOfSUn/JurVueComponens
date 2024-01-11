from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from util import date2int


# ---- User
class UserBase(SQLModel):
    FirstName: str
    LastName:   str
    MiddleName: Optional[str] = ''
    FullName: str = Field(index=True)
    Phone1: Optional[str] = ''
    Phone2: Optional[str] = ''
    Email1: Optional[str] = ''
    Email2: Optional[str] = ''
    Address: Optional[str] = ''
    is_active: bool = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.FullName:
            self.FullName = self.FirstName
            self.FullName += " "+self.MiddleName if self.MiddleName else ""
            self.FullName += " "+self.LastName


class User(UserBase, table=True):
    __tablename__ = 'users'
    id: Optional[int] = Field(default=None, primary_key=True)
    orders: List["Order"] = Relationship(back_populates="user")


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserEdit(UserBase):
    pass


class UserList(SQLModel):
    """
    Server based list
    """
    datatable: List[User] = []
    total_records: int
    total_filtered_records: int
    total_pages: int
    current_page: int
    page_size: int


class UserListRequest(SQLModel):
    """
    Client search request for UserList
    """
    search: Optional[str]
    name: Optional[str]
    phone: Optional[str] = ''
    email: Optional[str] = ''
    address: Optional[str] = ''
    is_active: Optional[bool] = True
    page: int = 1
    page_size: int = 15


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    # metadata = metadata
    id: Optional[int] = Field(default=None, primary_key=True)
    date: int
    count: float
    description: str = ""
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    item_id: Optional[int] = Field(default=None, foreign_key="items.id")
    user: Optional[User] = Relationship(back_populates="orders")  # orders - имя в таблице User
    item: Optional["Item"] = Relationship(back_populates="orders")  # orders - имя в таблице Item
    # item: Optional["Item"] = Relationship(back_populates="items")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.date:
            self.date = date2int()


class Item(SQLModel, table=True):
    __tablename__ = "items"
    # metadata = metadata
    id: Optional[int] = Field(default=None, primary_key=True)
    date: int
    name: str
    unit: str
    is_active: bool = True
    description: Optional[str] = ""
    orders: List["Order"] = Relationship(back_populates="item")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.date:
            self.date = date2int()


# engine = create_engine(
#     DB_LOCATION,
#     connect_args={"check_same_thread": False},
#     echo=True
# )


