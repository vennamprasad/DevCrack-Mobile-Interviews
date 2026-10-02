# Mobile App Penetration Testing Checklist

## Static Analysis
- [ ] Decompile APK and analyze code
- [ ] Check for hardcoded secrets/keys
- [ ] Analyze AndroidManifest.xml for security issues
- [ ] Check for exported components
- [ ] Analyze certificate pinning implementation
- [ ] Check ProGuard/R8 configuration
- [ ] Analyze cryptographic implementations

## Dynamic Analysis
- [ ] Intercept HTTPS traffic (test certificate pinning)
- [ ] Test API endpoints for vulnerabilities
- [ ] Test authentication bypass attempts
- [ ] Test for SQL injection
- [ ] Test for insecure data storage
- [ ] Test for insecure logging
- [ ] Test root detection bypass
- [ ] Test debugger detection bypass

## Runtime Analysis
- [ ] Hook into app with Frida
- [ ] Bypass certificate pinning
- [ ] Bypass root detection
- [ ] Bypass biometric authentication
- [ ] Extract sensitive data from memory
- [ ] Test for memory leaks of sensitive data

## Authentication & Session Management
- [ ] Test weak password policies
- [ ] Test for authentication bypass
- [ ] Test session timeout
- [ ] Test for session fixation
- [ ] Test token validation
- [ ] Test biometric authentication bypass

## Data Storage
- [ ] Check SharedPreferences encryption
- [ ] Check database encryption
- [ ] Check file storage security
- [ ] Check cache security
- [ ] Check clipboard data exposure

## Network Security
- [ ] Test TLS version enforcement
- [ ] Test certificate validation
- [ ] Test for man-in-the-middle vulnerabilities
- [ ] Test API key security
- [ ] Test request/response encryption

## Business Logic
- [ ] Test transaction limits bypass
- [ ] Test race conditions
- [ ] Test payment flow manipulation
- [ ] Test authorization checks
