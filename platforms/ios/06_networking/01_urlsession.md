# 🌐 URLSession
> **Targeted for iOS Developers**
> **Note:** Configuration, Tasks, and Delegate.

![Networking](https://img.shields.io/badge/Networking-URLSession-blue?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Basics](#1-basics)
- [2. Configuration](#2-configuration)
- [3. Background Downloads](#3-background-downloads)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. `URLSession` Configurations?

**Answer:**
1.  **`.default`**: Basic. Uses disk-based cache, stores cookies/credentials.
2.  **`.ephemeral`**: No persistent storage (RAM only). "Private Browsing".
3.  **`.background(identifier)`**: Performs uploads/downloads in a separate process. Continues even if the app is suspended/terminated.

### Q2. Types of Tasks?

**Answer:**
- **`dataTask`**: Returning a chunk of data (JSON/XML) in memory.
- **`downloadTask`**: Writes data to a temporary file on disk. (Resume supported).
- **`uploadTask`**: Sends a file or data from disk/memory.
- **`streamTask`**: Continuous stream (TCP/Socket).

### Q3. Caching Policies?

**Answer:**
Defined in `URLRequest.cachePolicy`.
- `.useProtocolCachePolicy`: Follows HTTP headers (Default).
- `.ignoreLocalCacheData`: Force fetch from server.
- `.returnCacheDataElseLoad`: Use cache if available, else load.
- `.returnCacheDataDontLoad`: Offline mode (fail if not cached).

### Q4. Parsing JSON?

**Answer:**
Use `JSONDecoder`.
```swift
let (data, response) = try await URLSession.shared.data(from: url)
let user = try JSONDecoder().decode(User.self, from: data)
```

---

### 5. Real-World Scenarios

### Q5. Scenario: You need to implement "Pull to Refresh" but ensure the network call bypasses the cache.

**Answer:**
Set `cachePolicy` to `.reloadIgnoringLocalCacheData` on the `URLRequest`.
This forces `URLSession` to talk to the server, ensuring fresh data.

### Q6. Scenario: Uploading a large video (500MB). App goes to background. Upload fails.

**Answer:**
Standard `dataTask` or `uploadTask` is suspended when the app suspends.
**Fix**: Use a **Background Configuration** (`URLSessionConfiguration.background`).
The OS takes over the upload task. Even if your app dies, the OS finishes the upload and wakes up your app (calls `handleEventsForBackgroundURLSession` in AppDelegate) to tell you it's done.

### Q7. Scenario: Implementing Multipart/Form-Data (Image Upload)?

**Answer:**
`URLSession` doesn't support this natively like Alamofire.
You must construct the HTTP Body manually:
1.  Boundary string.
2.  Headers: `Content-Type: multipart/form-data; boundary=...`
3.  Data: `--boundary`, Content-Disposition, Image Data, `--boundary--`.

### Q8. Scenario: Certificate Pinning implementation?

**Answer:**
Implement `urlSession(_:didReceive:completionHandler:)` delegate method.
Inside, explore `challenge.protectionSpace.serverTrust`. Extract the certificate/public key and compare it with the local hash embedded in your app bundle.

### Q9. Scenario: Detecting "No Internet" reliably?

**Answer:**
**NWPathMonitor** (Network framework).
Do not rely on a failed request. Monitor the state proactively.
```swift
let monitor = NWPathMonitor()
monitor.pathUpdateHandler = { path in
    if path.status == .satisfied { print("Online") }
}
```

### Q10. Scenario: Handling 401 Unauthorized (Token Refresh)?

**Answer:**
Since `URLSession` has no built-in interceptor:
1.  Check response status code.
2.  If 401, pause other requests? Not automatic.
3.  Ideally, wrap `URLSession` in a NetworkManager class that checks 401, calls `refreshToken()`, awaits, and then retries the original request.

### Q11. Scenario: Request Timeout?

**Answer:**
`configuration.timeoutIntervalForRequest`. Default is 60s.
If you need 10s for API A and 60s for API B, use distinct configurations or set `timeoutInterval` on the specific `URLRequest`.

### Q12. Scenario: App Transport Security (ATS) blocked your HTTP request?

**Answer:**
Error: "App Transport Security has blocked a cleartext HTTP (http://) resource load."
**Fix**:
1.  Use HTTPS (Correct way).
2.  Add exception domain to Info.plist > NSAppTransportSecurity (if you don't control the server).

### Q13. Scenario: Cookies management?

**Answer:**
`URLSession` automatically handles cookies via `HTTPCookieStorage.shared`.
If the server sends `Set-Cookie`, it's saved. Subsequent requests send `Cookie` header.
To clear login: Manually delete cookies from `HTTPCookieStorage` or use `.ephemeral` session.

### Q14. Scenario: How to mock URLSession for Testing?

**Answer:**
**URLProtocol**.
Create `MockURLProtocol`. Determine what response to return based on the request URL.
Inject a `URLSession` configured with this protocol into your Networking Service.

### Q15. Scenario: Dealing with massive JSON responses slowing down UI?

**Answer:**
Decoding `Data` -> `Structs` is CPU intensive.
If fetching a list of 5000 items:
1.  Run `JSONDecoder` on a background actor/queue.
2.  Switch to main only after decoding is done.
```swift
let user = try await Task.detached {
    try JSONDecoder().decode(User.self, from: data)
}.value
```
