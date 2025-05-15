from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, Base
from .routers import book, user, loan, auth
from models import books, users, roles, user_roles, loans

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(book.router)

@app.get("/")
def root():
    return {"message": "Welcome to the best online library!!"}


