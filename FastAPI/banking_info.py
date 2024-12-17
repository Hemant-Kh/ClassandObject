from fastapi import FastAPI, Path, Query, HTTPExeption

from pydantic import Basemodel, Field

app = FastAPI()

class Account(Basemodel):
    account_number: str = Field(..., example = "123456789", description = "The unique account number")
    account_holder: str = Field(..., example = "Hemant", description = "The name of account holder")
    account_balance: float = Field(..., example = "10000.59", description = "The initial balance in the account")
    account_type: str = Field(..., example = "Savings", description = "Type of the account(e.g savings, Current)")



class AccountResponse(Basemodel):
    account_number: str
    message: str

account_db = {}


# create a new bank account and store it in the database, this is a post method (update method)

@app.post('/account', response_model = AccountResponse ) # parameter is that the response will be in the format of that class
def create_account(account: Account):    # parameter is that the input will be in the format of that class
    if account.account_number in account_db:
        raise  HTTPExeption(status_code = 400, details = "Account number already exists")                               # 
    account_db[account.account_number] = account
    return {'account number ' : account.account_number, 'message' : 'Account succesfully created'}









