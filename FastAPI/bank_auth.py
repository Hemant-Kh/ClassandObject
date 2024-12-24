from fastapi import FastAPI, Path, Query, HTTPException, Depends
from pydantic import BaseModel, Field  # Fixed typo: Basemodel -> BaseModel


app = FastAPI()

def validate_api_key(api_key:str = Query(..., description="API key for authentication")):
    if api_key != "secure-api-key":
        raise HTTPException(status_code=403, detail="Invalid API key")

class Account(BaseModel):  # Fixed: Basemodel -> BaseModel
    account_number: str = Field(..., example="123456789",
                              description="The unique account number")
    account_holder: str = Field(..., example="Hemant",
                                description="The name of the account holder")
    balance: float = Field(..., example=10000.59,
                           description="The initial balance of the account")
    account_type: str = Field(..., example='Savings',
                              description="Type of the account (e.g. Savings, Current)")
    
class AccountResponse(BaseModel):  # Fixed: Basemodel -> BaseModel
    account_number: str
    message: str

account_db = {}

@app.post('/create_account', response_model=AccountResponse, dependencies=[Depends(validate_api_key)]) # dependencies is like a previous validation which has to be true for the function to execute.
def create_account(account:Account):
    if account.account_number in account_db:
        raise HTTPException(status_code=404, detail = "Account already exists" )
    account_db[account.account_number] = account

@app.get('/account/{account_number}', response_model=Account, dependencies=[Depends(validate_api_key)] )
def read_account(account_number:str = Path(..., description="the unique account number to be retrieved")):
    if account_number not in account_db:
        raise HTTPException(status_code=404, detail='account not found')
    return account_db[account_number]

@app.put('/account/{account_number}', response_model=AccountResponse, dependencies=[Depends(validate_api_key)])
def update_account(account_number:str, account :Account):
    if account_number not in account_db:
        raise HTTPException(status_code=404, detail='account not found')
    account_db[account_number] = account
    return {"account_number":account.account_number, "message": "Account successfully updated"}



