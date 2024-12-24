from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


SECRET_KEY = "supersecret"

ALGORITHM = "HS256"


origins = ["http://127.0.0.1:5500"]

app.add_middleware(

    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

users_db = {

    "user1": {"password": "password123", "roles": ["user"]},

    "admin": {"password": "adminpass", "roles": ["admin", "user"]},

}

class LoginRequest(BaseModel):
    username:str
    password:str


@app.post("/login-jwt")
def login_jwt(request: LoginRequest):

    if users_db.get(request.username) and users_db.get[request.username]['password'] == request.password:    #get method will always return true or false
        token_data ={
            'sub':request.username,
            'exp': datetime.utcnow() + timedelta(hours=1)

        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm = ALGORITHM )    
        return{"access token"}           

    raise HTTPException(status_code=401, detail="Invalid credentitals")


@app.get("/secure-data")

def secure_data(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username = payload.get("sub")

        return {"message": f"Hello, {username}"}

    except jwt.ExpiredSignatureError:

        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:

        raise HTTPException(status_code=401, detail="Invalid token")









