"""
FastAPI CRUD API for Tasks
A simple REST API with SQLite, Pydantic models, and auto-generated docs.
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
import sqlite3
import os

app = FastAPI(
    title="Task CRUD API",
    description="A simple FastAPI CRUD API for managing tasks",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "tasks.db"


def get_db():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            priority TEXT DEFAULT 'medium',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Pydantic models
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")


class Task(TaskBase):
    id: str
    completed: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class TaskList(BaseModel):
    tasks: List[Task]
    total: int
    page: int
    page_size: int


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "FastAPI Task CRUD"}


@app.get("/tasks", response_model=TaskList, tags=["Tasks"])
def list_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$", description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title and description"),
):
    """List all tasks with pagination and filtering."""
    conn = get_db()

    # Build query
    conditions = []
    params = []

    if completed is not None:
        conditions.append("completed = ?")
        params.append(1 if completed else 0)

    if priority:
        conditions.append("priority = ?")
        params.append(priority)

    if search:
        conditions.append("(title LIKE ? OR description LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Get total count
    cursor = conn.execute(f"SELECT COUNT(*) as count FROM tasks WHERE {where_clause}", params)
    total = cursor.fetchone()["count"]

    # Get paginated results
    offset = (page - 1) * page_size
    query = f"""
        SELECT * FROM tasks
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """
    cursor = conn.execute(query, params + [page_size, offset])
    rows = cursor.fetchall()
    conn.close()

    tasks = [dict(row) for row in rows]

    return TaskList(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size
    )


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task(task_id: str):
    """Get a single task by ID."""
    conn = get_db()
    cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    return dict(row)


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate):
    """Create a new task."""
    now = datetime.utcnow().isoformat()
    task_data = {
        "id": str(uuid4()),
        **task.model_dump(),
        "completed": False,
        "created_at": now,
        "updated_at": now
    }

    conn = get_db()
    conn.execute("""
        INSERT INTO tasks (id, title, description, completed, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task_data["id"],
        task_data["title"],
        task_data["description"],
        task_data["completed"],
        task_data["priority"],
        task_data["created_at"],
        task_data["updated_at"]
    ))
    conn.commit()
    conn.close()

    return task_data


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task(task_id: str, task: TaskUpdate):
    """Update an existing task."""
    conn = get_db()

    # Check if task exists
    cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing = cursor.fetchone()

    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    # Build update query
    updates = {}
    for field, value in task.model_dump(exclude_unset=True).items():
        if value is not None:
            updates[field] = value

    if not updates:
        conn.close()
        return dict(existing)

    updates["updated_at"] = datetime.utcnow().isoformat()

    set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
    conn.execute(
        f"UPDATE tasks SET {set_clause} WHERE id = ?",
        (*updates.values(), task_id)
    )
    conn.commit()

    # Fetch updated task
    cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated = cursor.fetchone()
    conn.close()

    return dict(updated)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: str):
    """Delete a task."""
    conn = get_db()

    cursor = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return None


@app.get("/stats", tags=["Stats"])
def get_stats():
    """Get task statistics."""
    conn = get_db()

    cursor = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) as pending,
            SUM(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) as high_priority
        FROM tasks
    """)
    row = cursor.fetchone()
    conn.close()

    stats = dict(row)
    stats["completion_rate"] = round(stats["completed"] / stats["total"] * 100, 1) if stats["total"] > 0 else 0

    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
