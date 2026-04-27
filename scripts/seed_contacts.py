from __future__ import annotations

import asyncio
from datetime import date

from sqlalchemy import select

from src.database.db import sessionmanager
from src.database.models import Contact


SEED_CONTACTS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+380501112233",
        "birthday": date(1990, 5, 14),
        "additional_data": "Seed contact 1",
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+380501112234",
        "birthday": date(1992, 8, 22),
        "additional_data": "Seed contact 2",
    },
    {
        "first_name": "Alex",
        "last_name": "Brown",
        "email": "alex.brown@example.com",
        "phone": "+380501112235",
        "birthday": date(1988, 1, 9),
        "additional_data": "Seed contact 3",
    },
    {
        "first_name": "Maria",
        "last_name": "Johnson",
        "email": "maria.johnson@example.com",
        "phone": "+380501112236",
        "birthday": date(1995, 11, 30),
        "additional_data": "Seed contact 4",
    },
    {
        "first_name": "Oleh",
        "last_name": "Koval",
        "email": "oleh.koval@example.com",
        "phone": "+380501112237",
        "birthday": date(1987, 3, 3),
        "additional_data": "Seed contact 5",
    },
]


async def seed_contacts() -> None:
    async with sessionmanager.session() as session:
        existing_contact = await session.scalar(select(Contact.id).limit(1))

        if existing_contact is not None:
            print("Seed skipped: contacts already exist.")
            return

        session.add_all(
            Contact(**contact_data) for contact_data in SEED_CONTACTS
        )
        await session.commit()
        print(f"Seed completed: inserted {len(SEED_CONTACTS)} contacts.")


if __name__ == "__main__":
    asyncio.run(seed_contacts())
