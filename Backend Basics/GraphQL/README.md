# ⚛️ GraphQL for Mobile Engineers

> **Master GraphQL query language, schema design, mutations, subscriptions, Apollo client caching, and REST vs GraphQL architectural trade-offs.**

![GraphQL](https://img.shields.io/badge/API-GraphQL-e10098?style=for-the-badge&logo=graphql&logoColor=white)
![Apollo](https://img.shields.io/badge/Client-Apollo_Kotlin_%2F_iOS-311C87?style=for-the-badge&logo=apollographql&logoColor=white)

---

## 📖 Module Contents

| Guide | Scope | Target Audience |
| :--- | :--- | :--- |
| **[01. GraphQL Fundamentals](./graph.md)** | Core concepts, over-fetching / under-fetching problems, schema definition, queries, and mutations. | Mid / Senior |
| **[02. GraphQL for Mobile Engineers (Deep Dive)](./graphql.md)** | Level 1–4 question bank: Schema federation, Apollo Client normalized cache, subscriptions over WebSockets, and performance. | Senior / Staff |

---

## ⚖️ GraphQL vs REST Decision Matrix

| Dimension | REST | GraphQL |
| :--- | :--- | :--- |
| **Endpoint** | Multiple resource-specific URLs (`/users`, `/posts`) | Single endpoint (`/graphql`) |
| **Data Fetching** | Fixed server-defined payloads | Client specifies exact requested fields |
| **Over/Under-Fetching** | Common issue requiring BFF (Backend-For-Frontend) | Eliminated by client-driven queries |
| **Network Caching** | Native HTTP caching via URLs and ETag headers | Complex; requires normalized client cache (Apollo) |
| **File Uploads** | Standard `multipart/form-data` | Requires GraphQL multipart request spec |
