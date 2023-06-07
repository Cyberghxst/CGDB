# CGDB
A simple tabled-based database with a key-value interface.

## Setup
```python
# New instance
db = CGDB("./database", ["core", "public"])
# Set
db.set(key="GREET", value="Hello world!", table="core")
# Get
greet = db.get(key="GREET", table="core")
print(greet) # "Hello world!"
# All
all = db.all(table="core")
print(all) # [{'key': 'GREET', 'value': 'Hello world!'}]
# Delete
db.delete(key="GREET", table="core")
```

### Options
There are two types of CGDB built with SQLITE or JSON. <br>
for JSON, import `json.py` <br>
for SQLITE3, import `sqlite.py`