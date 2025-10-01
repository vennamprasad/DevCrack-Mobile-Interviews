### 1. What is Realm Database in Android?
**Answer:** Realm is a mobile database that runs directly inside phones, tablets, or wearables. It is an alternative to SQLite and Core Data, offering object-oriented data storage and easy-to-use APIs.

---

### 2. How does Realm differ from SQLite?
**Answer:** Realm uses objects for data storage instead of tables and rows. It provides a more intuitive API, supports reactive data change notifications, and is faster for many operations compared to SQLite.

---

### 3. How do you define a Realm model in Android?
**Answer:** You define a model by creating a class that extends `RealmObject` and annotating fields with `@PrimaryKey` or `@Required` as needed.

```java
public class User extends RealmObject {
    @PrimaryKey
    private int id;
    private String name;
}
```

---

### 4. How do you perform a write operation in Realm?
**Answer:** All write operations must be done inside a transaction:

```java
realm.executeTransaction(new Realm.Transaction() {
    @Override
    public void execute(Realm realm) {
        User user = realm.createObject(User.class, 1);
        user.setName("John");
    }
});
```

---

### 5. How do you query data from Realm?
**Answer:** You use Realm's query API:

```java
RealmResults<User> users = realm.where(User.class)
                                .equalTo("name", "John")
                                .findAll();
```

---

### 6. What are the advantages of using Realm over other databases?
**Answer:** Realm offers easy object mapping, fast performance, built-in data change notifications, and simple migration support.

---

### 7. How do you handle migrations in Realm?
**Answer:** You set a migration strategy using `RealmConfiguration` and implement the `RealmMigration` interface to handle schema changes.

---

### 8. Is Realm thread-safe?
**Answer:** Realm instances are not thread-safe. You must get a new Realm instance for each thread.

---

### 9. How do you close a Realm instance?
**Answer:** Call `realm.close()` when you are done with the instance to free resources.

---

### 10. Can Realm be used with LiveData or RxJava?
**Answer:** Yes, Realm supports reactive extensions and can be integrated with RxJava and LiveData for observing data changes.