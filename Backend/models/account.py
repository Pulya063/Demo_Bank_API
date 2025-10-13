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