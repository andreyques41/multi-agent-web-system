from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.models import User, Lead
from backend.app.database import get_db

router = APIRouter()

@router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # Example registration logic
    hashed_password = password  # Replace with actual hashing
    new_user = User(username=username, email=email, hashed_password=hashed_password, created_at=datetime.utcnow())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user": new_user}

@router.post("/generate-lead")
def generate_lead(user_id: int, name: str, email: str, phone: str, message: str, db: Session = Depends(get_db)):
    new_lead = Lead(user_id=user_id, name=name, email=email, phone=phone, message=message, created_at=datetime.utcnow())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return {"message": "Lead generated successfully", "lead": new_lead}

@router.get("/leads")
def get_leads(user_id: int, db: Session = Depends(get_db)):
    leads = db.query(Lead).filter(Lead.user_id == user_id).all()
    return {"leads": leads}