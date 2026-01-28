from fastapi import FastAPI

app = FastAPI(title="Fintech Wallet Backend")

@app.get("/health")
def health_check():
    return {"status": "ok"}

