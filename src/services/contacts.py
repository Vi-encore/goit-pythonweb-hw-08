from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.schemas import ContactModel, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel):
        return await self.contact_repository.create_contact(body)

    async def get_contacts(
        self,
        skip: int,
        limit: int,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ):
        return await self.contact_repository.get_contacts(
            skip, limit, first_name, last_name, email
        )

    async def get_upcoming_birthdays(self, days: int = 7):
        return await self.contact_repository.get_upcoming_birthdays(days)

    async def get_contact(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def update_contact(
        self, contact_id: int, body: ContactModel | ContactUpdate
    ):
        return await self.contact_repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        return await self.contact_repository.remove_contact(contact_id)
