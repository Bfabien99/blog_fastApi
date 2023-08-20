from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"creator":"Brou Kouadio Stéphane-Fabien"}}

@app.get('/blogs')
def get_blogs():
    return {"data":"show all blogs"}

@app.get('/blog/{id}')
def get_blog(id):
    return {"data":"show blog "+id}