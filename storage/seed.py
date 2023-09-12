from faker import Faker

from db import session
from models import Contact

fake = Faker('en_US')

ONE = 1
NUMBER_CONTACTS = 10 + ONE


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


if __name__ == '__main__':
    create_contact(NUMBER_CONTACTS)
