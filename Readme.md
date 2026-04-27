# Contacts API (FastAPI + PostgreSQL)

## 1. Configure environment

Create a local `.env` file (you can copy from `.env.example`) and set the database URL:

```env
DB_URL=postgresql+asyncpg://postgres:12345@localhost:5432/contacts_app
```

## 2. Start PostgreSQL in Docker

Run PostgreSQL with automatic creation of the `contacts_app` database:

```bash
docker run --name contacts-postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=contacts_app -d postgres
```

`POSTGRES_DB=contacts_app` ensures the expected database exists at container startup.

## 3. Run migrations

```bash
alembic upgrade head
```

## 4. Seed demo data

Run the seed script to populate the database with a small demo dataset:

```powershell
.\seed_db.ps1
```

The seed script is idempotent: if contacts already exist, it skips inserting demo rows.

## 5. Start application

```bash
uvicorn main:app --reload
```

## API notes

- `GET /api/contacts/` supports filtering with query parameters `first_name`, `last_name`, and `email`.
- `GET /api/contacts/birthdays` returns contacts with birthdays in the next 7 days.
