from datetime import date, timedelta
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas.schemas import ContactModel, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> List[Contact]:
        stmt = select(Contact)

        if first_name:
            stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.where(Contact.email.ilike(f"%{email}%"))

        stmt = stmt.offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_upcoming_birthdays(self, days: int = 7) -> List[Contact]:
        stmt = select(Contact)
        contacts = await self.db.execute(stmt)
        today = date.today()
        end_date = today + timedelta(days=days - 1)

        upcoming_birthdays: List[Contact] = []

        for contact in contacts.scalars().all():
            next_birthday = self._get_next_birthday(contact.birthday, today)
            if today <= next_birthday <= end_date:
                upcoming_birthdays.append(contact)

        return upcoming_birthdays

    @staticmethod
    def _get_next_birthday(birthday: date, today: date) -> date:
        year = today.year

        try:
            next_birthday = birthday.replace(year=year)
        except ValueError:
            next_birthday = date(year, 2, 28)

        if next_birthday < today:
            try:
                next_birthday = birthday.replace(year=year + 1)
            except ValueError:
                next_birthday = date(year + 1, 2, 28)

        return next_birthday

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id)

    async def remove_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def replace_contact(
        self, contact_id: int, body: ContactModel
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump().items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def patch_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            for key, value in body.model_dump(
                exclude_unset=True, exclude_none=True
            ).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact
