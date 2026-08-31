# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-28

### Added

- Parse new ECS fields for ITDR events (`event.dataset: ITDR`, `event.action: New alert created`):
  - `event.outcome`
  - `event.severity`
  - `event.url`
- Parse new custom fields for ITDR events (`event.dataset: ITDR`, `event.action: New alert created`):
  - `cyberark.audit.status`
- Normalize ITDR `event.outcome` to ECS value `unknown` and preserve raw status in `cyberark.audit.status`
- Add anonymized ITDR test fixtures from raw CSV logs
