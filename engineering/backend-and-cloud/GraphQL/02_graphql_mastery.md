# ⚛️ GraphQL for Mobile Engineers

> **Target Audience:** Senior Engineers integrating modern backends.
> **Scope:** Schema, Queries, Mutations, Federation, and Caching (Apollo).

![GraphQL](https://img.shields.io/badge/API-GraphQL-pink?style=for-the-badge&logo=graphql)

---

## 📖 Table of Contents
- [Level 1: Concepts & vs REST (1-10)](#level-1-concepts-vs-rest)
- [Level 2: Queries & Mutations (11-20)](#level-2-queries--mutations)
- [Level 3: Apollo Client & Caching (21-30)](#level-3-apollo-client--caching)
- [Level 4: Advanced Scenarios (31+)](#level-4-advanced-scenarios)

---

## Level 1: Concepts & vs REST

### Q1. What is the fundamental difference between GraphQL and REST?
**Answer:**
*   **REST**: Resource-based. Multiple endpoints (`/users`, `/posts`). Server defines structure. Over-fetching (getting too much data) or Under-fetching (n+1 problem) is common.
*   **GraphQL**: Data-graph based. Single endpoint (`/graphql`). Client defines structure. Exact fetching (get exactly what you ask for).

### Q2. What is the "Over-fetching" and "Under-fetching" problem?
**Answer:**
*   **Over-fetching**: REST API returns a huge JSON with 50 fields when you only need `id` and `name`. Wastes bandwidth.
*   **Under-fetching**: You need User + Posts. REST requires 2 calls: `GET /user` -> `GET /user/posts`. GraphQL does this in 1 query.

### Q3. Explain Schema, Query, Mutation, Subscription?
**Answer:**
*   **Schema (.graphql)**: Defines Types and their relationships (Strongly typed).
*   **Query**: Read-only fetch (like GET).
*   **Mutation**: Write operation (like POST/PUT/DELETE).
*   **Subscription**: Real-time event stream via WebSockets.

### Q4. What is the "N+1 Problem"?
**Answer:**
Fetching a list of N items, then making N separate DB calls to fetch related data for each item.
*   **REST Check**: Client makes N+1 HTTP requests.
*   **GraphQL Check**: Server might make N+1 DB calls if resolvers aren't optimized (using **DataLoaders**).

---

## Level 2: Queries & Mutations

### Q5. How do you handle Fragments?
**Answer:**
Fragments are reusable units of logic.
```graphql
fragment UserFields on User {
  id
  name
  avatar
}

query GetFeed {
  posts {
    author {
      ...UserFields
    }
  }
}
```

### Q6. What are Directives? (`@include`, `@skip`)
**Answer:**
Dynamic control over the query execution.
```graphql
query GetUser($showEmail: Boolean!) {
  user(id: "1") {
    name
    email @include(if: $showEmail)
  }
}
```

### Q7. How does a Mutation return updated data?
**Answer:**
You explicitly ask for the changed fields in the response payload.
```graphql
mutation UpdateName($id: ID!, $name: String!) {
  updateUser(id: $id, name: $name) {
    id
    name  # Returns the new name immediately
  }
}
```

---

## Level 3: Apollo Client & Caching

### Q8. Explain the Apollo "Normalized Cache".
**Answer:**
Apollo flattens the response data.
It creates a lookup table keyed by `__typename` + `id` (e.g., `User:42`).
**Benefit**: If Query A fetches User:42, and Query B fetches the same user, Query B can read from cache instantly without network.

### Q9. What are Fetch Policies?
**Answer:**
*   `CacheFirst`: Check cache. If missing, fetch network. (Default).
*   `CacheAndNetwork`: Return cache fast, then update from network in background. (Good for Feeds).
*   `NetworkOnly`: Always fetch fresh data.
*   `NoCache`: Don't read or write to cache.

### Q10. What is "Optimistic UI"?
**Answer:**
Updating the UI *before* the server responds.
You provide an `optimisticResponse` object to the mutation. Apollo writes this to cache immediately. If server fails, it rolls back automatically.

---

## Level 4: Advanced Scenarios

### Q11. How to upload files in GraphQL?
**Answer:**
GraphQL Spec doesn't support file uploads natively.
**Solution**: Use "GraphQL Multipart Request Spec". The client sends a multipart-form with JSON operations + binary file map.

### Q12. How to handle "Schema Federation"?
**Answer:**
Microservices approach.
Multiple subgraphs (Accounts Service, Products Service) are composed into a single Supergraph Gateway. The Mobile App still talks to one endpoint.

### Q13. Debugging: "Cache Miss" hell.
**Scenario**: You updated a user's name in Detail screen, but List screen shows old name.
**Debug**:
1.  Check if your types have unique `id` fields. Apollo needs `id` to normalize.
2.  Did the Mutation return the `id`? If not, Apollo can't merge the result into the existing object.
3.  Check if using different arguments (pagination keys) caused storage in different keys.
