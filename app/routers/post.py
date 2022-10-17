from .. import models, schemas, utils
from typing import List, Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#get ALL posts from database
#@router.get("/", response_model = List[schemas.Post])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()

    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #below lines are how you use SQL Query Language to create posts in database
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() 

    
    newpost = post.dict()
    newpost.update({"owner_id":current_user.id})
    new_post = models.Post(**newpost)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

#Get only ONE Post by ID
#@router.get("/{id}", response_model=schemas.PostOut)
@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) #you have to turn id into a str otherwise error message for int indexing... comma at the end is needed for certain errors
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    Post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #print("This is the post: ", post)
    #if current_user.id == post.owner_id:

    if not Post: #if post == None because no ID matched p for p in my_posts
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

        #response.status_code = status.HTTP_404_NOT_FOUND
        #return "This is not the page you are looking for"

    return Post

#Delete one Post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) #comma after str(id) is recommended by professor to avoid potential error messages
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Could not find post with given ID: {id}")

    print(f"post owner ID:{post.owner_id}    current user ID: {current_user.id}")
    print("this is the post", post)

    if post.owner_id != current_user.id: #checks if the current user ID matches with the owner ID row
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session=False) #deletes the post
    db.commit()
    
#Update Post
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #print(update_post,updated_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_result = post_query.first()
    if post_result == None:#if post does not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")

    if post_result.owner_id != current_user.id: #checks if the current user ID matches with the owner ID row
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")

    post_query.update(post.dict(),synchronize_session=False)
    return post_result