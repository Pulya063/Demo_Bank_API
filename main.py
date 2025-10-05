from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

class Item(BaseModel):
    name: str
    id: int

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return {"request": request, "message": "Привіт, FastAPI!"}
