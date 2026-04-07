from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Deployment-ready GA2 app"}

@app.get("/health")
async def health():
    return {"status": "ok"}
