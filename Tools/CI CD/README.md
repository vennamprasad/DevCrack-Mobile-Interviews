# 🚀 Mobile CI/CD & Fastlane Automation

> **Building automated pipelines for mobile engineering: GitHub Actions, Bitrise, Fastlane match code signing, test automation, and App Store / Play Store deployment.**

![CICD](https://img.shields.io/badge/DevOps-CI%2FCD-blue?style=for-the-badge&logo=githubactions&logoColor=white)
![Fastlane](https://img.shields.io/badge/Tool-Fastlane-00F200?style=for-the-badge&logo=fastlane&logoColor=white)

---

## 📖 Module Guides

| Guide | Description | Key Focus |
| :--- | :--- | :--- |
| **[Mobile CI/CD Pipeline Architecture](./ci_cd.md)** | Continuous integration pipelines for Android and iOS. | Runner selection (macOS vs Linux), caching Gradle/Cocoapods caches, secrets management, running unit/instrumentation tests, and artifact signing. |
| **[Fastlane Automation Guide](./fastlane.md)** | The standard mobile automation toolkit. | `Fastfile` lanes, `match` (deterministic Git-based iOS code signing), `supply` (Google Play deployment), and `deliver` (App Store submission). |
