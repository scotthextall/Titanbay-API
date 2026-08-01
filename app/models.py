"""Describes tables that exist in the database such as columns, and relationships"""

import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, Integer, Numeric, DateTime, Date, ForeignKey, Uuid
from sqlalchemy.orm import relationship

from app.database import Base


class Fund(Base):
    __tablename__ = "funds"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    vintage_year = Column(Integer, nullable=False)
    target_size_usd = Column(Numeric(18, 2), nullable=False)

    # Newly created fund defaults to "Fundraising" status
    status = Column(String, nullable=False, default="Fundraising")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship between investments to the fund they are in
    investments = relationship("Investment", back_populates="fund")


class Investor(Base):
    __tablename__ = "investors"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    investor_type = Column(String, nullable=False)

    # Investor email must be unique - i.e. no duplicates in table
    email = Column(String, nullable=False, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship between investments and investors
    investments = relationship("Investment", back_populates="investor")


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)

    # Match investor_id and fund_id to id from investors and funds table respectively
    investor_id = Column(Uuid, ForeignKey("investors.id"), nullable=False)
    fund_id = Column(Uuid, ForeignKey("funds.id"), nullable=False)

    amount_usd = Column(Numeric(18, 2), nullable=False)
    investment_date = Column(Date, default=date.today, nullable=False)

    # Relationship between investments and funds/investors
    fund = relationship("Fund", back_populates="investments")
    investor = relationship("Investor", back_populates="investments")