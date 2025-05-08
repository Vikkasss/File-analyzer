from fastapi import FastAPI
from .routers import router
from .database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)