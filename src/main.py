
import uvicorn
from fastapi import FastAPI

# from src.cache.router import router as cache_router
# from src.games.router import router as games_router
# from src.providers.router import router as providers_router
from src.user.router import router as user_router
from src.user.auth.router import router as auth_router

app = FastAPI()
# app.include_router(cache_router)
# app.include_router(games_router)
# app.include_router(providers_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/", tags=["TEST"])
def home_page():
    return {"msg": "Alles ist gut"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)  #
