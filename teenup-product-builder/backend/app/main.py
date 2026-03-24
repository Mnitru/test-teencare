from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import parents, students, classes, registrations, subscriptions

app = FastAPI(title="TeenUp Mini LMS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parents.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(registrations.router)
app.include_router(subscriptions.router)

@app.get("/")
def root():
    return {"message": "TeenUp API đang chạy"}