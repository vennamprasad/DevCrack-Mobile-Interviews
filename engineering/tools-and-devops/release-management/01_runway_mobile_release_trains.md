# 🚂 Runway: Mobile Release Train Orchestration & Phased Rollouts

> **Mastering the mobile release cycle: Coordinating multi-team release trains, automated code freezes, App Store & Google Play staged rollouts, and stability health gating.**

---

## 📌 Executive Summary

Unlike web engineering—where code can be deployed continuously to production servers in seconds—**mobile engineering suffers from asymmetric, gatekept distribution**:
1. Binary reviews take 2 to 48 hours in Apple App Review and Google Play Console.
2. Users do not update simultaneously; old versions live in the wild for months.
3. Once a bug is packaged into a released IPA/APK, **you cannot undo it** without building a new binary and re-submitting it.

**Runway** is the mobile DevOps platform that automates this entire release lifecycle, integrating GitHub/GitLab, CI/CD (Fastlane/Bitrise), App Store Connect, Google Play, Sentry/Datadog, and Slack into a unified release train.

---

## 🏗️ The Modern Mobile Release Train Model

```
 Week 1: Development          Week 2: Code Freeze & QA          Week 3: Phased Rollout
[ Feature Branches Merged ] ──> [ Cut Release Branch ]   ──> [ 1% Canary Rollout ]
                                [   (release/v3.2.0) ]               │
                                        │                      (Health Gate Passed)
                                        ▼                            ▼
                                [ Regression Suite ]     ──> [ 5% -> 20% Rollout ]
                                [ Automated Fastlane ]               │
                                        │                      (Health Gate Passed)
                                        ▼                            ▼
                                [ App Store Approval ]   ──> [ 50% -> 100% Release ]
```

---

## ⏱️ Staged Rollout Strategies Compared

Both Apple and Google provide mechanisms to roll out updates to a percentage of users, protecting the broader install base against catastrophic zero-day regressions.

### Apple Phased Release vs. Google Play Staged Rollout

| Feature | Apple App Store (Phased Release) | Google Play (Staged Rollout) |
| :--- | :--- | :--- |
| **Schedule Control** | Fixed 7-day automatic curve:<br>• Day 1: 1%<br>• Day 2: 2%<br>• Day 3: 5%<br>• Day 4: 10%<br>• Day 5: 20%<br>• Day 6: 50%<br>• Day 7: 100% | Custom percentage configurable at any time (e.g., 2.5%, 10%, 25%, 50%, 100%). |
| **Manual Pause** | Can be paused for up to **30 consecutive days**. | Can be halted indefinitely. |
| **User Search / Manual Update** | Users can bypass the rollout by searching the app in App Store and tapping "Update". | Users chosen at random by Google Play; manual update honors rollout pool. |
| **Hotfix Strategy** | Must submit a new version (e.g., v3.2.1); resets the 7-day phased clock. | Can update the existing staged rollout percentage with a newer build code. |

---

## 🛡️ Stability Gating (Automated Circuit Breakers)

Never rely on manual human vigilance to catch release regressions. Runway connects APM telemetry (Sentry/Datadog) directly to store rollout APIs.

```
                  [ Staged Rollout Active at 10% ]
                                 │
                                 ▼
                     [ Real-Time Health Gate ]
                     (Monitoring Sentry / DD)
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
       [ Health Metrics Nominal ]      [ Stability Breach! ]
       • Crash-Free > 99.8%            • Crash-Free < 99.5% OR
       • ANR Rate < 0.40%              • User-Reported Bad Reviews Spike
                 │                               │
                 ▼                               ▼
       [ Advance to 20% Pool ]         [ AUTOMATIC ROLLOUT HALT ]
                                       • Store Rollout paused instantly
                                       • PagerDuty alert to Release Captain
                                       • Hotfix branch automatically cut
```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you coordinate a release train across 20+ feature teams without blocking the train when one team's feature fails QA?"
* **Answer**:
  1. **Strict Decoupling via Feature Flags**: No team is allowed to delay a release train due to incomplete or buggy code. All new features MUST be merged behind a feature flag (LaunchDarkly/Statsig).
  2. If Team X's feature is broken during the release regression window, **do not revert the commit** (which can introduce merge conflicts with other teams' work). Simply flip the feature flag to `OFF` for the release build.
  3. The train leaves on time. The feature can be polished and tested for the subsequent release train.

### Q2: "What is Google's 'Android Vitals Bad Behavior Threshold', and how does it impact Play Store distribution?"
* **Answer**:
  - Google Play Console enforces strict **Core Vital thresholds**:
    - **User-perceived Crash Rate**: Maximum **1.09%** across all devices (or >8% on any individual phone model).
    - **User-perceived ANR Rate**: Maximum **0.47%** across all devices.
  - **Penalty**: If an app exceeds either threshold, Google Play algorithms automatically **penalize search ranking**, remove the app from recommendation carousels, and display an explicit warning on the Play Store listing ("This app may stop working on your device").
