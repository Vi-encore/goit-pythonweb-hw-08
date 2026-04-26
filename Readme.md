To start a docker container with postgres use

```
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=12345 -d postgres

```
