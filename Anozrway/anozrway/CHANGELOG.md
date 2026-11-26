# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-26

### Added

- Add the Anozr Way format to parse the new professional leaks of an individual (`new_pro_leaks`) and the individuals reaching a high risk (`new_high_risk_individual`)
- Add smart descriptions for both event types
- Add the rules Individual Password Exposed, Individual Exposed By An Infostealer and Individual Reaching A High Risk
- Parse new ECS fields:
  - `@timestamp`
  - `event.action`
  - `event.category`
  - `event.dataset`
  - `event.kind`
  - `event.provider`
  - `event.risk_score`
  - `event.type`
  - `observer.product`
  - `observer.type`
  - `observer.vendor`
  - `threat.indicator.first_seen`
  - `threat.indicator.provider`
  - `threat.indicator.type`
  - `user.email`
  - `user.id`
  - `user.name`
- Parse new custom fields:
  - `anozrway.event_id`
  - `anozrway.exposed_data_types`
  - `anozrway.leak_date`
  - `anozrway.leak_type`
  - `anozrway.source_key`
  - `anozrway.threat_scores.account_takeover`
  - `anozrway.threat_scores.coercion`
  - `anozrway.threat_scores.identity_theft`
  - `anozrway.threat_scores.phishing`
