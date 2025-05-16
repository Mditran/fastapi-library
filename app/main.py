from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, Base
from .routers import book, user, loan
from .models import books, users, roles, user_roles, loans
from fastapi.middleware.cors import CORSMiddleware
from .seed_data import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI()

origins = [
    "www.enlace.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(book.router)
app.include_router(loan.router)

@app.get("/")
def root():
    return {"message": "Welcome to the best online library!!"}


