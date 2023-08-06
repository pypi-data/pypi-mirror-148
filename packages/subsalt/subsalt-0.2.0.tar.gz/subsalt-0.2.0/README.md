# Subsalt

Subsalt is a synthetic datastore that makes sensitive datasets shareable. This library provides an interface for retrieving data from Subsalt tables for use in other applications.

## Installation

```
pip install subsalt
```

## Usage

This library is a thin convenience wrapper around [psycopg2](https://pypi.org/project/psycopg2). psycopg2 or similar connectors can also be used directly if more flexibility is required.

**Note:** this library is currently in beta, and the interface may change significantly over time.

Retrieving data from Subsalt requires valid credentials. For access, contact the data owner or email `hello@getsubsalt.com`.

### Authentication

```python
client = subsalt.Client(
    username=os.getenv('SUBSALT_USERNAME'),
    password=os.getenv('SUBSALT_PASSWORD'),
)

# `client` can retrieve data on your behalf
```

### Retrieving data

```python
client = subsalt.Client(
    username=os.getenv('SUBSALT_USERNAME'),
    password=os.getenv('SUBSALT_PASSWORD'),
)

# Optional - get a list of tables you can access
for table in client.tables():
    print('{}.{}'.format(table.schema, table.table)

# Retrieve data via SQL
df = client.sql('select * from my_schema.my_table limit 250')
```