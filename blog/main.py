from fastapi import FastAPI
from . import schemas

app = FastAPI()
    
@app.post('/blog')
def create(blog: schemas.Blog):
    return {"data":blog}