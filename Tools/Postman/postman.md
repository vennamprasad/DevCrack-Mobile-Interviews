# 🚀 Postman API Testing
> **Targeted for Mobile Developers**
> **Note:** Collections, Environments, and Automated Tests.

![Postman](https://img.shields.io/badge/Tool-Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

---

## 📖 Table of Contents
- [1. Basics](#basics)
- [2. Collections & Environments](#collections--environments)
- [3. Scripting & Tests](#scripting--tests)
- [4. Mock Servers](#mock-servers)

---

### Q1. What are Environments?

**Answer:**
Environments allow you to store key-value pairs (variables) to switch contexts easily.
**Example:**
- Variable: `{{base_url}}`
- **Dev Env**: `localhost:8080`
- **Prod Env**: `api.example.com`
Allows using the *same* request collection against different backends without editing URLs manually.

### Q2. How to chain requests (Auth -> Data)?

**Answer:**
Use the **Tests** tab to capture data from Response A and set it as an environment variable for Request B.
**Request A (Login):**
```javascript
// Tests Tab
var jsonData = pm.response.json();
pm.environment.set("jwt_token", jsonData.token);
```
**Request B (Get Profile):**
Authorization: Bearer `{{jwt_token}}`

### Q3. Automated Testing Validation?

**Answer:**
In the **Tests** tab:
```javascript
// Check Status Code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Check Response Time
pm.test("Response time is less than 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Check JSON Body
pm.test("User is valid", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.name).to.eql("John Doe");
});
```

### Q4. What is Newman?

**Answer:**
**Newman** is the CLI runner for Postman. It allows running Postman Collections in a CI/CD pipeline (e.g., Jenkins, GitHub Actions) to automatically verify APIs before building the app.
`newman run MyCollection.json -e MyEnvironment.json`