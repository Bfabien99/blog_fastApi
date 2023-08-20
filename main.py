from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"creator":"Brou Kouadio Stéphane-Fabien"}}

@app.get('/blogs')
def get_blogs(limit: int=100):
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