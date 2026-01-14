# 📡 GraphQL Fundamentals
> **Targeted for Mobile Developers**
> **Note:** Flexible data fetching with a single endpoint.

![GraphQL](https://img.shields.io/badge/Backend-GraphQL-e10098?style=for-the-badge&logo=graphql&logoColor=white)

---

## 📖 Table of Contents
- [1. What is GraphQL?](#1-what-is-graphql)
- [2. Core Concepts](#2-core-concepts)
- [3. REST vs GraphQL](#3-rest-vs-graphql)
- [4. Mobile Implementation](#4-mobile-implementation-android)

---

### 1. What is GraphQL?
A query language for APIs and a runtime for fulfilling those queries with your existing data. It solves the **Over-fetching** and **Under-fetching** problems of REST.

### 2. Core Concepts
- **Schema**: The contract between client and server, defined in SDL (Schema Definition Language).
- **Query**: GET equivalent. Used to fetch data.
- **Mutation**: POST/PUT/DELETE equivalent. Used to modify data.
- **Subscription**: Real-time updates via WebSockets.
- **Resolver**: Function that fetches the data for a specific field.

**Example Query:**
```graphql
query {
  user(id: "123") {
    name
    email
    posts {
      title
    }
  }
}
```

### 3. REST vs GraphQL
| Feature | REST | GraphQL |
| :--- | :--- | :--- |
| **Endpoint** | Multiple (`/users`, `/posts`) | Single (`/graphql`) |
| **Fetching** | Fixed data structure | Client requests exactly what it needs |
| **Versioning** | v1, v2 | Schema evolution (deprecate fields) |
| **Over-fetching** | Common | Solved |
| **Caching** | Built-in HTTP caching | Harder (requires client-side logic) |

### 4. Mobile Implementation (Android)
Using **Apollo Kotlin** (formerly Apollo Android).

**Setup:**
1.  Add plugin and dependency.
2.  Download `schema.json`.
3.  Write `.graphql` query files.
4.  Apollo generates Kotlin models automatically.

**Code Example:**
```kotlin
// 1. Write Query (UserQuery.graphql)
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
  }
}

// 2. Execute in Kotlin
val response = apolloClient.query(GetUserQuery(id = "1")).execute()
val userName = response.data?.user?.name
```

### Interview Questions

**Q1. What is the N+1 problem and how does GraphQL solve it?**
**Answer:**
The N+1 problem happens when fetching a list of N items requires N additional database queries to fetch related data (e.g., fetching 10 posts, then 10 queries for authors).
GraphQL *backends* (via DataLoaders) batch these requests into a single database call, though this is a backend concern, mobile devs should understand why their queries might be slow if not handled.

**Q2. How do you handle authentication in GraphQL?**
**Answer:**
Ideally via HTTP Headers (Authorization Bearer token) just like REST. The context is passed to the resolvers.

**Q3. Disadvantages of GraphQL?**
**Answer:**
1.  **Complexity**: Setup is harder than REST.
2.  **Caching**: HTTP caching doesn't work out-of-the-box (POST requests).
3.  **File Uploads**: Not part of the spec (need workarounds like multipart requests).

**Q4. What are Fragments?**
**Answer:**
Reusable units of logic in GraphQL.
```graphql
fragment UserFields on User {
  id
  name
  profilePic
}

query {
  user {
    ...UserFields
  }
}
```
