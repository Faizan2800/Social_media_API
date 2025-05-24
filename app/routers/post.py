from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from ..oauth2 import get_current_user
from sqlalchemy import func

# Set up the router for post-related endpoints
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# -------------------- GET ALL POSTS --------------------
@router.get("/", response_model=List[schemas.PostOut])  # get used when retrieving data
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, 
              skip: int = 0,
              search: Optional[str] = ""):
    print(limit)
    
    # Optionally used when interacting directly with raw SQL (commented out here)
    # cursor.execute("SELECT * FROM social_media_posts")
    # posts = cursor.fetchall()  # Each row is a dictionary thanks to RealDictCursor

    # Retrieve posts matching the search query with pagination
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Retrieve posts and count of votes using an outer join, grouped by post
    vote_count = func.count(models.Vote.post_id).label("votes")
    results = (
        db.query(models.Post, vote_count)
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    return results
# -------------------- CREATE A POST --------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): 
    # stores it as a pydantic model
    # cursor.execute("""INSERT INTO social_media_posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))    
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)  # user ID from token
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())  # converts pydantic model to dict and unpacks
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # To get the auto-generated fields like id, created_at
    return new_post


# title: str, content: str, published: bool

# -------------------- GET A SINGLE POST BY ID --------------------
@router.get("/{id}", response_model=schemas.PostOut)  # id field is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(get_current_user)):
    # cursor.execute("""SELECT * from social_media_posts WHERE id = %s """, (str(id),))
    # test_post = cursor.fetchone()
    # post = db.query(models.Post)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

# -------------------- DELETE A POST --------------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM social_media_posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -------------------- UPDATE A POST --------------------
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    # cursor.execute(
    #     """
    #     UPDATE social_media_posts 
    #     SET title = %s, content = %s, published = %s 
    #     WHERE id = %s 
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
