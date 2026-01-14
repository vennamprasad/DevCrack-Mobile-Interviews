# 🏎️ Fastlane Automation
> **Targeted for Mobile Developers**
> **Note:** Automating screenshots, beta deployment, and store releases.

![Fastlane](https://img.shields.io/badge/Tool-Fastlane-00F200?style=for-the-badge&logo=fastlane&logoColor=white)

---

## 📖 Table of Contents
- [1. What is Fastlane?](#what-is-fastlane)
- [2. Lanes & Fastfile](#lanes--fastfile)
- [3. Match (Code Signing)](#match-code-signing)
- [4. Supply & Deliver](#supply--deliver)

---

### Q1. What is Fastlane?

**Answer:**
Fastlane is an open-source tool written in Ruby that automates the tedious tasks of mobile development. It handles:
- **Building**: `gym` (iOS), `gradle` (Android).
- **Signing**: `match` (iOS).
- **Screenshots**: `snapshot` (iOS), `screengrab` (Android).
- **Releasing**: `deliver` (iOS), `supply` (Android).

### Q2. Anatomy of a Fastfile?

**Answer:**
The `Fastfile` defines your automation "lanes".
```ruby
default_platform(:android)

platform :android do
  desc "Run tests"
  lane :test do
    gradle(task: "test")
  end

  desc "Deploy to Beta"
  lane :beta do
    gradle(task: "assembleRelease")
    firebase_app_distribution(
        app: "1:1234567890:android:321abc",
        groups: "testers"
    )
  end
end
```

### Q3. What is `match`?

**Answer:**
**`match`** is a Fastlane tool for iOS code signing. It syncs certificates and provisioning profiles via a private Git repository. It solves the "It works on my machine" signing issue by ensuring the whole team (and CI) uses the *exact same* credentials.

### Q4. Common Actions?

**Answer:**
- **`scan`**: Run iOS tests.
- **`gym`**: Build iOS app.
- **`slather`**: Generate coverage reports.
- **`supply`**: Upload metadata & binaries to Google Play.
- **`deliver`**: Upload metadata, screenshots & binaries to App Store Connect.
