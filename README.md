# FastAPI

Let's create a REST API for storing and managing contacts. The API will be built using the FastAPI infrastructure and use SQLAlchemy for database management.

The contact model is given below:
```commandline
{
    "first_name": "string",
    "last_name": "string",
    "birthday": "2023-09-11",
    "email": "string",
    "phone": "string",
    "address": "string"
  }
```

The API has the ability to perform the following actions:

1. Create a new contact;
2. Get a list of all contacts;
3. Get one contact by ID;
4. Update an existing contact;
5. Delete the contact;
6. Contacts are available for search by name, surname, email, phone or address;
7. The API can retrieve a list of contacts with birthdays for the next 7 days.
