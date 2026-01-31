from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.wallet_routes import router as wallet_router
from app.routes.transaction_routes import router as transaction_router
from app.routes.transfer_routes import router as transfer_router
from app.routes.analytics_routes import router as analytics_router



app = FastAPI(title="Fintech Wallet Backend")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(transfer_router)
app.include_router(transaction_router)
app.include_router(analytics_router)




@app.get("/health")
def health_check():
    return {"status": "ok"}