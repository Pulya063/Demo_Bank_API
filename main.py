from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from sqlalchemy import create_engine
from uuid import uuid4
app = FastAPI(title="Bank Account Example")

# Модель рахунку
class Account(BaseModel):
    name: str
    surname: str
    date: str = None
    balance: float = 0

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%m/%d/%Y")
        except ValueError:
            raise ValueError("Date must be in MM/DD/YYYY format")
        return v
    def show_info(self):
        return {_ for _ in self}

# Словник для збереження рахунків в пам'яті
accounts = {}

# --- GET: отримати інформацію про рахунок ---
@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.show_info()

# --- POST: створити новий рахунок ---
@app.post("/accounts/")
def create_account(account: Account):
    account_id = str(uuid4())  # генеруємо унікальний ID
    accounts[account_id] = account
    return {"account_id": account_id, "owner": account.owner, "balance": account.balance}

def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8008, reload=True)


if __name__ == "__main__":
    main()


