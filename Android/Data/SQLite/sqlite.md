# SQLite Interview Questions (Basic & Advanced)

## Basic Questions

### 1. What is SQLite?
**Answer:**  
SQLite is a lightweight, serverless, self-contained SQL database engine. It is embedded into applications and does not require a separate server process.

---

### 2. How do you create a table in SQLite?
**Answer:**  
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);
```

---

### 3. How do you insert data into a table?
**Answer:**  
```sql
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
```

---

### 4. How do you query data from a table?
**Answer:**  
```sql
SELECT * FROM users;
```

---

### 5. What data types does SQLite support?
**Answer:**  
SQLite supports: `NULL`, `INTEGER`, `REAL`, `TEXT`, and `BLOB`.

---

### 6. How do you update data in SQLite?
**Answer:**  
```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
```

---

### 7. How do you delete data from a table?
**Answer:**  
```sql
DELETE FROM users WHERE id = 1;
```

---

### 8. How do you add a new column to an existing table?
**Answer:**  
```sql
ALTER TABLE users ADD COLUMN age INTEGER;
```

---

### 9. What is a primary key in SQLite?
**Answer:**  
A primary key uniquely identifies each row in a table. In SQLite, it is often an `INTEGER PRIMARY KEY`.

---

### 10. How do you prevent SQL injection in SQLite?
**Answer:**  
Use parameterized queries or prepared statements.

---

## Advanced Questions

### 11. How do you create an index in SQLite?
**Answer:**  
```sql
CREATE INDEX idx_users_email ON users(email);
```

---

### 12. What is a transaction in SQLite?
**Answer:**  
A transaction is a sequence of operations performed as a single logical unit of work.  
```sql
BEGIN TRANSACTION;
-- SQL statements
COMMIT;
```

---

### 13. How do you perform a JOIN in SQLite?
**Answer:**  
```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
```

---

### 14. How do you use triggers in SQLite?
**Answer:**  
```sql
CREATE TRIGGER update_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

---

### 15. How do you handle foreign keys in SQLite?
**Answer:**  
Enable foreign keys:  
```sql
PRAGMA foreign_keys = ON;
```
Define foreign key:  
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

---

### 16. How do you backup an SQLite database?
**Answer:**  
Copy the database file (`.db` or `.sqlite`) to a backup location.

---

### 17. How do you optimize performance in SQLite?
**Answer:**  
- Use indexes
- Avoid unnecessary columns
- Use transactions for batch inserts

---

### 18. How do you check the SQLite version?
**Answer:**  
```sql
SELECT sqlite_version();
```

---

### 19. How do you store binary data in SQLite?
**Answer:**  
Use the `BLOB` data type.

---

### 20. How do you handle concurrency in SQLite?
**Answer:**  
SQLite uses locks to handle concurrency. For high concurrency, consider WAL (Write-Ahead Logging) mode:  
```sql
PRAGMA journal_mode = WAL;
```

---

### 21. How do you drop a table in SQLite?
**Answer:**  
```sql
DROP TABLE users;
```

---

### 22. How do you export data from SQLite to CSV?
**Answer:**  
Using the SQLite CLI:  
```
.mode csv
.output users.csv
SELECT * FROM users;
```

---

### 23. How do you use prepared statements in SQLite (with Python)?
**Answer:**  
```python
import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Bob', 'bob@example.com'))
conn.commit()
```

---

### 24. How do you handle NULL values in SQLite?
**Answer:**  
Use `IS NULL` or `IS NOT NULL` in queries:  
```sql
SELECT * FROM users WHERE email IS NULL;
```

---

### 25. How do you rename a table in SQLite?
**Answer:**  
```sql
ALTER TABLE users RENAME TO customers;
```

---
