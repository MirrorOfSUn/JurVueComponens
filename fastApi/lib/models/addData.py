import random

from sqlmodel import create_engine, Session

from Db_model import User
with open('first_name.txt') as f:
    fn = f.read().splitlines()

with open('last_name.txt') as f:
    ln = f.read().splitlines()

engine = create_engine(
    'sqlite:///../../DB/users.sqlite',
    connect_args={"check_same_thread": False},
    echo=True
)


def get_phone():
    def n():
        return random.randint(0, 10)
    return f"{n()}{n()}{n()}-{n()}{n()}{n()}-{n()}{n()}{n()}{n()}"


session = Session(bind=engine, expire_on_commit=False)

for i in range(500):
    first_i = random.randint(0, len(fn))
    last_i = random.randint(0, len(ln))
    middle_i = random.randint(0, len(fn))
    first = fn[first_i]
    last = ln[last_i]
    middle = ''
    if random.randint(0, 10) >5:
        middle = fn[first_i][0]

    phone1 = get_phone()
    phone2 = ""
    if random.randint(0, 10) > 5:
        phone2 = get_phone()

    email1 = f"{first}.{last}@email.com"
    email2 = ""
    if random.randint(0, 10) > 5:
        email2 = f"{first}.{last}@email.com"

    u = User(FirstName=first,
             LastName=last,
             MiddleName=middle,
             Phone1=phone1,
             Phone2=phone2,
             Email1=email1,
             Email2=email1,
             Address=f"Address of {last}",
             is_active=True
            )
    print(u)

    session.add(u)
    session.commit()
session.close()

# new_user = User(FirstName: name)


