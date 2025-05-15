from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, Base
from .routers import book, user, loan

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(book.router)

@app.get("/")
def root():
    return {"message": "Welcome to the best online library!!"}


