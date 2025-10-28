from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import jwt
from datetime import datetime, timedelta

from services import AuthService, BankingService, PortfolioService
from repositories import ClientRepository, BankCardRepository, InsuranceRepository

app = FastAPI(title="Banking System API", version="1.0.0")
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

# Pydantic Models
class ClientCreate(BaseModel):
    c_name: str
    c_mail: str
    c_id_card: str
    c_phone: str
    c_password: str
    c_address: Optional[str] = None

class BankCardCreate(BaseModel):
    b_number: str
    b_type: str
    b_c_id: int
    b_expiry_date: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class TransferRequest(BaseModel):
    from_card: str
    to_card: str
    amount: float
    description: str

class InsurancePurchase(BaseModel):
    purchase_date: str
    premium_amount: float
    coverage_period: int

# Utility Functions
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Authentication Endpoints
@app.post("/api/auth/login")
async def login(login_data: LoginRequest):
    client = AuthService.verify_client(login_data.email, login_data.password)
    if not client:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token({"c_id": client.c_id, "email": client.c_mail})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/auth/register")
async def register(client_data: ClientCreate):
    try:
        client_id = ClientRepository.create_client(client_data.dict())
        return {"message": "Client registered successfully", "client_id": client_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Client Management Endpoints
@app.get("/api/clients", dependencies=[Depends(verify_token)])
async def get_all_clients():
    clients = ClientRepository.get_all_clients()
    return clients

@app.get("/api/clients/{c_id}", dependencies=[Depends(verify_token)])
async def get_client_by_id(c_id: int):
    client = ClientRepository.get_client_by_id(c_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/api/clients/{c_id}", dependencies=[Depends(verify_token)])
async def update_client(c_id: int, client_data: ClientCreate):
    ClientRepository.update_client(c_id, client_data.dict())
    return {"message": "Client updated successfully"}

# Bank Card Endpoints
@app.get("/api/bank-cards/client/{c_id}", dependencies=[Depends(verify_token)])
async def get_client_cards(c_id: int):
    cards = BankCardRepository.get_cards_by_client(c_id)
    return cards

@app.post("/api/bank-cards", dependencies=[Depends(verify_token)])
async def create_bank_card(card_data: BankCardCreate):
    BankCardRepository.create_card(card_data.dict())
    return {"message": "Bank card created successfully"}

# Insurance Endpoints
@app.get("/api/insurances")
async def get_all_insurances():
    insurances = InsuranceRepository.get_all_insurances()
    return insurances

@app.get("/api/insurances/{i_id}")
async def get_insurance_by_id(i_id: int):
    insurance = InsuranceRepository.get_insurance_by_id(i_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance

@app.post("/api/insurances/{i_id}/purchase", dependencies=[Depends(verify_token)])
async def purchase_insurance(i_id: int, purchase_data: InsurancePurchase, token: dict = Depends(verify_token)):
    client_id = token.get("c_id")
    InsuranceRepository.purchase_insurance(client_id, i_id, purchase_data.dict())
    return {"message": "Insurance purchased successfully"}

# Transaction Endpoints
@app.post("/api/transactions/transfer", dependencies=[Depends(verify_token)])
async def transfer_funds(transfer_data: TransferRequest):
    success, message = BankingService.transfer_funds(
        transfer_data.from_card,
        transfer_data.to_card,
        transfer_data.amount,
        transfer_data.description
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@app.get("/api/transactions/{c_id}", dependencies=[Depends(verify_token)])
async def get_client_transactions(c_id: int):
    transactions = TransactionRepository.get_client_transactions(c_id)
    return transactions

# Portfolio Endpoints
@app.get("/api/portfolio/{c_id}", dependencies=[Depends(verify_token)])
async def get_client_portfolio(c_id: int):
    portfolio = PortfolioService.get_client_portfolio(c_id)
    return portfolio

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
