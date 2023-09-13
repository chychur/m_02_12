from faker import Faker

from db import session
from models import Contact, User

fake = Faker('en_US')

ONE = 1
NUMBER_CONTACTS = 10 + ONE
NUMBER_USERS = 3 + ONE


def create_contact(number_contacts):
    for _ in range(ONE, number_contacts):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthday=fake.date_between(),
            email=fake.ascii_free_email(),
            phone=fake.phone_number(),
            address=fake.address()
        )
        session.add(contact)
    session.commit()


def create_user(number_users):
    for _ in range(ONE, number_users):
        contact = User(
            email=fake.ascii_free_email(),
            password=fake.password(
                length=10,
                digits=True,
                special_chars=True,
                upper_case=True
            )
        )
        session.add(contact)
    session.commit()


if __name__ == '__main__':
    create_contact(NUMBER_CONTACTS)
    create_user(NUMBER_USERS)
