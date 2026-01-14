# ⚠️ API Error Handling
> **Targeted for iOS Developers**
> **Note:** Parsing Errors, User Feedback, and Retries.

![Errors](https://img.shields.io/badge/Networking-Errors-red?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Types of Errors](#1-types-of-errors)
- [2. Mapping Errors](#2-mapping-errors)
- [3. Retry Logic](#3-retry-logic)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. Common Networking Errors?

**Answer:**
1.  **Transport Error**: No internet, Timeout (`NSURLErrorDomain`).
2.  **HTTP Error**: Server reached, but 4xx (Client) or 5xx (Server) status code.
3.  **Decoding Error**: JSON doesn't match Model (`DecodingError.keyNotFound`).
4.  **Business Error**: Server sent 200 OK, but payload says `{"success": false}`.

### Q2. Best practice for parsing errors?

**Answer:**
Create a custom Enum.
```swift
enum APIError: Error {
    case invalidURL
    case serverError(statusCode: Int)
    case decodingError
    case unknown(Error)
}
```
Map `URLSession` errors to this clean Enum in your Network Layer before passing to the ViewModel.

### Q3. Handling Token Expiry (401)?

**Answer:**
Use an **Interceptor** (or `Authenticator`).
1.  Detect 401.
2.  Queue the failed request.
3.  Call Refresh Token API.
4.  If success, retry the queued request with new token.
5.  If fail, logout user.
*Alamofire has built-in `RequestInterceptor`. In URLSession, you implement it manually.*

---

### 5. Real-World Scenarios

### Q4. Scenario: User gets a generic "Something went wrong" message. How to improve?

**Answer:**
Map errors to user-friendly strings locally.
- 500 -> "Our servers are having trouble."
- No Internet -> "Please check your connection."
- 401 -> "Session expired. Logging out."
Never show raw JSON errors ("key 'id' not found") to the user.

### Q5. Scenario: "Decoding Error" but you don't know which field failed.

**Answer:**
Catch `DecodingError` specifically and print it.
```swift
do {
    _ = try decoder.decode(...)
} catch let DecodingError.keyNotFound(key, context) {
    print("Missing key: \(key) in \(context.codingPath)")
} catch let DecodingError.typeMismatch(type, context) {
    print("Type mismatch: expected \(type) at \(context.codingPath)")
}
```

### Q6. Scenario: How to implement "Exponential Backoff" for retries?

**Answer:**
If request fails, wait 1s -> retry. Fail? Wait 2s. Fail? Wait 4s.
Prevents hammering a struggling server.
```swift
func retry(attempt: Int) {
    let delay = pow(2.0, Double(attempt))
    DispatchQueue.main.asyncAfter(deadline: .now() + delay) { ... }
}
```

### Q7. Scenario: API returns 200 OK for errors (GraphQL style).

**Answer:**
You cannot rely on `response.statusCode`.
You must decode the JSON body.
```json
{ "data": null, "errors": [{ "message": "Unauthorized" }] }
```
Check if `errors` array is not empty. If so, throw a custom Error, even if HTTP is 200.

### Q8. Scenario: Handling multiple parallel errors?

**Answer:**
If you fire 3 requests and all 3 fail (e.g., No Internet), you don't want to show 3 Alert popups stacked on top of each other.
**Fix**: Use a centralized `ErrorManager` or `Toast` system that debounces messages (show only one "No Internet" toast).

### Q9. Scenario: Cancellation Error (`NSURLErrorCancelled`)?

**Answer:**
This happens when you explicitly call `task.cancel()`.
**Important**: Do NOT treat this as a failure (don't show "Request Failed" alert).
Filter it out: `if error.code == .cancelled { return }`.

### Q10. Scenario: Logging errors to backend (Sentry/Crashlytics)?

**Answer:**
Log non-fatal errors.
`Crashlytics.crashlytics().record(error: apiError)`
Essential for monitoring API health in production (e.g., catching a spike in 500 errors after a backend deploy).

### Q11. Scenario: Backend changed a field from `Int` to `String` (Breaking Change). App crashes.

**Answer:**
Use `do-catch` to handle decoding safely.
Maybe use a **flexible decoder strategy**:
```swift
// Custom implementation to handle String or Int
enum StringOrInt: Decodable {
    init(from decoder: Decoder) throws { ... } // try decode Int, else try String
}
```

### Q12. Scenario: Handling Empty Response body (204 No Content)?

**Answer:**
`JSONDecoder` will throw "Data Corrupted" if you try to decode empty data.
Check status 204 first. Or make your return type `Void` / `EmptyResponse?`.
`if response.statusCode == 204 { return }`

### Q13. Scenario: Silent failures?

**Answer:**
Analytics requests often fail silently. You don't warn the user.
Configuration: `wrapper.retry(3)` then give up. Do not block UI.

### Q14. Scenario: Date Parsing errors?

**Answer:**
Backend sends "2023-01-01". Default decoder expects different format?
Set `decoder.dateDecodingStrategy = .iso8601` (or `.formatted(formatter)`).
Mismatch causes instant Decoding Error.

### Q15. Scenario: Debugging encrypted traffic?

**Answer:**
You can't see HTTPS body in console.
Use **Charles Proxy** or **Proxyman**.
Install their Root Certificate on simulator/device to perform Man-in-the-Middle on yourself and inspect JSON payload/headers.
