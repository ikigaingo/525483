from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import api

from app.models import Base
from app.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title='API Ikigai NGO Audit Suspense')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(api.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
