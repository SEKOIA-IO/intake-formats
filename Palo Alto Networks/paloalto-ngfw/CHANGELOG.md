# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-09

### Changed

- Extend parsing of existing ECS fields:
  - `destination.packets`: parse `PacketsReceived` in JSON TRAFFIC events, including zero values
  - `event.sequence`: parse the sequence number in CONFIG CSV events with or without change-detail columns
  - `source.packets`: parse `PacketsSent` in JSON TRAFFIC events, including zero values
  - `user.target.name`: extract the account name from CONFIG user-management XPath entries

### Fixed

- Fix existing ECS fields:
  - `event.category`: classify CONFIG events as configuration changes and include IAM for targeted accounts
  - `event.outcome`: normalize CONFIG results and report failed configuration changes as failures
  - `event.type`: classify CONFIG events as changes and include user events for targeted accounts
  - `observer.name`: map the device name from CONFIG CSV events with or without change-detail columns
- Fix existing custom fields:
  - `action.outcome`: normalize CONFIG results to `success` or `failure` consistently with `event.outcome`

## 2026-08-13

### Added

- Support PAN-OS audit subtype CSV events (audit logger), including `GRP_MGMT` events carrying embedded Linux `auditd` payloads in `EventDescription`
- Parse ECS fields for PAN-OS audit subtype CSV events (audit logger):
  - `action.outcome`
  - `action.type`
  - `event.action`
  - `event.category`
  - `event.code`
  - `event.outcome`
  - `event.sequence`
  - `event.type`
  - `group.name`
  - `process.command_line`
  - `process.executable`
  - `process.name`
  - `process.pid`
  - `related.user`
  - `user.id`
  - `user.name`
  - `user.target.name`

### Changed

- Update `action.name` mapping for PAN-OS audit subtype events (map from audit object value `log-critical-activity`)
- Normalize quote handling for audit `exe` and `acct` values to support both escaped and unescaped forms
- Keep `user.id` as actor UID and map `acct` to `user.target.name` while preserving `user.name` for compatibility

## 2025-16-01

- Add parsing of session.id and session.endreason

## 2025-07-01

- Always display url.original

## 2024-15-01

### Update

- Change to timestamp of all types
