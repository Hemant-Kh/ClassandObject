from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field  # Fixed typo: Basemodel -> BaseModel

app = FastAPI()

class Account(BaseModel):
    account_number: str = Field(..., example='123456789', description="Account number")
    