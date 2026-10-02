# 🌐 REST API Fundamentals
> **Targeted for Mobile Developers**
> **Note:** Mastering HTTP, Resources, and Constraints.

![REST](https://img.shields.io/badge/Backend-REST-blue?style=for-the-badge&logo=postman&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Principles](#1-what-is-rest)
- [2. HTTP Methods](#2-http-methods)
- [3. Status Codes](#3-http-status-codes)
- [4. Statelessness](#4-statelessness)
- [5. Interview Questions](#interview-questions)

---

### 1. What is REST?
**REST (Representational State Transfer)** is an architectural style for distributed hypermedia systems. It is not a standard or protocol but a set of constraints.

**Key Constraints:**
1.  **Client-Server**: Separation of concerns.
2.  **Stateless**: Each request must contain all necessary info.
3.  **Cacheable**: Responses must define themselves as cacheable or not.
4.  **Uniform Interface**: Standardized way to communicate (Resources, Verbs).
5.  **Layered System**: Client doesn't know if it's connected to end server or intermediate.
6.  **Code on Demand (Optional)**: Servers can extend client functionality (e.g., JS).

### 2. HTTP Methods
Verbs that define the action:

| Method | Role | Idempotent | Safe |
| :--- | :--- | :---: | :---: |
| **GET** | Retrieve a resource. | ✅ | ✅ |
| **POST** | Create a resource. | ❌ | ❌ |
| **PUT** | Update/Replace a resource. | ✅ | ❌ |
| **PATCH** | Partial update of a resource. | ❌ | ❌ |
| **DELETE** | Remove a resource. | ✅ | ❌ |
| **HEAD** | Retrieve headers (no body). | ✅ | ✅ |

### 3. HTTP Status Codes
Categorized by the first digit:

- **2xx (Success)**
    - `200 OK`: Standard success.
    - `201 Created`: Resource successfully created (POST).
    - `204 No Content`: Successful request, but no body returned (DELETE).
- **3xx (Redirection)**
    - `301 Moved Permanently`: New URL.
    - `304 Not Modified`: Cached version is still valid.
- **4xx (Client Error)**
    - `400 Bad Request`: Invalid syntax/validation.
    - `401 Unauthorized`: Authentication required.
    - `403 Forbidden`: Authenticated but no permission.
    - `404 Not Found`: Resource doesn't exist.
    - `429 Too Many Requests`: Rate limiting.
- **5xx (Server Error)**
    - `500 Internal Server Error`: Generic server crash.
    - `503 Service Unavailable`: Server overloaded/maintenance.

### 4. Statelessness
In REST, **stateless** means the server does not store any session context between requests.
- **Pros**: Scalability (easy to add servers), Reliability (server failure doesn't kill session).
- **Cons**: Overhead (request must contain all info, e.g., tokens).

---

## Interview Questions

### Q1. What is the difference between specific HTTP verbs?
**Answer:**
- **PUT vs PATCH**: `PUT` is for replacing the *entire* resource (if you only send name, other fields might be nulled). `PATCH` is for *partial* updates (only change what is sent).
- **POST vs PUT**: `POST` creates a new resource (usually under a collection). `PUT` creates or replaces a resource at a *specific* URI.

### Q2. How do you handle versioning in REST?
**Answer:**
1.  **URI Versioning**: `/api/v1/users` (Most common).
2.  **Header Versioning**: `Accept: application/vnd.myapi.v1+json`.
3.  **Parameter Versioning**: `/api/users?version=1`.

### Q3. What means "Idempotent"?
**Answer:**
An operation is idempotent if making the same request multiple times has the **same effect** as making it once.
- `DELETE /users/1` is idempotent (calling it 10 times still results in user 1 being gone).
- `POST /users` is NOT idempotent (calling it 10 times creates 10 users).

### Q4. REST vs SOAP?
**Answer:**
| Feature | REST | SOAP |
| :--- | :--- | :--- |
| **Protocol** | HTTP (usually) | HTTP, SMTP, TCP, etc. |
| **Format** | JSON, XML, HTML | XML only |
| **Structure** | Flexible | Rigid (WSDL) |
| **Performance**| Lightweight | Heavy (XML parsing) |
