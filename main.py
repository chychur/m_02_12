import time

from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from storage.models import get_db
from routes import contacts, birthday, search


app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get("/api/healthchecker", name="HealthChecker")  # DB connection testing
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


@app.get("/", name="root")
async def read_root():
    return {"message": "Welcome to FastApi. REST API v1.0"}


app.include_router(contacts.router, prefix='/api')
app.include_router(birthday.router, prefix='/api')
app.include_router(search.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.7", port=8000)