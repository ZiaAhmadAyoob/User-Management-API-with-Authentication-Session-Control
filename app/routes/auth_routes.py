from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from app.auth import create_user, login, get_user
from app.schemas import UserCreate

router = APIRouter()

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(get_user)):
    return login(form_data)

@router.post("/users",  status_code=201)
def create_new_user(user: UserCreate):
    return create_user(user)