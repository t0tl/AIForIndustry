## Postgres instance with PgAdmin
This example shows how to run a Postgres instance with PgAdmin.

Let's start by creating a network for our containers to communicate with each other.

```bash
docker network create pg-network
```

We also need to create a volume for our Postgres data. This is so that we can persist the data even if the container is removed.

```bash
docker volume create pgdata
```

```bash
docker run -d \
  --name dev-postgres \
  --network pg-network \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

Now we can run the PgAdmin container.

```bash
docker run -d \
  --name dev-pgadmin \
  --network pg-network \
  -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' \
  -e 'PGADMIN_DEFAULT_PASSWORD=admin' \
  -p 80:80 \
  dpage/pgadmin4
```

Let's navigate to `http://localhost` and login with the email and password we set above. We can now add a new server and connect to our Postgres instance. The server address is the name of the container running postgres as they are on the same network, the username `postgres` and the password is `mysecretpassword`.

Let's stop and remove the containers.

```bash
docker stop dev-postgres dev-pgadmin
docker rm dev-postgres dev-pgadmin
```

And remove the network and volume. (this will remove all data stored in the volume)

```bash
docker network rm pg-network
docker volume rm pgdata
```

Quite annoying to type all these commands right?

Let's checkout the `docker-compose.yml` file to learn how to make this easier. 

With the docker-compose file, we can start the containers with a single command.
```bash
docker-compose up -d
```

And stop them with another single command.
```bash
docker-compose down
```

Try querying the stat_activity table to see previous queries to database. Go to Tools -> Query Tool and run the following query.
```SQL
SELECT * FROM pg_stat_activity
```