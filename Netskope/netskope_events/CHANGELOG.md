# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-11-16

### Added

- Parse new ECS fields:
  - `url.domain`: map from `details.diff.added` raw field key `exception/Domain` to normalize exception domain values into a standard ECS field for cross-source search and correlation
- Parse new custom fields:
  - `netskope.events.domain_notes`: map from `details.diff.added` raw field key `exception/Domain/Notes` to preserve exception-specific note context that has no direct ECS equivalent

## [1.0.1] - 2026-10-16

### Added

- Parse new ECS fields:
  - `user.target.email` for `Compromised Credential` alerts
- Parse new custom fields:
  - `netskope.alerts.breach_date` for `Compromised Credential` alerts

## [1.0.0] - 2026-08-14

### Added

- Parse new custom fields:
  - `netskope.events.record_type`
