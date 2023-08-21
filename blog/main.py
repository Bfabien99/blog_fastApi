from fastapi import FastAPI, Depends

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

@app.get('/blogs')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"data":blogs}

@app.get('/blog/{id}')
def get_a_blog(id: int, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id==id).first()
    return {"data":blogs}
    
@app.post('/blog', name="Create a new blog")
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog