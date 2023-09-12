from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from storage.models import Contact
from .schemas import ContactCreate
from storage.models import get_db
from fastapi import APIRouter, Depends

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/birthday", response_model=List[ContactCreate])
def get_birthdays(days: int = 7, db: Session = Depends(get_db)):
    today = datetime.today().date()
    period = []
    for num in range(days):
        current_day = today + timedelta(days=num)
        period.append(current_day)
    #print(period)

    contacts = db.query(Contact).all()
    _contacts = []
    for contact in contacts:
        contact_date = contact.birthday.replace(year=today.year)
        #print(contact_date)
        if contact_date in period:
            _contacts.append(contact)
    return _contacts
