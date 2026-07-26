from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels



from src.database import *


#print(f'settings = {settings.DB_URL}')


app = FastAPI()


app.include_router(router_auth)
app.include_router(router_hotels)



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)