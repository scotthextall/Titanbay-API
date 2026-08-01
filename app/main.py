from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.database import Base, engine, get_db

# Create application object
app = FastAPI(title="Titanbay Private Markets API")

# Create Postgres tables
Base.metadata.create_all(bind=engine)

# GET /funds endpoint. Output as list of FundOut objects
@app.get("/funds", response_model=list[schemas.FundOut])
def list_funds(db: Session = Depends(get_db)):

    # Get every row from funds table via SQLAlchemy. Equivalent to SELECT * FROM funds
    return db.query(models.Fund).all()

# POST /funds endpoint. Payload is the validated FundCreate object. Use status_code 201 for successful creation
@app.post("/funds", response_model=schemas.FundOut, status_code=201)
def create_fund(payload: schemas.FundCreate, db: Session = Depends(get_db)):

    # Convert validated Pydantic object into SQLAlchemy object. ** unpacks dictionary into individual keyword arguments
    fund = models.Fund(**payload.model_dump())

    # Stages new fund then writes to Postgres
    db.add(fund)
    db.commit()

    # Reload object from database so automatically created values (id and created_at) are populated before returning fund
    db.refresh(fund)
    return fund

# PUT /funds endpoint. Payload is the validated FundUpdate object
@app.put("/funds", response_model=schemas.FundOut)
def update_fund(payload: schemas.FundUpdate, db: Session = Depends(get_db)):

    # Get fund from funds table in database based on fund id
    fund = db.get(models.Fund, payload.id)

    # If fund doesn't exist, raise error 404
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund Not Found")

    # Loop to update value of each field (except id) in-place on existing fund object
    for field, value in payload.model_dump(exclude={"id"}).items():
        setattr(fund, field, value)

    # Save in-place changes to Postgres. Refresh/reload before returning
    db.commit()
    db.refresh(fund)
    return fund

# GET /funds/{fund_id} endpoint
@app.get("/funds/{fund_id}", response_model=schemas.FundOut)
def get_fund(fund_id: UUID, db: Session = Depends(get_db)):

    # Get fund from funds table based on fund_id
    fund = db.get(models.Fund, fund_id)

    # Raise error 404 if fund doesn't exist
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund Not Found")
    return fund

# GET /investors endpoint
@app.get("/investors", response_model=list[schemas.InvestorOut])
def list_investors(db: Session = Depends(get_db)):

    # Get every row from investors table and output as list
    return db.query(models.Investor).all()

# POST /investors endpoint
@app.post("/investors", response_model=schemas.InvestorOut, status_code=201)
def create_investor(payload: schemas.InvestorCreate, db: Session = Depends(get_db)):
    investor = models.Investor(**payload.model_dump())

    # Stage new investor and write to Postgres. Email must be unique (see models.py). If duplicate, SQLAlchemy raises IntegrityError. Rollback failed transaction
    db.add(investor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="An investor with this email already exists")

    db.refresh(investor)
    return investor

# GET /funds/{fund_id}/investments endpoint
@app.get("/funds/{fund_id}/investments", response_model=list[schemas.InvestmentOut])
def list_investments(fund_id: UUID, db: Session = Depends(get_db)):

    # Get fund based on fund_id
    fund = db.get(models.Fund, fund_id)

    # If fund doesn't exist, raise error 404
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund Not Found")

    # Return every row from investments table belonging to fund_id, and output as list
    return db.query(models.Investment).filter(models.Investment.fund_id == fund_id).all()

# POST /funds/{fund_id}/investments endpoint
@app.post("/funds/{fund_id}/investments", response_model=schemas.InvestmentOut, status_code=201)
def create_investment(payload: schemas.InvestmentCreate, fund_id: UUID, db: Session = Depends(get_db)):
    fund = db.get(models.Fund, fund_id)
    if fund is None:
        raise HTTPException(status_code=404, detail="Fund Not Found")

    investor = db.get(models.Investor, payload.investor_id)
    if investor is None:
        raise HTTPException(status_code=404, detail="Investor Not Found")

    investment = models.Investment(fund_id=fund_id, **payload.model_dump())
    db.add(investment)
    db.commit()
    db.refresh(investment)
    return investment
