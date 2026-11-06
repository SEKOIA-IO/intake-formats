# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-03

### Added

- Add parsing support for `Result description: Processing error` events by extending `set_not_processed_fields` filter (shared stage)
- Newly populated ECS fields for `Processing error` events (existing field names, no schema addition):
    - `event.action`
    - `event.category`
    - `event.module`
    - `event.reason`
    - `event.type`
    - `file.directory`
    - `file.name`
    - `process.executable`
    - `process.pid`
    - `user.domain`
    - `user.name`

### Changed

- Modify parsing logic for existing ECS fields in `set_not_processed_fields`:
    - `event.reason`
    - `process.executable`
    - `user.domain`
    - `user.name`
- Improve parsing for `Not processed` events when optional fields are missing
- Improve user parsing robustness for identities with spaces in domain names (for example `NT AUTHORITY\\SYSTEM`)

### Fixed

- Fix `TypeError` in `set_not_processed_fields` when `Reason` is missing by making `event.reason` null-safe
- Fix `TypeError` in `set_not_processed_fields` when `Application path` or `Name` is missing by making `process.executable` null-safe
- Normalize `process.executable` path composition for `Not processed` events

## 2023-12-20

### Add

- Add for the first time the kaspersky endpoint security
