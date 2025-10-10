from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI(title="Bank Account Example")

class Account(BaseModel)
    owner: str
    balance: float = 0

accounts = {}

@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "owner": account.owner, "balance": account.balance}

@app.post("/accounts/")
def create_account(account: Account):
    account_id = str(uuid4())
    accounts[account_id] = account
    return {"account_id": account_id, "owner": account.owner, "balance": account.balance}

@app.post("/accounts/update_balance/{accounts_id}")
def update_balance(accounts_id: str, new_balance: float):
    try:
        accounts[accounts_id].balance = new_balance
    except KeyError:
        return HTTPException(status_code=404, detail="Account not found")
    return {"account": accounts_id, "old_balance": accounts[accounts_id].balance, "balance": new_balance}

