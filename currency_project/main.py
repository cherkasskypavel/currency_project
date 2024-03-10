from fastapi import FastAPI
from app.api.endpoints.users import auth
import uvicorn


app = FastAPI()
app.include_router(auth)

if __name__ == '__main__':
    uvicorn.run(app)