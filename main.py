from fastapi import FastAPI
from models import Blog
import uvicorn

from typing import Optional

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"creator":"Brou Kouadio Stéphane-Fabien"}}

@app.get('/blogs')
def get_blogs(limit: int=100, published: bool=True, sort: Optional[str] = None):
    if published:
        return {"data":f"{limit} published blogs from db"}
    return {"data":f"{limit} blogs from db"}

@app.get('/blogs/unpublished')
def get_unpublished_blogs():
    return {"data":"show all unpublished blogs"}

@app.get('/blog/{id}')
def get_blog(id: int):
    # fetch blog with id = id
    return {"data":f"show blog {id}"}

@app.get('/blog/{id}/comments')
def get_blog_comments(id: int):
    # fetch comments of blog with id = id
    return {"data":{"comments":f"comments of blog {id}"}}

@app.post('/blog')
def create_blog(blog: Blog):
    return {"data":blog}


if __name__ =='__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)