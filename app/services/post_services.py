from sqlalchemy.orm import Session
from app.models.post import Post, Comment
from app.schemas.post_schemas import PostCreate, CommentCreate
from app.models.user import User


def create_post(data: PostCreate, db: Session):
    post = db.query(Post).filter(Post.title == data.title).first()
    if post:
        return False
    post = Post(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def list_posts(db: Session, user: User):
    '''return list pydantic model - PostList'''
    posts = db.query(Post).filter(Post.post_user_id == user.id).all()
    user_posts = []
    for post in posts:
        my_dict = {
            'title':post.title,
            'description':post.description,
            'email':user.email,
            'username':user.username
        }
        user_posts.append(my_dict)
    return user_posts

def one_post_id(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return {'title':post.title, 'description':post.description, 'email':post.owner.email, 'username':post.owner.username}
    return False

def create_comment(db: Session, data: CommentCreate):
    post = db.query(Post).get({'id':data.post_id})
    if not post:
        return False
    comment = Comment(**data.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, user: User, post_id):
    '''return list pydantic model - CommentList'''
    comments = db.query(Comment).filter((Comment.post_id == post_id) & (Comment.comment_user_id == user.id)).all()
    user_posts = []
    for comment in comments:
        my_dict = {
            'created_at':comment.created_at,
            'username':comment.user.username,
            'message':comment.message,
        }
        user_posts.append(my_dict)
    return user_posts