from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import sys
sys.path.append('./lib')
sys.path.append('./lib/models')
from app import api_app
# import DB
# import models
# from database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="main app")

app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="frontend", html=True), name="ui")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")