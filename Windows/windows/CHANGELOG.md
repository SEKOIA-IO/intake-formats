# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2026-10-30

### Fixed

- Split `TargetUserName` in UPN format (`user@domain`) into `user.target.name` and `user.target.domain`

## [1.0.4] - 2026-10-20

### Changed

- Extend parsing of existing custom fields:
  - `action.properties.Path` from PowerShell event message payloads when top-level `Path` is absent or empty

## [1.0.3] - 2026-09-30

### Added

- Parse new custom fields:
  - `action.properties.DnsHostName` for computer account change events
  - `action.properties.PasswordLastSet` for account-management events

## [1.0.2] - 2026-09-10

### Added

- Parse new custom fields:
  - `action.properties.ImpersonationLevel` for Windows 4624 events (`An account was successfully logged on`)

## [1.0.1] - 2024-02-29

### Add

- Parse new ECS fields:
  - `registry.path`
