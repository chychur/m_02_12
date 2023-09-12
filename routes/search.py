from typing import List

from sqlalchemy.orm import Session
from storage.models import Contact
from .schemas import ContactCreate
from storage.models import get_db
from fastapi import HTTPException, status, APIRouter, Depends

router = APIRouter(prefix='/contacts', tags=["Search"])


@router.get("/search/", response_model=List[ContactCreate])
async def search_contacts(
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        db: Session = Depends(get_db)
        ) -> List[Contact]:
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name == first_name)
        contacts = query.all()
    elif last_name:
        query = query.filter(Contact.last_name == last_name)
        contacts = query.all()
    elif email:
        query = query.filter(Contact.email == email)
        contacts = query.all()
    elif phone:
        query = query.filter(Contact.phone == phone)
        contacts = query.all()
    elif address:
        query = query.filter(Contact.address == address)
        contacts = query.all()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    if query:
        return contacts
    else:
        return []




    #query = db.query(Contact)
    #print(query)
    # _contacts = []
    # for contact in contacts:
    #     print(contact.__dict__.values())
    #     print(type(user_input))
#     if search:
#         query = query.filter(Contact.first_name == search)
#         contacts = query.all()
#
#
#
#         # if str(user_input) in contact.__dict__.values():
#         #     print(contact)
#         #     _contacts.append(contact)
#         # else:
#         #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
#
#     return contacts
#
#
# @router.put("/{contact_id}", response_model=ContactCreate)
# async def update_contact(body: ContactCreate, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
#     if contact:
#         contact.first_name = body.first_name
#         contact.last_name = body.last_name
#         contact.email = body.email
#         contact.phone = body.phone
#         contact.birthday = body.birthday
#         contact.address = body.address
#         db.commit()
#     return contact

