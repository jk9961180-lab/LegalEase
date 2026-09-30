from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LegalEase API is running"}

@app.get("/api")
def get_api():
    return {"status": "API ready"}
