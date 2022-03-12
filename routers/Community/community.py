from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import session
from database import get_db
from oauth2 import get_current_plantUser
from repository.Community.community import addDownVoteForPost, addUpVoteForPost, createNewCommunityPost, getCommunityPostById, getCommunityPosts, removeCommunityPost, updateCommunityPost
from repository.Community import userAuth
from schemas.community_schemas import CommunityPost, ShowCommunityPost

router = APIRouter(
    prefix='/community',
    tags=['community post']
)


# get new post
@router.get('/getpost', response_model=List[ShowCommunityPost])
def getCommunityPost(req: Request, db: session = Depends(get_db)):
    return getCommunityPosts(req, db)


# user belong posts
@router.get('/getuserposts/{id}', response_model=List[ShowCommunityPost])
def getUsersPost(id: int, db: session = Depends(get_db)):
    return getCommunityPostById(id, db)


# create new post
@router.post('/create/{id}', response_model=CommunityPost)
def createCommunityPost(id: int, request: CommunityPost, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return createNewCommunityPost(id, request, db)

# update post


@router.put('/updatepost/{id}', response_model=CommunityPost)
def updatePost(id: int, req: Request, request: CommunityPost, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return updateCommunityPost(id, req, request, db)
# remove post


@router.delete('/removeposts/{id}')
def removePost(id: int, req: Request, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return removeCommunityPost(id, req, db)

# add up vote


@router.post('/addvote/{id}')
def addVote(id: int, req: Request,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addUpVoteForPost(id, req, db)


# add down vote
@router.post('/adddownvote/{id}')
def addVote(id: int, req: Request,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addDownVoteForPost(id, req, db)

# add image to post
# remove image from post

# create new comment
# get new comment
# update new comment
# remove new comment
