from pydantic import BaseModel

class Blog(BaseModel):
    title : str
    body : str

class ShowBlog(Blog):
    id: int

    class Config:
        orm_mode = True