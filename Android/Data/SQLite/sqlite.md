# 🗃️ SQLite Interview Questions
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Raw SQLite is rarely used in modern Android; Room is preferred. However, understanding SQL internals is critical.

![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQL-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Basics & Key Concepts](#-basic-questions)
- [2. Advanced Operations](#-advanced-questions)
- [3. Transactions & Concurrency](#-12-what-is-a-transaction-in-sqlite)
- [4. Performance & Optimization](#-17-how-do-you-optimize-performance-in-sqlite)

---

## 🟢 Basic Questions

### 1. What is SQLite?
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. It makes it easier to store data in a structured manner.

### 2. What are the storage classes in SQLite?
SQLite uses a dynamic typing system with five storage classes:
- **NULL**: The value is a NULL value.
- **INTEGER**: A signed integer.
- **REAL**: A floating point value.
- **TEXT**: A text string.
- **BLOB**: A blob of data, stored exactly as it was input.

### 3. How do you access a database in Android using SQLite?
Android provides the `SQLiteOpenHelper` class to manage database creation and version management. You extend this class and override `onCreate()` and `onUpgrade()`.

### 4. What is the role of SQLiteOpenHelper?
`SQLiteOpenHelper` is a helper class to manage database creation and version management. It provides `getReadableDatabase()` and `getWritableDatabase()` methods to access the database.

### 5. How do you insert data into an SQLite database?
Use the `insert()` method of the `SQLiteDatabase` class, passing the table name and a `ContentValues` object containing the data.

### 6. How do you query data from an SQLite database?
Use the `query()` or `rawQuery()` methods of the `SQLiteDatabase` class. `query()` provides a structured interface, while `rawQuery()` accepts a raw SQL query string.

### 7. What is a Cursor in Android SQLite?
A `Cursor` is an interface that provides random read-write access to the result set returned by a database query. It points to a single row of the result set at a time.

### 8. How do you update data in an SQLite database?
Use the `update()` method of the `SQLiteDatabase` class, specifying the table name, `ContentValues` with new data, and a `WHERE` clause to identify the rows to update.

### 9. How do you delete data from an SQLite database?
Use the `delete()` method of the `SQLiteDatabase` class, specifying the table and a `WHERE` clause to identify the rows to delete.

### 10. What is a Content Provider in relation to SQLite?
A Content Provider abstracts the underlying data storage (often SQLite) and provides a mechanism to share data between applications securely.

---

## 🟠 Advanced Questions

### 11. How do you handle database upgrades in SQLiteOpenHelper?
Override `onUpgrade()` method. Typically, you alter tables or drop and recreate them, then migrate data if necessary.

### 12. What is a transaction in SQLite?
A transaction is a sequence of operations performed as a single logical unit of work. In Android, use `beginTransaction()`, `setTransactionSuccessful()`, and `endTransaction()`.

### 13. Why should you use transactions in SQLite?
Transactions ensure data integrity (ACID properties) and can significantly improve performance when performing multiple insert or update operations.

### 14. What is database normalization?
Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller, related tables.

### 15. How do you prevent SQL injection in Android SQLite?
Use parameterized queries (e.g., `?` placeholders) with strict argument binding via `selectionArgs` in `query()` or `execSQL()` methods.

### 16. What is the difference between `execSQL()` and `rawQuery()`?
- `execSQL()`: Used for SQL statements that do not return data (e.g., INSERT, UPDATE, DELETE, CREATE TABLE).
- `rawQuery()`: Used for SQL statements that return data (e.g., SELECT).

### 17. How do you optimize performance in SQLite?
- Use transactions for batch operations.
- Index columns used in WHERE clauses and joins.
- Query only necessary columns (avoid `SELECT *`).
- Use `VACUUM` to reclaim unused space.

### 18. What is Write-Ahead Logging (WAL) in SQLite?
WAL is a journaling mode that allows simultaneous readers and writers, improving concurrency and performance compared to the default rollback journal.

### 19. How do you enable Foreign Key constraints in SQLite?
Foreign Key constraints are disabled by default. Enable them by executing `PRAGMA foreign_keys = ON;` or calling `setForeignKeyConstraintsEnabled(true)` on the database instance.

### 20. How do you handle concurrency in SQLite?
SQLite uses locks to handle concurrency. For high concurrency, consider WAL (Write-Ahead Logging) mode:
```sql
PRAGMA journal_mode = WAL;
```

### 21. How do you drop a table in SQLite?
```sql
DROP TABLE users;
```

### 22. How do you export data from SQLite to CSV?
Using the SQLite CLI:
```sql
.mode csv
.output users.csv
SELECT * FROM users;
```

### 23. Explain Prepared Statements in SQLite.
Prepared statements compil SQL ahead of time, improving performance and security against injection.
```sql
INSERT INTO users (name, email) VALUES (?, ?)
```

### 24. How do you handle NULL values in SQLite?
Use `IS NULL` or `IS NOT NULL` in queries:
```sql
SELECT * FROM users WHERE email IS NULL;
```

### 25. How do you rename a table in SQLite?
```sql
ALTER TABLE users RENAME TO customers;
```
