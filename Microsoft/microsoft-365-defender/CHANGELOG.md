# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-12 - 1.0.7

### Fixed

- Fix `TypeError` on `email.from.address` ECS field parsing, caused by attempting to read sender values from `Entities` when `Entities` is absent/empty
- Harden `Entities`-based field extraction with null/empty checks
## 2026-07-20 - 1.0.6

### Added

- Parse custom fields:
    - `microsoft.defender.threat.last_verdict`
    - `microsoft.defender.threat.verdict`

## 2025-09-01 - 1.0.5

### Fixed

- Add remote device name in DeviceLogonEvents

## 2025-08-06 - 1.0.4

### Fixed

- Fix url domain when uri is present

## 2025-07-18 - 1.0.3

### Fixed

- Fix process fields in some categories

### Changed

- add more fields and test

## 2023-12-07 - 1.0.2

### Fixed

- Fix process fields in some categories

## 2023-12-07 - 1.0.1

### Changed

- extract more data
