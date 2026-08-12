# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.8] - 2026-08-12

### Added

- Parse new custom fields:
    - `microsoft.defender.url_chain`

## [1.0.7] - 2026-08-12

### Fixed

- Fix `TypeError` on `email.from.address` ECS field parsing, caused by attempting to read sender values from `Entities` when `Entities` is absent/empty
- Harden `Entities`-based field extraction with null/empty checks

## [1.0.6] - 2026-07-20

### Added

- Parse custom fields:
    - `microsoft.defender.threat.last_verdict`
    - `microsoft.defender.threat.verdict`

## [1.0.5] - 2025-09-01

### Fixed

- Add remote device name in DeviceLogonEvents

## [1.0.4] - 2025-08-06

### Fixed

- Fix url domain when uri is present

## [1.0.3] - 2025-07-18

### Fixed

- Fix process fields in some categories

### Changed

- Add more fields and test

## [1.0.2] - 2023-12-07

### Fixed

- Fix process fields in some categories

## [1.0.1] - 2023-12-07

### Changed

- Extract more data
