from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from passlib.context import CryptContext

from . import schemas, models
from sqlalchemy.orm import Session
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get('/blogs', response_model=List[schemas.ShowBlog], tags=["blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blogs"])
def get_a_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"detail":f"Blog with the id {id} was not found"}
    return blog
   
@app.post('/blog', name="Create a new blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog, tags=["blogs"])
def update_blog(id:int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} was not found")

    blog.update({"title":request.title, "body":request.body})
    db.commit()
    return blog.first()
    
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete_blog(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} was not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"data":"Deleted!"}

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
#get user with id
@app.get('/users', response_model=List[schemas.ShowUser], tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

#get user with id
@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def get_an_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} was not found")
    return user

#create user
@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pass = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#update user
@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["users"])
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} was not found")

    hashed_pass = pwd_cxt.hash(request.password)
    user.update({"name":request.name, "email":request.email, "password":hashed_pass})
    db.commit()
    return user.first()

#delete user
@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} was not found")
    user.delete(synchronize_session=False)
    db.commit()
    return {"data":"Deleted!"}