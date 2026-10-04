from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "OT Security Platform API  is running"}

