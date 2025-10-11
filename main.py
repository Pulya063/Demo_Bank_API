import json
from datetime import date, datetime
from typing import List

from eth_account import account
# import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from uuid import uuid4

# app = FastAPI(title="Bank Account Example")

class Account(BaseModel):
    name: str
    surname: str
    date: datetime
    balance: float = 0

    @field_validator('date')
    def parce_date(cls, value):
        if not value:
            # raise ValueError('Date cannot be empty')
            print("Date cannot be empty")
        if isinstance(value, date):
            return value
        try:
            value = value.strip().replace("'", "")
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            # raise ValueError('Date must be in format YYYY-MM-DD')
            print("Date must be in format YYYY-MM-DD")
        return value

    def show_info(self, account_id: str):
        return {
            "account_id": account_id,
            "name": self.name,
            "surname": self.surname,
            "date": self.date.strftime('%Y-%m-%d'),
            "balance": self.balance
        }


accounts: dict[str , Account] = {}


# @app.post("/accounts/")
def create_account(account: Account):
    try:
        account_id = str(uuid4())
        accounts[account_id] = account
        return print(json.dumps(account.show_info(account_id), indent=4))
    except Exception:
        print("Account creation failed")

# @app.get("/accounts/sort_by/")
def sort_by(by: str = "name" or float == 0, reverse: bool = True):
    if by not in Account.model_fields:
        # raise HTTPException(status_code=404, detail = "Sort by field '{}' not found.")
        return print("Sort by field '{}' not found.".format(by))
    sorted_list = sorted(accounts.items(), key=lambda x: getattr(x[1], by), reverse=reverse)
    for account_id, acc_info in sorted_list:
        print(json.dumps(acc_info.show_info(account_id), indent=4))
    return sorted_list
# @app.get("/accounts/search/")
def search_account(search_word: str):
    saccounts = []
    for account_id, acc in accounts.items():
        acc_dict = acc.model_dump()
        for value in acc_dict.values():
            if search_word.lower() in str(value).lower():
                saccounts.append(acc.show_info(account_id))
    if not saccounts:
        # raise HTTPException(status_code=404, detail="No accounts found")
        print("No accounts found")
    for acc_info in saccounts:
        print(json.dumps(acc_info, indent=4))

    return saccounts

# @app.get("/accounts/show_accounts/")
def show_all_accounts():
    if accounts == {} or not accounts:
        # raise HTTPException(status_code=404, detail="No accounts found")
        print("No accounts found")
    else:
        for account_id, account in accounts.items():
            print(json.dumps(account.show_info(account_id), indent=4))

# @app.get("/accounts/delete/")
def delete_account(account_id: str):
    if account_id in accounts:
        try:
            del accounts[account_id]
            return print(json.dumps(account.show_info(account_id), indent=4))
        except Exception:
            # raise HTTPException(status_code=404, detail="Account deletion failed")
            print("Account deletion failed")
    else:
        return None


# def main():
#     uvicorn.run("main:app", host="127.0.0.1", port=8909, reload=True)
#
#
# if __name__ == "__main__":
#     main()


def main():
    while True:
        print("\nКоманди: create, search, show, exit")
        cmd = input(">>> ").lower()
        if cmd == "create":
            try:
                name, surname, date_str, balance = input(
                    "Input data to create an account(name, surname, date, balance): ").split(',')
                account = Account(
                    name=name.strip(),
                    surname=surname.strip(),
                    date=date_str.strip(),
                    balance=float(balance.strip())
                )
                result = create_account(account)
                print("✅ Account created:")
            except ValueError:
                print("Invalid input")
            except TypeError:
                print("Invalid input")
            except Exception as e:
                print(e)
        elif cmd == "search":
            src = input("Input what do you want to search: ")
            search_account(src)
        elif cmd == "show":
            show_all_accounts()
        elif cmd == "sort_by":
            inp = input("Input what you want to sort by: ")
            rev = input("What is the reverse order? ")
            inp = inp.lower()
            sort_by(inp, rev)
        elif cmd == "exit":
            print("👋 Вихід...")
            break
        else:
            print("❌ Невідома команда")

if __name__ == "__main__":
    main()
