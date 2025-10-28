from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Client:
    c_id: int
    c_name: str
    c_mail: str
    c_id_card: str
    c_phone: str
    c_password: str
    c_address: Optional[str] = None

@dataclass
class BankCard:
    b_number: str
    b_type: str
    b_c_id: int
    b_expiry_date: Optional[str] = None

@dataclass
class Insurance:
    i_id: int
    i_name: str
    i_amount: float
    i_person: str
    i_year: int
    i_project: str
    i_provider: Optional[str] = None

@dataclass
class FinanceProduct:
    p_id: int
    p_name: str
    p_description: str
    p_amount: float
    p_year: int
    p_risk_assessment: Optional[str] = None

@dataclass
class Fund:
    f_id: int
    f_name: str
    f_type: str
    f_amount: float
    risk_level: str
    f_manager: int
    f_benchmark: Optional[str] = None

@dataclass
class Property:
    pro_id: int
    pro_type: str
    pro_status: str
    pro_quantity: int
    pro_income: float
    pro_location: Optional[str] = None

@dataclass
class Transaction:
    transaction_id: int
    from_card: str
    to_card: str
    amount: float
    transaction_date: str
    description: str
