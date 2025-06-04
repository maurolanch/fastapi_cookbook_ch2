from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_example.database import SessionLocal, User
from pydantic import BaseModel



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get("/users/")
def read_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

class UserBody(BaseModel):
    name: str
    email:str


@app.post("/user")
def add_new_user(
    user: UserBody,  
    db: Session = Depends(get_db)
    ):
    new_user = User(
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
    ):
    user = (
        db.query(User).filter(User.id == user_id).first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@app.post("/user/{user_id}")
def update_user(
    user_id: int,
    user:UserBody,
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(User).filter(User.id == user_id).first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.user_name = user.name
    db.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/user")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

