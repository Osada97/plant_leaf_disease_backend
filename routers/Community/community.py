from typing import List
from fastapi import APIRouter, Depends, Request, File, UploadFile
from sqlalchemy.orm import session
from database import get_db
from oauth2 import get_current_plantUser
from repository.Community.comments import RemoveImageInComment, addCommentToPost, addDownVoteForComment, addImageToComment, addVoteForComment, getCommentOnId, removeCommentId, updateCommentId
from repository.Community.community import addDownVoteForPost, addImageToCommunityPost, addUpVoteForPost, createNewCommunityPost, getCommunityPostById, getCommunityPosts, removeCommunityPost, removeCommunityPostsComment, removeImageFromPost, updateCommunityPost
from repository.Community import userAuth
from schemas.community_schemas import CommunityPost, PostBool, ShowComment, ShowCommunityPost, CreateComment, Comment, ShowCommunityPostOnId

router = APIRouter(
    prefix='/community',
    tags=['community post']
)


# get new post
@router.get('/getpost', response_model=List[PostBool])
def getCommunityPost(req: Request, db: session = Depends(get_db)):
    return getCommunityPosts(req, db)


# user belong posts
@router.get('/getuserposts/{id}', response_model=List[PostBool])
def getUsersPost(id: int, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return getCommunityPostById(id, db, new_current_user)


# create new post
@router.post('/create/{id}', response_model=ShowCommunityPost)
def createCommunityPost(id: int, request: CommunityPost, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return createNewCommunityPost(id, request, db)

# update post


@router.put('/updatepost/{id}', response_model=ShowCommunityPost)
def updatePost(id: int, request: CommunityPost, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return updateCommunityPost(id, new_current_user, request, db)
# remove post


@router.delete('/removeposts/{id}')
def removePost(id: int, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return removeCommunityPost(id, new_current_user, db)

# remove comments that post have


@router.delete('/removepostscomment/{postId}/{commentId}')
def removePostsComment(postId: int, commentId: int, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return removeCommunityPostsComment(postId, commentId, new_current_user, db)

# add up vote


@router.post('/addvote/{id}')
def addVote(id: int,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addUpVoteForPost(id, new_current_user, db)


# add down vote
@router.post('/adddownvote/{id}')
def addVote(id: int,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addDownVoteForPost(id, new_current_user, db)

# add image to post


@router.post('/addimagetopost/{id}')
def addImagePost(id: int,  db: session = Depends(get_db), file: List[UploadFile] = File(..., media_type='image/jpeg'), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addImageToCommunityPost(id, new_current_user, db, file)
# remove image from post


@router.delete('/removeimageinpost/{id}')
def addImagePost(id: int,  db: session = Depends(get_db),  new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return removeImageFromPost(id, new_current_user, db)

#! COMMENT
# create new comment


@router.post('/comment/create/{id}', response_model=ShowComment)
def createComment(id: int, req: Request, request: CreateComment, db: session = Depends(get_db),  new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addCommentToPost(id, new_current_user, request, db)
# get new comment


@router.get('/comment/get/{id}', response_model=List[Comment])
def getComment(id: int, req: Request,  db: session = Depends(get_db)):
    return getCommentOnId(id, req, db)

# update  comment


@router.put('/comment/update/{id}')
def updateComment(id: int, request: CreateComment, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return updateCommentId(id, new_current_user, request, db)


# remove  comment
@router.delete('/comment/delete/{id}')
def removeComment(id: int, db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return removeCommentId(id, new_current_user, db)

# add up vote for commenet


@router.post('/comment/upvote/{id}')
def addVote(id: int,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addVoteForComment(id, new_current_user, db)


# add down vote for commenet
@router.post('/comment/downvote/{id}')
def addVote(id: int,  db: session = Depends(get_db), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addDownVoteForComment(id, new_current_user, db)

# add image to comment


@router.post('/comment/addimage/{id}')
def addImage(id: int, db: session = Depends(get_db), file: List[UploadFile] = File(..., media_type='image/jpeg'), new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return addImageToComment(id, db, file, new_current_user)

# remove image to comment


@router.delete('/comment/removeimage/{id}')
def removeImage(id: int, db: session = Depends(get_db),  new_current_user: userAuth.loginUser = Depends(get_current_plantUser)):
    return RemoveImageInComment(id, db, new_current_user)
