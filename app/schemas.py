"""Describes what is allowed to go through API - i.e. what requests and responses must look like"""

from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# Define required FundStatus and InvestorType values
FundStatus = Literal["Fundraising", "Investing", "Closed"]
InvestorType = Literal["Individual", "Institution", "Family Office"]

# Define POST /funds request body. id and created_at not required as server generates these values
class FundCreate(BaseModel):
    name: str
    # Vintage year must be between 1900 and 2100 (decision made)
    vintage_year: int = Field(ge=1900, le=2100)
    # Target size must be >0
    target_size_usd: Decimal = Field(gt=0)
    # Decided to default to Fundraising status for a newly created fund
    status: FundStatus = "Fundraising"

# Define PUT /funds request body
class FundUpdate(FundCreate):
    id: UUID

# Define server response body
class FundOut(FundCreate):
    # Allows Pydantic to build object from SQLAlchemy model attributes - e.g. fund.name, fund.id, fund.vintage_year etc. Without this, can only build using dictionary
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime

# Define POST /investors request body
class InvestorCreate(BaseModel):
    name: str
    investor_type: InvestorType
    email: str

# Define server response body
class InvestorOut(InvestorCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime

# Define POST /funds/{fund_id}/investments request body
class InvestmentCreate(BaseModel):
    investor_id: UUID
    amount_usd: Decimal = Field(gt=0)
    investment_date: date

# Define server response body
class InvestmentOut(InvestmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    fund_id: UUID