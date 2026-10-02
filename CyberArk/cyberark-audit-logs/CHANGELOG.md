# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-29

### Fixed

- Extend ITDR field extraction to support new nested-key extraction from raw field `customData.nested_items`, while preserving existing flat-key extraction from raw field `customData.*`:
  - ECS fields:
    - `event.outcome`
    - `event.severity`
    - `event.url`
  - custom fields:
    - `cyberark.audit.status`
- Split ITDR parser logic into dedicated stages with explicit priority and fallback (`nested` stage first, then `flat` fallback when nested values are missing)

## 2026-09-09

### Added

- Parse new ECS fields for ITDR events (`event.dataset: ITDR`, `event.action: New alert created`):
  - `event.outcome`
  - `event.severity`
  - `event.url`
- Parse new custom fields for ITDR events (`event.dataset: ITDR`, `event.action: New alert created`):
  - `cyberark.audit.status`
- Add anonymized ITDR test fixtures from raw CSV logs

### Fixed

- Normalize ITDR `event.outcome` from `customData.Status` (only when it is present) with ECS semantics: `success`/`failure` when resolvable, `unknown` otherwise
