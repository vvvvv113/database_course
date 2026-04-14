# Homework6 Bookstore Database + Python CLI

This example creates a small bookstore database in SQLite and then uses Python to interact with it through a command-line interface created by Yiduo Lu.

## Files

- `createTables.sql` - creates the tables
- `insertRows.sql` - inserts sample categories and books
- `bookstore_cli.py` - Python CRUD program
- `bookstore.db` - database file you will create by running the commands below

## Create the database
Database file name is bookstore.db.
Run these commands in the terminal:

```bash
python3 - <<'PY'
import sqlite3
sqlite3.connect('bookstore.db').close()
PY
```

Then load the SQL files using SQLite in Python or DB Browser for SQLite.

If your environment has the `sqlite3` shell installed, you can run:

```bash
sqlite3 bookstore.db < createTables.sql
sqlite3 bookstore.db < insertRows.sql
```

## Run the Python CLI

```bash
python3 bookstore_cli.py
```
I add 3 extra functions:
9. Search books by author
10. View 'Read Now' books
11. Count books per category

## Notes

- This example uses parameterized queries in Python.
- The `image` field stores the filename only.
- The actual images can be reused later in the Flask web app.
