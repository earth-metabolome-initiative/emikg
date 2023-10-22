# Common errors encountered during development

## API not responding
Sometimes, APIs were not responding simply because I had forgotten to export the APIs from the __init__.py file in the api folder. 

## No space left on device
If you get the following error:

```bash
OSError: [Errno 28] No space left on device
```

Then you can run the following command to free up space:

```bash
docker system prune -af
```

## Connection to server at "postgres_database" failed
When starting the dockers, it is possible that the postgres database is not ready yet. In that case, you will get the following error:

```bash
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "postgres_database" (172.24.0.2), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

In that case, you can simply restart the dockers after a few seconds and it should work.
