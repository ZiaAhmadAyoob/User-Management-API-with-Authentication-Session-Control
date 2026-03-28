from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.database import get_db   
from app.auth import (
    get_user,
    delete_user,
    create_analysis,
    get_all_analysis,
    get_analysis,
    delete_analysis,
    get_user_detail,
    get_all_users   
)

router = APIRouter()

@router.get("/users/{user_id}")
def get_new_user_detail(
    user_id: str,
    token: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return get_user_detail(user_id, token, db)


@router.get("/users")
def get_new_all_users(
    limit: int = Query(10),
    offset: int = Query(0),
    sort: str = Query("asc"),
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return get_all_users(limit, offset, sort, current_user, db)   # ✅ FIXED


@router.delete("/users/{user_id}")
def delete_new_user(
    user_id: str,
    token: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return delete_user(user_id, token, db)


# ---------------- ANALYSIS ---------------- #

@router.post("/users/{user_id}/analysis")
def create_new_analysis(
    user_id: str,
    text: str = Query(...),
    token: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return create_analysis(user_id, text, token, db, token)


@router.get("/users/{user_id}/analysis")
def get_new_all_analysis(
    user_id: str,
    token: str = Depends(get_user),
    db: Session = Depends(get_db),   # ✅ ADD
    limit: int = Query(10),
    offset: int = Query(0),
    sort: str = Query("asc"),
    min_words: int = Query(0)
):
    return get_all_analysis(user_id, token, db, limit, offset, sort, min_words)


@router.get("/users/{user_id}/analysis/{analysis_id}")
def get_new_analysis(
    user_id: str,
    analysis_id: str,
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return get_analysis(user_id, analysis_id, current_user, db)


@router.delete("/users/{user_id}/analysis/{analysis_id}")
def delete_new_analysis(
    user_id: str,
    analysis_id: str,
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)   # ✅ ADD
):
    return delete_analysis(user_id, analysis_id, current_user, db)