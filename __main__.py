from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from controllers import router
from fastapi.middleware.cors import CORSMiddleware
from init_db import create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="localhost", port=8080, reload=True, workers=1)
