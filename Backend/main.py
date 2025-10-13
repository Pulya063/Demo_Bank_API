import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from Routes import accounts
from starlette.responses import Response

app = FastAPI(title="Bank Account JSON API")
app.include_router(accounts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",  "http://192.168.1.108:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ Incoming: {request.method} {request.url}")
    response: Response = await call_next(request)
    print(f"⬅️ Outgoing: {response.status_code}")
    response.headers["X-Custom-Header"] = "MyValue"
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=2103, reload=True)

# def main():
#     while True:
#         print("\nКоманди: create, search, show, exit")
#         cmd = input(">>> ").lower()
#         if cmd == "create":
#             try:
#                 name, surname, date_str, balance = input(
#                     "Input data to create an account(name, surname, date, balance): ").split(',')
#                 account = Account(
#                     name=name.strip(),
#                     surname=surname.strip(),
#                     date=date_str.strip(),
#                     balance=float(balance.strip())
#                 )
#                 result = create_account(account)
#                 print("✅ Account created:")
#             except ValueError:
#                 print("Invalid input")
#             except TypeError:
#                 print("Invalid input")
#             except Exception as e:
#                 print(e)
#         elif cmd == "search":
#             src = input("Input what do you want to search: ")
#             search_account(src)
#         elif cmd == "show":
#             show_all_accounts()
#         elif cmd == "sort_by":
#             inp = input("Input what you want to sort by: ")
#             rev = input("What is the reverse order? ")
#             inp = inp.lower()
#             sort_by(inp, rev)
#         elif cmd == "exit":
#             print("👋 Вихід...")
#             break
#         else:
#             print("❌ Невідома команда")
#
# if __name__ == "__main__":
#     main()
