from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.schemas import (
    # ContactBase,
    ContactResponse,
    ContactUpdate,
    # ContactCreate,
    ContactModel,
)
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])
CONTACT_NOT_FOUND = "Contact not found"


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(
        skip=skip,
        limit=limit,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    return contacts


@router.get("/birthdays", response_model=List[ContactResponse])
async def read_upcoming_birthdays(days: int = 7, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.get_upcoming_birthdays(days)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=CONTACT_NOT_FOUND
        )
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def patch_contact(
    body: ContactUpdate, contact_id: int, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=CONTACT_NOT_FOUND
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=CONTACT_NOT_FOUND
        )
    return contact
