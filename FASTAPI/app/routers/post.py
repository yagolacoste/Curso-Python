from typing import List, Optional
from fastapi import Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",  # pone un prefijo para no repetir en cada caso
    tags=['Posts']
)  ##agrega este enrutador para que al estar separado por .py pueda acceder


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user), limit: int = 10, skip: int = 10, search: Optional[str] = ""):
    ##Dejo evidencia de que uso execute con sql
    # posts = cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # print(posts)
    # return {"data": posts}
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(created_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(
                     oauth2.get_current_user)):  ##llama al get_current_user del oauth para verificar ese usuario
    new_post = models.Post(owner_id=current_user.id,
                           **created_post.dict())  ## esto hace que el post que recibimos lo convierta en un diccionario y que a su vez lo ponga en el mismo formato que se requiere
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s)""",
    #                (post.title, post.content, post.published))
    # cursor.execute("SELECT * FROM posts WHERE id = LAST_INSERT_ID();")
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,
             db: Session = Depends(get_db), current_user: int = Depends(
            oauth2.get_current_user)):  ##hace saltar una exceptcion de que tiene que ser un integer si o si
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perfomr requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute("DELETE FROM posts Where id= %s", (str(id),))
    # conn.commit()
    # if cursor.rowcount == 0:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} not found")
    # # my_posts.pop(index)  ##remueve el valor en el indice
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perfomr requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
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
