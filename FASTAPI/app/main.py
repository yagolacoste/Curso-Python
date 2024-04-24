import time

import mysql.connector
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


####Extiende de BaseModel
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


##Esto sirve para hacer una conexion a la base de datos mysql pero hay que cambiar pequeñas cosas para usar otro motor
##Este codigo en si esta mal porque estamos mostrando nuestros datos de la base de datos
while True:
    try:
        conn = mysql.connector.connect(host='localhost', database='fastapi', user="root ",
                                       password="root")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SHOW DATABASES")
        for bd in cursor:
            print(bd)
        print("Database connection was succesfull!!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

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


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    ##Dejo evidencia de que uso execute con sql
    # posts = cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data": posts}
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict())  ## esto hace que el post que recibimos lo convierta en un diccionario y que a su vez lo ponga en el mismo formato que se requiere
    db.add(new_post)
    db.commit()
    db.refresh()
    return {"data": new_post}
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)""",
    #                (post.title, post.content, post.published))
    # cursor.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID();")
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}


##En este ejemplo cambio de posicion la funcion porque pasaba que cuando leia /post/ pensaba que era el path
##/post/id y tomaba el lastest como id
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int,
             db: Session = Depends(get_db)):  ##hace saltar una exceptcion de que tiene que ser un integer si o si
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": posts}
    # ##post= find_post(int(id)) ##Lo que le paso aca es que lo casteo porque vino un string como id y tenemos integer
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} was not found")
    # return {"Post_detail": post}
    # ## ESTO LO HIZO PORQUE NO HABIA BASE DE DATOS
    # # post = find_post(id)
    # # if not post:
    # #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} is not found")
    # # # if not post:
    # # #     response.status_code = status.HTTP_404_NOT_FOUND
    # # #     return {'message': f"post with id:{id} is not found"}
    # # return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute("DELETE FROM posts Where id= %s", (str(id),))
    # conn.commit()
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    # # my_posts.pop(index)  ##remueve el valor en el indice
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    post_query.update(update_posts.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
    #                (post.title, post.content, post.published, id))
    # conn.commit()
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    #
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # updated_post = cursor.fetchone()
    # return {"data": updated_post}

    # index = find_index(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # return {"post_detail": post}
