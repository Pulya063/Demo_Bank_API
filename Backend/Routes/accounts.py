from uuid import uuid4
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, field_validator
from datetime import datetime

class Account(BaseModel):
    name: str
    surname: str
    date: str
    balance: float = 0

    @field_validator("date")
    def validate_date(cls, value):
        if not value:
            raise ValueError("Date cannot be empty")
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in format YYYY-MM-DD")
        return value

    def show_info(self, account_id: str) -> dict:
        return {
            "account_id": account_id,
            "name": self.name,
            "surname": self.surname,
            "date": self.date,
            "balance": self.balance,
        }

router = APIRouter(prefix="/accounts", tags=["Accounts"])
accounts: dict[str, Account] = {}

@router.post("/")
def create_account(account: Account):
    account_id = str(uuid4())
    accounts[account_id] = account
    return account.show_info(account_id)

@router.get("/show_accounts/")
def show_all_accounts():
    if not accounts:
        return {"message": "No accounts found", "data": []}
    return [acc.show_info(aid) for aid, acc in accounts.items()]

@router.get("/sort_by/")
def sort_by(by: str = "name", reverse: bool = True):
    if by not in Account.model_fields:
        raise HTTPException(status_code=404, detail=f"Sort by field '{by}' not found.")
    sorted_list = sorted(accounts.items(), key=lambda x: getattr(x[1], by), reverse=reverse)
    return [acc.show_info(aid) for aid, acc in sorted_list]

@router.get("/search/{search_word}")
def search_account(search_word: str):
    results = []
    for account_id, acc in accounts.items():
        acc_dict = acc.model_dump()
        if any(search_word.lower() in str(v).lower() for v in acc_dict.values()):
            results.append(acc.show_info(account_id))
    return results

@router.put("/change_all_danes/{account_id}")
def change_all_dane(account_id: str, account: Account):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
    accounts[account_id] = account
    return {"updated": account_id, "data": account.show_info(account_id)}

@router.delete("/delete/{account_id}")
def delete_account(account_id: str):
    if account_id not in accounts:
        raise HTTPException(status_code=404, detail="Account not found")
    del accounts[account_id]
    return [acc.show_info(aid) for aid, acc in accounts.items()]
