# app/api/v1/router.py
from fastapi import APIRouter
#from app.api.v1 import accounts, transactions, auth

api_router = APIRouter()

#api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
#api_router.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
#api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
