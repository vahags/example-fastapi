from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags=['Users']
)

#Create User
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #this resets the new_user variable ??

    return new_user

#Get all users
@router.get("/", response_model = List[schemas.UserCreate])
def get_users(db: Session = Depends(get_db)):
#     cursor.execute("""SELECT * FROM users""")
#     posts = cursor.fetchall()
    users = db.query(models.User).all()
    return users

#get one user
@router.get("/{id}", response_model = schemas.UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user