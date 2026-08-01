"""Seed script to add sample data for running locally"""

from app.database import Base, SessionLocal, engine
from app.models import Fund, Investor, Investment
from datetime import date

# Create Postgres tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

fund = Fund(
    name="Titanbay Growth Fund I",
    vintage_year=2024,
    target_size_usd=250000000,
    status="Investing",
)
db.add(fund)

# Send pending changes to Postgres as investment requires fund.id
db.flush()

investor = Investor(
    name="CalPERS",
    investor_type="Institution",
    email="seed@calpers.ca.gov",
)
db.add(investor)

# Send pending changes to Postgres as investment requires investor.id
db.flush()

investment = Investment(
    fund_id=fund.id,
    investor_id=investor.id,
    amount_usd=50000000,
    investment_date=date(2024, 6, 1),
)
db.add(investment)

db.commit()
db.close()

print("Seed data created.")