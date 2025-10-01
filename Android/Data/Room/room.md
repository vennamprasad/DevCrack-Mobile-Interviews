# Room Database Interview Questions

## Basic Questions

### 1. What is Room in Android?
Room is a persistence library that provides an abstraction layer over SQLite to allow fluent database access while harnessing the full power of SQLite.

### 2. What are the main components of Room?
- **Entity:** Represents a table within the database.
- **DAO (Data Access Object):** Contains methods for accessing the database.
- **Database:** The main access point to the persisted data.

### 3. How do you define an Entity in Room?
An Entity is defined using the `@Entity` annotation on a data class. Each property represents a column.

```kotlin
@Entity
data class User(
    @PrimaryKey val uid: Int,
    @ColumnInfo(name = "name") val name: String?
)
```

### 4. What is a DAO in Room?
DAO is an interface annotated with `@Dao` that defines database operations like `@Insert`, `@Delete`, `@Update`, and `@Query`.

### 5. How do you create a Room Database?
Extend `RoomDatabase` and annotate with `@Database`. Include entities and DAOs.

```kotlin
@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

## Advanced Questions

### 6. How does Room handle database migrations?
Room uses the `Migration` class to define migration paths between versions. You register migrations when building the database.

### 7. What is the purpose of `@Query` annotation?
`@Query` is used to define custom SQL queries for fetching, updating, or deleting data.

### 8. How does Room support LiveData and Flow?
Room can return `LiveData` or `Flow` from DAO queries, enabling reactive data updates in the UI.

### 9. What is the difference between `@Embedded` and `@Relation`?
- `@Embedded` is used to include fields from another object as columns in the same table.
- `@Relation` is used to define relationships between entities, such as one-to-many or many-to-one.

### 10. How do you test Room databases?
Use in-memory databases (`Room.inMemoryDatabaseBuilder`) for unit testing, and use `@Test` annotations to verify DAO operations.

### 11. How do you integrate Room with Dependency Injection (DI)?
Room databases and DAOs can be provided as dependencies using DI frameworks like Dagger or Hilt. Annotate your `AppDatabase` provider with `@Singleton` and inject DAOs where needed.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase =
        Room.databaseBuilder(context, AppDatabase::class.java, "app_db").build()

    @Provides
    fun provideUserDao(db: AppDatabase): UserDao = db.userDao()
}
```

### 12. How can you secure data stored in Room?
- Use SQLCipher to encrypt the SQLite database.
- Restrict access to the database file using proper file permissions.
- Avoid storing sensitive data in plain text.
- Use ProGuard or R8 to obfuscate code and prevent reverse engineering.

### 13. How do you use SQLCipher with Room for encryption?
Add SQLCipher dependencies and configure the Room database builder with a passphrase:

```kotlin
val passphrase: ByteArray = SQLiteDatabase.getBytes("your-secure-passphrase".toCharArray())
val factory = SupportFactory(passphrase)
Room.databaseBuilder(context, AppDatabase::class.java, "secure-db")
    .openHelperFactory(factory)
    .build()
```

### 14. What are best practices for securing Room database access?
- Use DI to manage database instances and avoid memory leaks.
- Encrypt sensitive data before storing.
- Validate user input to prevent SQL injection (even though Room uses parameterized queries).
- Regularly update dependencies to patch security vulnerabilities.

### 15. How do you handle large data sets efficiently in Room?
- Use paging libraries like Paging 3 to load data in chunks.
- Write optimized SQL queries with proper indexing.
- Avoid loading entire tables into memory; use limit and offset in queries.

### 16. How do you perform multi-threaded operations with Room?
- Room supports suspend functions and RxJava/Flow for asynchronous operations.
- Always perform database operations off the main thread using coroutines or executors.

### 17. How do you handle complex relationships (many-to-many) in Room?
- Create a junction (cross-reference) entity to represent the relationship.
- Use `@Relation` annotations in data classes to fetch related data.

### 18. What strategies do you use for versioning and migration in production apps?
- Plan migrations ahead and test thoroughly.
- Use fallback strategies like `fallbackToDestructiveMigration` only for non-critical data.
- Maintain migration scripts and automate migration testing.

### 19. How do you optimize Room queries for performance?
- Use projections to fetch only required columns.
- Add indexes to frequently queried columns.
- Profile queries using Android Studio’s Database Inspector.

### 20. How do you handle schema changes without data loss?
- Write custom migration logic to transform and preserve data.
- Backup data before applying migrations in critical applications.
- Use temporary tables if needed during migration steps.
### 21. Can you show basic migration logic in Room with an example?
To migrate a Room database from one version to another, implement a `Migration` object specifying the start and end versions and the SQL statements needed to update the schema.

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        // Example: Add a new column to the User table
        database.execSQL("ALTER TABLE User ADD COLUMN age INTEGER DEFAULT 0 NOT NULL")
    }
}

// Register migration when building the database
Room.databaseBuilder(context, AppDatabase::class.java, "app_db")
    .addMigrations(MIGRATION_1_2)
    .build()
```