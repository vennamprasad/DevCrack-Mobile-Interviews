# 🤖 iOS CI/CD
> **Targeted for DevOps & Leads**
> **Note:** Xcode Cloud, Fastlane, and Scripts.

![CI/CD](https://img.shields.io/badge/DevOps-CI%2FCD-black?style=for-the-badge&logo=githubactions&logoColor=white)

---

## 📖 Table of Contents
- [1. Xcode Cloud](#1-xcode-cloud)
- [2. Fastlane Match](#2-fastlane-match)
- [3. Versioning](#3-versioning)

---

### Q1. Xcode Cloud vs Others (Bitrise, CircleCI)?

**Answer:**
- **Xcode Cloud**: Integrated into Xcode. Free (limited hours). Deep integration with TestFlight. **Limitation**: Only for Apple platforms.
- **Bitrise/CircleCI**: More flexible. Supports Android/Web. More plugins.

### Q2. Automating Version Numbers?

**Answer:**
Using `agvtool` (Apple Generic Versioning Tool).
- **xcconfig**: `MARKETING_VERSION` (1.0), `CURRENT_PROJECT_VERSION` (42).
- **Fastlane**: `increment_build_number()` automatically bumps the build number based on TestFlight's latest upload or git commit count.

### Q3. What is Fastlane Match?

**Answer:**
Solves "Code Signing Hell".
It creates all certificates/profiles, stores them encrypted in a **private Git repo**, and syncs them to all developer machines and CI servers.
Command: `fastlane match development` / `fastlane match appstore`.

### Q4. dSYM Uploads?

**Answer:**
Required for Crashlytics/Sentry to symbolicate crashes.
- If Bitcode is enabled (deprecated), you must download dSYMs from App Store Connect first.
- If Bitcode is disabled, upload the dSYM generated during the CI Build directly to Crashlytics.
