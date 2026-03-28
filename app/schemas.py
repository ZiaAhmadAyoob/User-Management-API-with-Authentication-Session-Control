from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LLMRequest(BaseModel):
    prompt: str
                