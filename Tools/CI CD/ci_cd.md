# 🚀 CI/CD for Mobile Apps
> **Targeted for Mobile DevOps & Leads**
> **Note:** Continuous Integration, Deployment pipelines, and automation.

![CI/CD](https://img.shields.io/badge/DevOps-CI%2FCD-blue?style=for-the-badge&logo=githubactions&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Concepts](#core-concepts)
- [2. Mobile-Specific Challenges](#mobile-specific-challenges)
- [3. Popular Tools](#popular-tools)
- [4. Best Practices](#best-practices)

---

### Q1. What is CI/CD and why is it important specifically for mobile?

**Answer:**
**CI (Continuous Integration)**: Merging code frequently (daily) to a shared repo, triggering automated builds and tests.
**CD (Continuous Delivery/Deployment)**: Automating the release process to testers (Beta) or users (Production).

**Importance for Mobile:**
- **Fragmentation**: Android/iOS have different build processes.
- **Binary Artifacts**: Unlike web, you produce a signed binary (`.apk`, `.ipa`).
- **Review Times**: App Store reviews take time; automating the submission reduces the manual overhead.

### Q2. Typical Mobile CI/CD Flow?

**Answer:**
1.  **Push Code**: Dev pushes to `develop` or `main`.
2.  **Lint & Test**: Run Lint, Detekt, Unit Tests.
3.  **Build**: Assemble Debug/Release builds.
4.  **UI Test**: Run Espresso/XCTest on Emulators/Devices (e.g., Firebase Test Lab).
5.  **Sign**: Sign the artifact (Keystore/Certificate).
6.  **Distribute**:
    - **Alpha/Beta**: Upload to Firebase App Distribution / TestFlight.
    - **Production**: Upload to Play Console / App Store.

### Q3. Environment Variables & Secrets?

**Answer:**
**Never commit secrets** (API Keys, Keystore passwords) to Git.
- **CI Secrets**: Store them in the CI provider's secret manager (e.g., GitHub Secrets, Bitrise Secrets).
- **Injection**: Inject them during the build process into `local.properties` or environment variables accessible by Gradle/Fastlane.

### Q4. Build Flavors in CI?

**Answer:**
CI pipelines key off the branch name or tags:
- `feature/*` -> Runs Lint + Unit Tests.
- `develop` -> Builds `debug` flavor + Distributes to QA.
- `main` -> Builds `release` flavor + Uploads to Store.

---
