import time

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
import uvicorn

from storage.models import get_db
from routes import contacts, birthday, search

# TODO: remove after
from storage.models import User
from routes.schemas import UserCreate
from auth_service import Hash, create_access_token, get_current_user

app = FastAPI()
hash_handler = Hash()


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


# test endpoint
@app.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.email}


@app.post("/signup")
async def signup(body: UserCreate, db: Session = Depends(get_db)):
    exist_user: User | None = db.query(User).filter_by(email=body.email).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = User(email=body.email, password=hash_handler.get_password_hash(body.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@app.post("/login")
async def login(body: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=body.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


app.include_router(contacts.router, prefix='/api')
app.include_router(birthday.router, prefix='/api')
app.include_router(search.router, prefix='/api')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.7", port=8000)
