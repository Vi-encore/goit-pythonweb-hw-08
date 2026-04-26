To start a docker container with postgres use

```
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres

```

### Contacts API

- `GET /api/contacts/` supports filtering with query parameters `first_name`, `last_name`, and `email`.
- `GET /api/contacts/birthdays` returns contacts with birthdays in the next 7 days.
