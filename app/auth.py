from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
import uuid
from sqlalchemy.orm import Session
from app.database import get_db   
from app.core.security import verify_password, hash_password, create_access_token, oauth2_scheme
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import User, Analysis
from app.schemas import UserCreate

def get_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        session_id = payload.get("session_id")

        if user_id is None or session_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # ✅ get user from DB
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # ✅ CRITICAL CHECK (Single Device Login)
        if user.current_session_id != session_id:
            raise HTTPException(
                status_code=401,
                detail="Session expired due to login from another device"
            )

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def create_user(user: UserCreate, db: Session = Depends(get_db),current_user: str = Depends(get_user)):   
    if not user.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")
    if user.age <= 0:
        raise HTTPException(status_code=400, detail="Age must be positive")

    user_id = str(uuid.uuid4())

    new_user = User(
        id=user_id,
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": user_id
    }

def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    email = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.email == email).first()

    if user:
        if verify_password(password, user.hashed_password):

            # ✅ NEW: generate session_id
            session_id = str(uuid.uuid4())

            # ✅ store in DB
            user.current_session_id = session_id
            db.commit()

            # ✅ include in token
            token = create_access_token({
                "user_id": user.id,
                "session_id": session_id
            })

            return {"access_token": token, "token_type": "bearer"}

        raise HTTPException(status_code=401, detail="Invalid password")

    raise HTTPException(status_code=401, detail="User not found")

def get_all_users(
    limit: int = Query(10),
    offset: int = Query(0),
    sort: str = Query("asc"),
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)   
):

    if limit <= 0 or limit > 400:
        raise HTTPException(status_code=400, detail="limit must be positive")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be zero or positive")
    if sort not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort value")

    users = db.query(User).all()  

    reverse_order = sort == "desc"
    users = sorted(users, key=lambda x: x.id, reverse=reverse_order)

    paginated_users = users[offset: offset + limit]

    return {
        "total_users": len(users),
        "limit": limit,
        "offset": offset,
        "data": paginated_users
    }

def get_user_detail(user_id: str,
                    token: str = Depends(get_user),
                    db: Session = Depends(get_db),current_user: str = Depends(get_user)):  

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(user_id: str,
                token: str = Depends(get_user),
                db: Session = Depends(get_db),current_user: str = Depends(get_user)):  

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if token != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    db.delete(user)
    db.commit()

    return JSONResponse(content={"message": "User deleted successfully"}) 

def create_analysis(
    user_id: str,
    text: str = Query(...),
    token: str = Depends(get_user),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_user)
):

    user = db.query(User).filter(User.id == user_id).first()   # ✅ FIXED
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not text or text.strip() == "":
        raise HTTPException(status_code=400, detail="Text is required")

    if len(text) > 200:
        raise HTTPException(status_code=400, detail="Text is too long")

    if token != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    analysis_id = str(uuid.uuid4())

    word_count = len(text.split())
    uppercase_count = sum(1 for c in text if c.isupper())
    special_character_count = sum(
        1 for c in text if not c.isalnum() and not c.isspace()
    )

    new_analysis = Analysis(  
        id=analysis_id,
        user_id=user_id,
        text=text,
        word_count=word_count,
        uppercase_count=uppercase_count,
        special_character_count=special_character_count
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return {
        "analysis_id": analysis_id,
        "word_count": word_count,
        "uppercase_count": uppercase_count,
        "special_character_count": special_character_count
    }

def get_all_analysis(user_id: str, current_user: str = Depends(get_user),
                     db: Session = Depends(get_db),
                     limit: int = Query(10, description="Number of users to return, must be positive"),
                     offset: int = Query(0, description="Starting index, must be zero or positive"),
                     sort: str = Query("asc", description="asc or desc for sorting by ID"),
                     min_words: int = Query(0, description="Minimum word count for filtering, must be zero or positive"),
                     ):

    if limit <= 0 or limit > 400:
        raise HTTPException(status_code=400, detail="limit must be positive")

    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be zero or positive")

    if sort not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort value")

    if min_words < 0:
        raise HTTPException(status_code=400, detail="min_words must be zero or positive")

    user = db.query(User).filter(User.id == user_id).first()   # ✅ FIXED
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    analyses = db.query(Analysis).filter(
        Analysis.user_id == user_id,
        Analysis.word_count >= min_words
    ).all()   # ✅ DB QUERY

    reverse_order = sort == "desc"

    analyses = sorted(analyses, key=lambda x: x.id, reverse=reverse_order)

    paginated = analyses[offset: offset + limit]

    return {
        "user_id": user_id,
        "total_after_filter": len(analyses),
        "limit": limit,
        "offset": offset,
        "data": paginated
    }

def get_analysis(
    user_id: str,
    analysis_id: str,
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()  
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == user_id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

def delete_analysis(
    user_id: str,
    analysis_id: str,
    current_user: str = Depends(get_user),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first() 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == user_id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    db.delete(analysis)
    db.commit()

    return JSONResponse(content={"message": "Analysis deleted successfully"})