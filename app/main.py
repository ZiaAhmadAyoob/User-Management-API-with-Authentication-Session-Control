from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import auth_routes, protected_routes, llm_routes
from app.database import Base, engine

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(protected_routes.router)
app.include_router(llm_routes.router)