# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-11-19

### Added

- Parse WithSecure Elements inbox rule scan events (`inboxRuleScan`)
- Parse new ECS fields:
  - `user.email`: map `details.userPrincipalName` when no `userName` is provided, for inbox rule scan and email scan events
- Parse new custom fields:
  - `withsecure.inbox_rule.name`: map `details.inboxRuleName` for inbox rule scan events
- Add a smart description for inbox rule scan events

### Changed

- Extend parsing of existing ECS fields:
  - `event.category`: set to `email` for inbox rule scan events
  - `event.type`: set to `info` for inbox rule scan events
  - `service.type`: map `details.serviceType` for inbox rule scan events

### Fixed

- Fix existing ECS fields:
  - `user.name`: map `details.userPrincipalName` when no `userName` is provided, so Microsoft 365 cloud events (inbox rule scan, email scan) are attributed to their user

## [1.0.0] - 2023-10-02

### Changed

- Remove beta flag
