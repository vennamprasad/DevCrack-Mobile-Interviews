# 🔗 Mobile Deep Linking, Deferred Routing & Attribution (Branch.io & AppsFlyer)

> **Architecting the mobile growth funnel: Universal Links, Android App Links, Deferred Deep Linking through the App Store, and privacy-first attribution (SKAdNetwork / Privacy Sandbox).**

---

## 📌 Executive Summary

Modern mobile applications do not exist in isolation. Users discover content via web browsers, social media ads (Instagram, TikTok), SMS, and email campaigns.

The two fundamental platform challenges every mobile architect must master are:
1. **Seamless Deep Linking (Branch.io)**: Opening the mobile app directly to specific content, and **Deferred Deep Linking** (remembering the destination even if the user has to install the app from the App Store first).
2. **Mobile Measurement & Attribution (AppsFlyer / Adjust)**: Determining with mathematical precision which marketing campaign, ad creative, or organic channel generated an install or in-app purchase.

---

## 🏗️ Deep Linking Architecture: Protocols Compared

```
                ┌────────────────────────────────────────────────────────┐
                │                     Incoming Link                      │
                └──────────────────────────┬─────────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
[ Custom URL Scheme ]                                       [ Universal Links / App Links ]
(e.g., myapp://product/123)                                 (e.g., https://app.example.com/product/123)
 • ❌ Unsecured (Any app can register it)                   • ✅ Cryptographically verified domain
 • ❌ Shows ugly browser error if not installed             • ✅ Fallbacks cleanly to web browser
 • ⚠️ Deprecated for primary external routing               • ✅ Required standard for iOS & Android
```

---

## 🔄 The Magic of "Deferred Deep Linking" (Branch.io)

What happens if a user clicks a link to buy a pair of shoes, but **does not have the app installed**?

```
[ User clicks Branch Link on Web / Instagram ]
                     │
                     ▼
           [ Branch Routing Server ]
   (Captures Device Fingerprint / IP / Clipboard)
                     │
                     ▼
        [ Redirect to Apple App Store ]
                     │
                     ▼
          [ User Installs & Opens App ]
                     │
                     ▼
           [ App Initializes Branch SDK ]
                     │
                     ▼
         [ Branch Match Server Query ]
(Matches Install to Pre-Install Click Context)
                     │
                     ▼
       [ Deferred Deep Link Payload Delivered ]
  { "target": "product_detail", "sku": "shoe_984" }
                     │
                     ▼
   [ App Automatically Pushes Product Screen! ]
```

---

## 💻 Scalable Deep Link Router Pattern (Kotlin)

Never parse URL query parameters inside an Activity or Fragment! Centralize routing behind a clean, type-safe Deep Link Router.

```kotlin
sealed class DeepLinkDestination {
    data class ProductDetail(val productId: String, val referralCode: String?) : DeepLinkDestination()
    data class UserProfile(val username: String) : DeepLinkDestination()
    object Cart : DeepLinkDestination()
    data class Unknown(val rawUri: Uri) : DeepLinkDestination()
}

class DeepLinkParser {
    fun parse(uri: Uri): DeepLinkDestination {
        val pathSegments = uri.pathSegments
        return when {
            // Pattern: /product/{id}
            pathSegments.size >= 2 && pathSegments[0] == "product" -> {
                DeepLinkDestination.ProductDetail(
                    productId = pathSegments[1],
                    referralCode = uri.getQueryParameter("ref")
                )
            }
            // Pattern: /user/{username}
            pathSegments.size >= 2 && pathSegments[0] == "user" -> {
                DeepLinkDestination.UserProfile(username = pathSegments[1])
            }
            // Pattern: /cart
            pathSegments.firstOrNull() == "cart" -> DeepLinkDestination.Cart
            else -> DeepLinkDestination.Unknown(uri)
        }
    }
}

// Router orchestrating navigation via Jetpack Compose / Navigation Component
class AppNavigator(
    private val navController: NavController,
    private val parser: DeepLinkParser
) {
    fun handleDeepLink(uri: Uri) {
        when (val destination = parser.parse(uri)) {
            is DeepLinkDestination.ProductDetail -> {
                navController.navigate("product/${destination.productId}?ref=${destination.referralCode}")
            }
            is DeepLinkDestination.UserProfile -> {
                navController.navigate("profile/${destination.username}")
            }
            is DeepLinkDestination.Cart -> {
                navController.navigate("cart")
            }
            is DeepLinkDestination.Unknown -> {
                // Fallback to in-app WebView or Home
                navController.navigate("home")
            }
        }
    }
}
```

---

## 📊 Mobile Measurement Partners (MMP): AppsFlyer & Adjust

An MMP acts as an **unbiased referee** between ad networks (Google Ads, Meta Ads, TikTok) and the app publisher.

### Why You Cannot Build Attribution In-House:
1. **Self-Attributing Networks (SANs)**: Google and Meta do not share user device IDs directly. Only certified MMPs receive raw impression/click callbacks via secure server-to-server APIs.
2. **Deduplication Engine**: If a user views an ad on TikTok, clicks an ad on Instagram, and then downloads the app via Google Search, who gets credit?
   - The MMP runs **Last-Touch Attribution** logic across all networks to ensure the publisher doesn't pay triple commissions.

---

## 🔒 The Privacy Revolution: SKAdNetwork & Privacy Sandbox

### 1. iOS App Tracking Transparency (ATT) & SKAdNetwork (SKAN 4.0)
Since iOS 14.5, accessing the `IDFA` (Identifier for Advertisers) requires user opt-in prompt (`requestTrackingAuthorization`). Over 75% of users opt out.
- **SKAdNetwork**: Apple's privacy-preserving attribution framework.
- Apple sends postbacks directly to ad networks with a **Conversion Value** (0-63 integer or coarse tier: low/medium/high).
- Timers and randomized delays prevent advertisers from identifying individual users.

### 2. Android Privacy Sandbox
Android's counterpart to deprecate GAID (Google Advertising ID):
- **Attribution Reporting API**: Measures conversions without cross-app identifiers.
- **Protected Audience API**: Enables remarketing directly on-device without third-party data tracking.

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "Why do Universal Links frequently fail on iOS, and how do you debug them?"
* **Answer**:
  1. **Domain Verification Failure**: The Apple App Site Association (`apple-app-site-association` or AASA file) must be hosted at `https://<domain>/.well-known/apple-app-site-association` with a valid SSL certificate and `application/json` MIME type without `.json` extension.
  2. **Apple CDN Cache**: Apple routes AASA scraping through its own CDN cache. Changes to AASA can take up to 48 hours to propagate to devices.
  3. **User Opt-Out**: If a user taps the domain button in the top-right corner of Safari after following a Universal Link, iOS remembers that the user prefers Safari, disabling Universal Links for that domain until manually re-enabled.

### Q2: "How does Deferred Deep Linking work when clipboard access is restricted on modern iOS/Android versions?"
* **Answer**:
  - Historically, SDKs copied the click identifier to the system clipboard and read it on first app launch.
  - Starting with iOS 14 and Android 12, the OS displays invasive clipboard snooping toast warnings ("App pasted from Safari").
  - Modern deferred deep linking uses **Native Install Referrers**:
    - **Google Play Install Referrer API**: Google Play securely passes the click referrer URL directly to the app during `onReceive` or via Play Services API.
    - **Apple SKAdNetwork / Private Click Measurement**: Cryptographic attribution tokens verified on first launch.
