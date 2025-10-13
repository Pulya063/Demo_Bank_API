from uuid import uuid4

from fastapi import HTTPException, APIRouter

from pydantic import BaseModel, field_validator
from datetime import datetime

class Account(BaseModel):
    name: str
    surname: str
    date: str
    balance: float = 0

    @field_validator('date')
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
            "balance": self.balance
        }
router = APIRouter(prefix="/accounts", tags=["Accounts"])

accounts: dict[str , Account] = {}

@router.post("/")
def create_account(account: Account):
    account_id = str(uuid4())
    accounts[account_id] = account
    # return print(json.dumps(account.show_info(account_id), indent=4)
    return account.show_info(account_id)

@router.get("/sort_by/")
def sort_by(by: str = "name" or float == 0, reverse: bool = True):
    if by not in Account.model_fields:
        raise HTTPException(status_code=404, detail = "Sort by field '{}' not found.")
        # return print("Sort by field '{}' not found.".format(by))
    sorted_list = sorted(accounts.items(), key=lambda x: getattr(x[1], by), reverse=reverse)
    for account_id, acc_info in sorted_list:
        # print(json.dumps(acc_info.show_info(account_id), indent=4))
        return acc_info.show_info(account_id)
    return sorted_list
@router.get("/search/")
def search_account(search_word: str):
    results = []
    for account_id, acc in accounts.items():
        acc_dict = acc.model_dump()
        for value in acc_dict.values():
            if search_word.lower() in str(value).lower():
                results.append(acc.show_info(account_id))
                break
    return results

@router.get("/show_accounts/")
def show_all_accounts():
    if accounts == {} or not accounts:
        raise HTTPException(status_code=404, detail="No accounts found")
        # print("No accounts found")
    else:
        for account_id, account in accounts.items():
            # print(json.dumps(account.show_info(account_id), indent=4))
            return account.show_info(account_id)
        return None

@router.get("/delete/")
def delete_account(account_id: str):
    if account_id in accounts:
        try:
            del accounts[account_id]
            # return    print(json.dumps(account.show_info(account_id), indent=4))
            for account_id, acc in accounts.items():
                return acc.show_info(account_id)
        except Exception:
            raise HTTPException(status_code=404, detail="Account deletion failed")
            # print("Account deletion failed")
    else:
        return None