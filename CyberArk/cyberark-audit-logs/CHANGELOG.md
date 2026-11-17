# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-22

### Changed

- Extend parsing of existing ECS fields:
  - `event.severity`: map from `customData.nested_items[name=Severity].value` with fallback to `customData.Severity`
  - `event.url`: map from `customData.nested_items[name=Alert_link].value` with fallback to `customData.Alert_link`
- Extend parsing of existing custom fields:
  - `cyberark.audit.status`: map from `customData.nested_items[name=Status].value` with fallback to `customData.Status`
- Split ITDR parser logic into dedicated `nested`, `flat`, and `derived` stages with explicit priority and fallback

### Fixed

- Fix parsing of existing ECS fields:
  - `event.outcome`: set `unknown` for ITDR alert-creation events instead of inferring from alert triage `Status`

## [1.0.0] - 2026-09-09

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
