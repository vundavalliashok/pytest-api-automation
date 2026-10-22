from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

app = FastAPI(
    title="Pytest API Automation Demo",
    description="A portfolio-ready REST API for demonstrating pytest automation.",
    version="1.0.0",
)

class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=80)]
    email: Annotated[str, Field(min_length=5, max_length=254)]
    age: Annotated[int, Field(ge=18, le=120)]

class User(UserCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

# In-memory storage keeps the sample runnable without external services.
_users: dict[int, User] = {}
_next_id = 1

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(payload: UserCreate):
    global _next_id
    if any(user.email.lower() == payload.email.lower() for user in _users.values()):
        raise HTTPException(status_code=409, detail="Email already exists")
    user = User(id=_next_id, **payload.model_dump())
    _users[_next_id] = user
    _next_id += 1
    return user

@app.get("/users", response_model=list[User], tags=["users"])
def list_users():
    return list(_users.values())

@app.get("/users/{user_id}", response_model=User, tags=["users"])
def get_user(user_id: int):
    user = _users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="User not found")
    del _users[user_id]
    return None

@app.post("/testing/reset", include_in_schema=False)
def reset_test_data():
    """Demo-only helper. Do not expose an endpoint like this in production."""
    global _next_id
    _users.clear()
    _next_id = 1
    return {"status": "reset"}
