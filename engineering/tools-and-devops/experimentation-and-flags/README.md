# 🎛️ Feature Flags, Progressive Delivery & Experimentation (A/B Testing)

> **Decouple deployment from release: Instant kill switches, canary percentage rollouts, warehouse-native experimentation, and statistical rigor using Split.io, LaunchDarkly, and Eppo.**

![Flags](https://img.shields.io/badge/Discipline-Feature_Delivery_&_Experimentation-blue?style=for-the-badge)

---

## 📖 Module Guides

| Guide | Description | Key Focus |
| :--- | :--- | :--- |
| **[01. Split.io & Enterprise Feature Flags](./01_split_io_and_feature_flags.md)** | Progressive rollouts & safety kill switches. | Local evaluation in-memory cache, background SSE streaming, instant emergency kill switches without app store releases, and LaunchDarkly comparison. |
| **[02. Eppo & Statistical A/B Testing](./02_eppo_and_ab_testing.md)** | Modern statistical A/B testing platforms. | Warehouse-native experimentation (Snowflake/BigQuery), CUPED variance reduction (50% faster experiments), Sample Ratio Mismatch (SRM) detection, and guardrail metric tracking. |
| **[03. LaunchDarkly Enterprise Feature Flags](./03_launchdarkly_enterprise_flags.md)** | The enterprise gold standard in progressive delivery. | Server-Sent Events (SSE) edge streaming (<200ms latency), offline caching, multivariate user targeting, clean repository wrapper pattern, and automated circuit breakers. |
| **[04. Statsig Feature Gates & Pulse Metrics](./04_statsig_modern_feature_gates.md)** | Unified feature management and automated health gating. | Feature gates, dynamic runtime configurations, automated pulse health metrics (crash/latency correlation), global holdouts, and multi-team layer isolation. |

---

[⬅️ Back to Tools & DevOps Overview](../README.md)
