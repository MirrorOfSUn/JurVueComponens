import math
from typing import Union, Sequence, List, Annotated
from fastapi import status, Query, Depends, HTTPException
# from sqlalchemy.orm import Session
from sqlmodel import Session, select, SQLModel, col, or_, func
from Db_model import User, Item, Order, UserEdit, UserList, UserCreate, UserListRequest

from . import api_app, engine, get_session


def select_generator(model: SQLModel, q: dict):
    pass


@api_app.post("/users", response_model=UserList)
def user_list_search(*, db: Session = Depends(get_session), so: UserListRequest):

    # first page = 1

    query = select(User)
    query_count = select(func.count(User.id))
    total_records = db.exec(query_count).one()
    if so.search:
        query = query.where(or_(
            col(User.FirstName).contains(so.search),
            col(User.MiddleName).contains(so.search),
            col(User.LastName).contains(so.search),
            col(User.FullName).contains(so.search),
            col(User.Phone1).contains(so.search),
            col(User.Phone2).contains(so.search),
            col(User.Email1).contains(so.search),
            col(User.Email2).contains(so.search),
            col(User.Address).contains(so.search)
        ))
        query_count = query_count.where(or_(
            col(User.FirstName).contains(so.search),
            col(User.MiddleName).contains(so.search),
            col(User.LastName).contains(so.search),
            col(User.FullName).contains(so.search),
            col(User.Phone1).contains(so.search),
            col(User.Phone2).contains(so.search),
            col(User.Email1).contains(so.search),
            col(User.Email2).contains(so.search),
            col(User.Address).contains(so.search)
        ))
    else:
        if so.name:
            query = query.where(col(User.FullName).contains(so.name))
            query_count = query_count.where(col(User.FullName).contains(so.name))
        if so.phone:
            query = query.where(
                or_(
                    col(User.Phone1).contains(so.phone),
                    col(User.Phone2).contains(so.phone)
                ))
            query_count = query_count.where(
                or_(
                    col(User.Phone1).contains(so.phone),
                    col(User.Phone2).contains(so.phone)
                ))
        if so.email:
            query = query.where(or_(col(User.Email1).contains(so.email), col(User.Email2).contains(so.email)))
            query_count = query_count.where(or_(col(User.Email1).contains(so.email), col(User.Email2).contains(email)))
        if so.address:
            query = query.where(col(User.Address).contains(so.address))
            query_count = query_count.where(col(User.Address).contains(so.address))

    query = query.where(User.is_active == so.is_active)
    query_count = query_count.where(User.is_active == so.is_active)

    total_filtered_records = db.exec(query_count).one()
    total_pages = math.ceil(total_filtered_records/so.page_size)
    if so.page >= total_pages:
        so.page = total_pages if total_pages else 1
    offset = (so.page-1) * so.page_size  # page -1 because numeration start from 1
    users = db.exec(query.offset(offset).limit(so.page_size)).all()

    user_list = UserList(datatable=users,
                         total_records=total_records,
                         total_filtered_records=total_filtered_records,
                         total_pages=total_pages,
                         page_size=so.page_size,
                         current_page=so.page)
    return user_list


@api_app.get("/users", response_model=UserList)
def user_list_all(*, db: Session = Depends(get_session),
                  name: Annotated[str, Query(max_length=50)] = '',
                  phone: Annotated[str, Query(max_length=15)] = '',
                  email: Annotated[str, Query(max_length=50)] = '',
                  address: Annotated[str, Query(max_length=50)] = '',
                  is_active: bool = True,
                  page: int = 1,
                  page_size: int = Query(default=100, le=100)):

    if page < 1:
        page = 1  # first page = 1
    query = select(User)
    query_count = select(func.count(User.id))
    total_records = db.exec(query_count).one()
    if name:
        query = query.where(col(User.FullName).contains(name))
        query_count = query_count.where(col(User.FullName).contains(name))
    if phone:
        query = query.where(
            or_(
                col(User.Phone1).contains(phone),
                col(User.Phone2).contains(phone)
            ))
        query_count = query_count.where(
            or_(
                col(User.Phone1).contains(phone),
                col(User.Phone2).contains(phone)
            ))
    if email:
        query = query.where(or_(col(User.Email1).contains(email), col(User.Email2).contains(email)))
        query_count = query_count.where(or_(col(User.Email1).contains(email), col(User.Email2).contains(email)))
    if address:
        query = query.where(col(User.Address).contains(address))
        query_count = query_count.where(col(User.Address).contains(address))

    query = query.where(User.is_active == is_active)
    query_count = query_count.where(User.is_active == is_active)

    total_filtered_records = db.exec(query_count).one()
    total_pages = math.ceil(total_filtered_records/page_size)
    if page >= total_pages:
        page = total_pages if total_pages else 1
    offset = (page-1) * page_size  # page -1 because numeration start from 1
    users = db.exec(query.offset(offset).limit(page_size)).all()

    user_list = UserList(datatable=users,
                         total_records=total_records,
                         total_filtered_records=total_filtered_records,
                         total_pages=total_pages,
                         page_size=page_size,
                         current_page=page)
    return user_list


@api_app.post("/user", status_code=status.HTTP_201_CREATED)
def user_create(user: UserCreate):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    new_user = User(**user.dict())

    # add it to the session and commit it
    session.add(new_user)
    session.commit()

    # grab the id given to the object from the database
    id = new_user.id

    # close the session
    session.close()
    # return the id
    return f"created user with id {id}"


@api_app.get("/user/{user_id}")
def user_get_by_id(*, db: Session = Depends(get_session), user_id: int):
    # session = Session(bind=engine, expire_on_commit=False)
    user = db.exec(select(User).where(User.id == user_id)).first()
    # session.close()
    return user


@api_app.patch("/user/{user_id}", response_model=UserEdit)
def user_update(*, db: Session = Depends(get_session), user_id: int, user: User):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@api_app.delete("/user/{user_id}")
def user_delete(user_id: int):
    return "Delete user"
