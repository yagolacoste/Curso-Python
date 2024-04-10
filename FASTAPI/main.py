from random import randrange
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


####Extiende de BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 4


my_posts = [{"title": "My title of posts 1", "content": "My contento of posts 1", "id": 1},
            {"title": "My favourite food ", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")  ##es la dependencia de get
def root():
    return {"message": " Welcom to te api fast111"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


##En este ejemplo cambio de posicion la funcion porque pasaba que cuando leia /post/ pensaba que era el path
##/post/id y tomaba el lastest como id
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):  ##hace saltar una exceptcion de que tiene que ser un integer si o si
    ##post= find_post(int(id)) ##Lo que le paso aca es que lo casteo porque vino un string como id y tenemos integer
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'message': f"post with id:{id} is not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_posts(id: int):
    index = find_index(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found")
    my_posts.pop(index)  ##remueve el valor en el indice
    return Response(status_code=status.HTTP_204_NO_CONTENT)
