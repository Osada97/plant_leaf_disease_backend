from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from database import get_db
from oauth2 import get_current_plantUser
from repository.Community.community import createNewCommunityPost, getCommunityPosts
from repository.Community import userAuth
from schemas.community_schemas import CommunityPost, ShowCommunityPost

router = APIRouter(
    prefix='/community',
    tags=['community post']
)

# get new post


@router.get('/getpost', response_model=List[ShowCommunityPost])
def getCommunityPost(db: session = Depends(get_db)):
    return getCommunityPosts(db)
# get new post with user id
# create new post


@router.post('/create/{id}', response_model=CommunityPost)
def createCommunityPost(id: int, request: CommunityPost, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return createNewCommunityPost(id, request, db)

# update new post
# remove new post

# add up vote
# remove up vote
# add down vote
# remove down vote

# add image to post
# remove image from post

# create new comment
# get new comment
# update new comment
# remove new comment
