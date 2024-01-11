from sqlmodel import Session, select, col, create_engine
from Db_model import User, Item, Order

from config import DB_LOCATION

engine = create_engine(
    DB_LOCATION,
    connect_args={"check_same_thread": False},
    echo=True
)

# Add user
# user1 = User(FirstName="FN3", LastName="LN3", Phone1="12345")
# user2 = User(FirstName="FN4", LastName="LN4", Phone1="67890")
#
# with Session(engine) as db:
#     db.add(user1)
#     db.add(user2)
#     db.commit()

# Add Items
# item1 = Item(name="Item 1", unit="bottle", description="bottle of weather")
# item2 = Item(name="Item 2", unit="box", description="box of wine")
#
# with Session(engine) as db:
#     db.add(item1)
#     db.add(item2)
#     db.commit()

# Add Order
# item1 = Order(count=10, description="User ordered 10 boxes of wine", user_iq=1, item_id=2)
# item2 = Order(count=10, description="User ordered 10 boxes of wine", user_iq=2, item_id=2)
#
#
# with Session(engine) as db:
#     db.add(item1)
#     db.add(item2)
#     db.commit()

with Session(engine) as db:
    users = db.exec(select(User)).all()
    print(users)

    user_1 = db.exec(select(User).where(col(User.FullName).contains('AA'))).first()
    print(user_1)
    print(user_1.orders)
