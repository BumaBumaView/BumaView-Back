from fastapi import FastAPI
import dotenv

from .dependencies import validate_env
from .web import user_router, company_router, question_router, interview_router, auth_router
from .repository.db import create_tables

app = FastAPI()

create_tables()

app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/api", tags=["users"])
app.include_router(company_router.router, prefix="/api", tags=["companies"])
app.include_router(question_router.router, prefix="/api", tags=["questions"])
app.include_router(interview_router.router, prefix="/api", tags=["interviews"])

dotenv.load_dotenv()
validate_env()


@app.get("/")
def read_root():
  return {"Hello": "World"}
