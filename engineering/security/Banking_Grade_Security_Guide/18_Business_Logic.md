# 💼 Business Logic & Transaction Integrity Defense

> **Preventing parameter tampering, transaction replay attacks, race conditions, and unauthorized privilege escalation in financial mobile applications.**

---

## 🛡️ 1. Anti-Replay & Transaction Signing Architecture

Never trust transaction data coming from the client without cryptographic proof of integrity and server-side nonce validation.

```
Client App                             Backend Gateway
    │                                         │
    │ ─── 1. Request Transaction Nonce ─────> │
    │ <── 2. Returns Unique Nonce (UUID/hash) ─│
    │                                         │
    │ [Sign payload + Nonce with Private Key] │
    │                                         │
    │ ─── 3. Submit Transaction Payload ────> │
    │        - Amount, Recipient, Nonce       │
    │        - Digital Signature              │
    │        - Play Integrity Attestation JWS │
    │                                         │
    │                                         │ [Verify Signature against Public Key]
    │                                         │ [Verify Nonce is valid and UNUSED]
    │                                         │ [Mark Nonce as CONSUMED immediately]
    │                                         │ [Process Transaction]
    │ <── 4. Transaction Confirmation ────────│
```

---

## 📋 Business Logic Security Checklist

- [ ] **Server-Side Validation**: Never perform financial checks (balance sufficiency, transaction limits, discounts) purely on client UI.
- [ ] **Idempotency Keys**: Require unique client-generated UUID idempotency keys on payment requests to prevent double-charging on network retries.
- [ ] **Dynamic Nonces**: Every fund transfer must require a short-lived, single-use server nonce signed by the device's KeyStore private key.
- [ ] **Play Integrity API Binding**: Bind the transaction hash into the Google Play Integrity API `requestHash` parameter to prove the payload originated from an untampered app binary on a genuine certified device.
- [ ] **Step-Up Authentication**: Enforce biometric or SMS/hardware OTP re-authentication when transferring above high-value risk thresholds.
