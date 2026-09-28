# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Parse "Modify Entry" logs and extract:
  - `event.action`
  - `vmware_vcenter.entry_cn`
- Parse SSO group management logs for "Adding users to group" and extract:
  - acting user and domain
  - actor role
  - target user information
  - target group in `group.name`

### Changed

- Add normalized group membership change description: `User added to '{group.name}' group`

## 2026-08-14 - 1.0.1

### Added

- Parse new ECS fields:
  - `service.name`

## 2023-10-02 - 1.0.0

### Changed

- Remove beta flag
