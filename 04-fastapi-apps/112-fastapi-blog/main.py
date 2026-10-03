"""
FastAPI Blog API with SQLite - Posts, Comments, Categories, Pagination
"""

from fastapi import FastAPI, HTTPException, Depends, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./blog.db"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Association tables
post_categories = Table(
    'post_categories', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# SQLAlchemy Models
class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("PostModel", secondary=post_categories, back_populates="categories")

class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    published = Column(Integer, default=0)  # 0=draft, 1=published
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("CategoryModel", secondary=post_categories, back_populates="posts")
    comments = relationship("CommentModel", back_populates="post", cascade="all, delete-orphan")

class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    approved = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("PostModel", back_populates="comments")

# Pydantic Models
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    author: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    approved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)
    category_ids: Optional[List[int]] = []
    published: bool = False

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    content: Optional[str] = None
    category_ids: Optional[List[int]] = None
    published: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    author: str
    published: bool
    views: int
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse]
    comment_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    author: str
    published: bool
    views: int
    created_at: datetime
    categories: List[CategoryResponse]
    comment_count: int = 0

    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    per_page: int
    pages: int

# FastAPI App
app = FastAPI(
    title="Blog API",
    description="A Blog API with posts, comments, categories, and pagination",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

# Helper function
def slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return re.sub(r'^-+|-+$', '', text)

# Startup event
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ==================== CATEGORIES ====================

@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    slug = slugify(category.name)
    result = await db.execute(select(CategoryModel).filter(CategoryModel.slug == slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    db_category = CategoryModel(
        name=category.name,
        slug=slug,
        description=category.description
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryModel).order_by(CategoryModel.name))
    return result.scalars().all()

@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryModel).filter(CategoryModel.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CategoryModel).filter(CategoryModel.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()

# ==================== POSTS ====================

@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    slug = slugify(post.title)
    result = await db.execute(select(PostModel).filter(PostModel.slug == slug))
    if result.scalar_one_or_none():
        slug = f"{slug}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    db_post = PostModel(
        title=post.title,
        slug=slug,
        content=post.content,
        author=post.author,
        published=1 if post.published else 0
    )

    if post.category_ids:
        result = await db.execute(select(CategoryModel).filter(CategoryModel.id.in_(post.category_ids)))
        categories = result.scalars().all()
        db_post.categories = list(categories)

    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return PostResponse(
        **{
            **db_post.__dict__,
            "published": bool(db_post.published),
            "comment_count": len(db_post.comments)
        }
    )

@app.get("/posts", response_model=PaginatedResponse)
async def get_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    author: Optional[str] = None,
    category_id: Optional[int] = None,
    published_only: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select, func, select

    query = select(PostModel)
    count_query = select(func.count()).select_from(PostModel)

    if published_only:
        query = query.filter(PostModel.published == 1)
        count_query = count_query.filter(PostModel.published == 1)

    if author:
        query = query.filter(PostModel.author.ilike(f"%{author}%"))
        count_query = count_query.filter(PostModel.author.ilike(f"%{author}%"))

    if category_id:
        query = query.join(post_categories).filter(post_categories.c.category_id == category_id)
        count_query = count_query.select_from(PostModel).join(post_categories).filter(post_categories.c.category_id == category_id)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.order_by(PostModel.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    posts = result.scalars().all()

    items = []
    for p in posts:
        items.append(PostListResponse(
            id=p.id,
            title=p.title,
            slug=p.slug,
            author=p.author,
            published=bool(p.published),
            views=p.views,
            created_at=p.created_at,
            categories=[CategoryResponse.model_validate(c) for c in p.categories],
            comment_count=len([c for c in p.comments if c.approved])
        ))

    pages = (total + per_page - 1) // per_page

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages
    )

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(PostModel).filter(PostModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Increment views
    post.views += 1
    await db.commit()

    return PostResponse(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        author=post.author,
        published=bool(post.published),
        views=post.views,
        created_at=post.created_at,
        updated_at=post.updated_at,
        categories=[CategoryResponse.model_validate(c) for c in post.categories],
        comment_count=len([c for c in post.comments if c.approved])
    )

@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_data: PostUpdate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(PostModel).filter(PostModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_data.title:
        post.title = post_data.title
        post.slug = slugify(post_data.title)
    if post_data.content:
        post.content = post_data.content
    if post_data.published is not None:
        post.published = 1 if post_data.published else 0
    if post_data.category_ids is not None:
        result = await db.execute(select(CategoryModel).filter(CategoryModel.id.in_(post_data.category_ids)))
        categories = result.scalars().all()
        post.categories = list(categories)

    post.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(post)

    return PostResponse(
        id=post.id,
        title=post.title,
        slug=post.slug,
        content=post.content,
        author=post.author,
        published=bool(post.published),
        views=post.views,
        created_at=post.created_at,
        updated_at=post.updated_at,
        categories=[CategoryResponse.model_validate(c) for c in post.categories],
        comment_count=len([c for c in post.comments if c.approved])
    )

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(PostModel).filter(PostModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()

# ==================== COMMENTS ====================

@app.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(PostModel).filter(PostModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = CommentModel(
        post_id=post_id,
        author=comment.author,
        content=comment.content
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int,
    approved_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    result = await db.execute(select(PostModel).filter(PostModel.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    query = select(CommentModel).filter(CommentModel.post_id == post_id)
    if approved_only:
        query = query.filter(CommentModel.approved == 1)
    query = query.order_by(CommentModel.created_at.desc())

    result = await db.execute(query)
    comments = result.scalars().all()

    return [CommentResponse(
        id=c.id,
        post_id=c.post_id,
        author=c.author,
        content=c.content,
        approved=bool(c.approved),
        created_at=c.created_at
    ) for c in comments]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
