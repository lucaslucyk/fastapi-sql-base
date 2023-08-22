from fastapi import FastAPI
from api.v1.routers import users

app = FastAPI()


@app.get('/')
async def home():
    return {'ping': 'pong'}


app.include_router(users.router, prefix="/users")