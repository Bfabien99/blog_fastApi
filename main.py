from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"data":{"creator":"Brou Kouadio Stéphane-Fabien"}}

@app.get('/about')
def index():
    return {"data":"about page"}