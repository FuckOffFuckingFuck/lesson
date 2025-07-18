import uvicorn
from fastapi import FastAPI

from app.users.auth.router import router as auth_router
from app.users.router import router as user_router


app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
async def mainpage():
    return {"message": "mainpage"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)  # , host="0.0.0.0", port=8000
