from fastapi import FastAPI
import uvicorn

from app.api.endpoints.users import auth
from app.api.endpoints.currency import currency
from app.db.database import Base


app = FastAPI()
app.include_router(auth)
app.include_router(currency)

if __name__ == '__main__':
    uvicorn.run(app)    

   