# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-13

### Added

- Support PAN-OS audit subtype CSV events (audit logger), including `GRP_MGMT` events carrying embedded Linux `auditd` payloads in `EventDescription`
- Parse new ECS fields:
  - `action.outcome`
  - `action.type`
  - `event.action`
  - `event.category` for audit events
  - `event.code`
  - `event.outcome`
  - `event.type` for audit events
  - `process.executable`
  - `process.name`
  - `process.pid`
  - `related.user`
  - `user.id`
  - `user.name`

### Changed

- Update `action.name` mapping for PAN-OS audit subtype events (map from audit object value `log-critical-activity`)
- Normalize quote handling for audit `exe` and `acct` values to support both escaped and unescaped forms

## 2025-16-01

- Add parsing of session.id and session.endreason

## 2025-07-01

- Always display url.original

## 2024-15-01

### Update

- Change to timestamp of all types
