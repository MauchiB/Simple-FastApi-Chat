from fastapi import APIRouter, Depends, HTTPException, Path
from app.dependencies import get_current_user
from typing import Annotated, List
from sqlalchemy.orm import Session
from app.schemas.post_schemas import PostCreate, PostList, CommentCreate, CommentList
from app.services.post_services import create_post, list_posts, create_comment, list_comments, one_post_id
from app.dependencies import get_db, get_token


post_router = APIRouter(prefix='/post', tags=['posts'])


@post_router.post('/create-post', summary='Create post')
def create_user_post(data: PostCreate, user: Annotated[get_current_user, Depends()], db: Annotated[Session, Depends(get_db)]):
    data.post_user_id = user.id
    post = create_post(data=data, db=db)
    if post:
        return {'title':post.title,
                'description':post.description,
                'user':post.owner.username}
    else:
        raise HTTPException(status_code=409, detail={'error':'Post is already created'})
    
@post_router.get('/my-posts', response_model=List[PostList], summary='Return your posts')
def my_posts(user: Annotated[get_token, Depends()], db: Annotated[Session, Depends(get_db)]):
    posts = list_posts(db=db, user=user)
    return posts

@post_router.get('/{post_id}', response_model=PostList, summary='returns an ID post')
def one_post(user: Annotated[get_token, Depends()], db: Annotated[Session, Depends(get_db)], post_id: int = Path()):
    post = one_post_id(db=db, post_id=post_id)
    if post:
        return post
    raise HTTPException(status_code=404, detail={'post':'Post not found'})


@post_router.post('/create-comment/{post_id}', response_model=CommentCreate)
def create_comment_for_post(comment: CommentCreate,
                            user: Annotated[get_token, Depends()],
                            db: Annotated[Session, Depends(get_db)],
                            post_id: int = Path(),
                            ):
    comment.comment_user_id = user.id
    comment.post_id = post_id
    comment = create_comment(db=db, data=comment)
    if comment:
        return comment
    else:
        raise HTTPException(status_code=404, detail={'create':'Post is not found'})


@post_router.get('/comments-for/{post_id}', response_model=List[CommentList], description='Retrieves the list of comments to the post')
def my_posts(user: Annotated[get_token, Depends()], db: Annotated[Session, Depends(get_db)], post_id: int = Path()):
    comments = list_comments(db=db, user=user, post_id=post_id)
    return comments

