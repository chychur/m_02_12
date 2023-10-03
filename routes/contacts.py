from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

from storage.models import get_db, User

from .schemas import ContactModel, ContactResponse
from repository import contacts as repository_contacts
from auth_service import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


# route for get contact list
@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0,
                        limit: int = 100,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


# route for get a contact by 'id'
@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


# route for create contact
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


# route for update contact
@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel,
                         contact_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


# route for delete contact
@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


# route for get contact list by first_name, last_name or email
@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(first_name: str = None,
                          last_name: str = None,
                          email: EmailStr = None,
                          phone: str = None,
                          address: str = None,
                          db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(first_name, last_name, email, phone, address, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


# route for get contact list with birthdays for the next 7 days
@router.get("/birthdays/", response_model=List[ContactResponse])
async def read_birthdays_contacts(start_date: date = date.today(),
                                  end_date: date = (date.today() + timedelta(days=7)),
                                  db: Session = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_birthday_contacts(start_date, end_date, current_user, db)
    if len(contacts) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts
