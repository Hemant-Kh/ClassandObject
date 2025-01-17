from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field  # Fixed typo: Basemodel -> BaseModel

app = FastAPI()

# Define the Account model


class Account(BaseModel):  # Fixed: Basemodel -> BaseModel
    account_number: str = Field(..., example="123456789",
                              description="The unique account number")
    account_holder: str = Field(..., example="Hemant",
                                description="The name of the account holder")
    balance: float = Field(..., example=10000.59,
                           description="The initial balance of the account")
    account_type: str = Field(..., example='Savings',
                              description="Type of the account (e.g. Savings, Current)")

# Define the response model


class AccountResponse(BaseModel):  # Fixed: Basemodel -> BaseModel
    account_number: str
    message: str


# In-memory database for accounts
account_db = {}

#get (display), post (add new thing), put(update), delete - these are the methods used in FastAPI 

@app.get('/')
def home():
    return "status: is good"




@app.post('/account', response_model=AccountResponse)
def create_account(account: Account):
    if account.account_number in account_db:
        # Fixed: details -> detail
        raise HTTPException(status_code=400, detail="Account already exists")
    account_db[account.account_number] = account
    return {
        'account_number': account.account_number,
        'message': 'Account successfully created'
    }

@app.get('/account/{account_number}', response_model=Account )
def read_account(account_number:str = Path(..., description="the unique account number to be retrieved")):
    if account_number not in account_db:
        raise HTTPException(status_code=404, detail='account not found')
    return account_db[account_number]

@app.put('/account/{account_number}', response_model=AccountResponse)
def update_account(account_number:str, account :Account):
    if account_number not in account_db:
        raise HTTPException(status_code=404, detail='account not found')
    account_db[account_number] = account
    return {"account_number":account.account_number, "message": "Account successfully updated"}

@app.delete('/account/{accoount_number}', response_model = dict)
def delete_account(account_number:str):
    if account_number not in account_db:
        raise HTTPException(status_code=404, detail='account not found')
    del account_db[account_number]
    return {"message" : "account successfully deleted"}




def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()