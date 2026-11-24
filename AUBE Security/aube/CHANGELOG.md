# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-23

### Added

- AUBE Portal 1.2.0 events (schema 1.1) list the server's IP addresses: its own
  addresses go to `host.ip`, together with `host.hostname`, and addresses several
  servers appear behind (NAT, bastion) to `aube.server.shared_ip_addresses`
- The analyst's evaluation comment, when AUBE Portal sends it, to
  `aube.evaluation.comment`
- The AI Evaluation Assistant's explanation the analyst saw when confirming,
  when AUBE Portal sends it, to `aube.evaluation.ai_comment`
- The AI Evaluation Assistant's own evaluation of the period, when AUBE Portal
  sends AI explanations and the analyst had one on screen when confirming
  (event schema 1.2): `aube.evaluation.ai_verdict`,
  `aube.evaluation.ai_risk_level` and `aube.evaluation.ai_confidence`
  (keywords, the same values whatever the analyst's language, so a rule can
  match them) and `aube.evaluation.ai_reason` (text, at most 2,000
  characters). They are the model's opinion and are not AUBE's severity or
  score
- Schema 1.0 events are parsed as before

## [1.0.0] - 2026-11-04

### Added

- Initial format for AUBE Portal's Sekoia event schema v1 (confirmed anomalies, withdrawals, test events)
