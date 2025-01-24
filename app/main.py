from fastapi import FastAPI
from app.routers import task
from app.routers import user

app = FastAPI()



@app.get("/main")
async def root():
    return {"message": "Привет я твой друг"}

app.include_router(user.router)
app.include_router(task.router)