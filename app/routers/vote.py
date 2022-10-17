from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database

router = APIRouter(
    prefix = "/vote", 
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post_result = post_query.first() #will return none if post does not exist in the posts table

    if post_result == None: #if the post doesn't exist, raise a 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Post with ID {vote.post_id} does not exist')

    if (vote.dir) == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'user {current_user.id} has already liked the post with the post of {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}
