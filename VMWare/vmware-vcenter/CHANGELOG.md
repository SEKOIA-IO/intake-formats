# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-10-06

### Added

- Parse new ECS fields:
  - for `Modify Entry` events:
    - `event.action`
  - for `SSO group management` events (`Adding users to group`):
    - `event.action`
    - `event.category`
    - `event.reason`
    - `event.type`
    - `group.name`
    - `related.user`
    - `user.domain`
    - `user.name`
    - `user.roles`
    - `user.target.domain`
    - `user.target.name`
- Parse new custom fields:
  - for `Modify Entry` events:
    - `vmware_vcenter.entry_cn`
  - for `SSO group management` events (`Adding users to group`):
    - `vmware_vcenter.target_user_domains`
    - `vmware_vcenter.target_user_names`
    - `vmware_vcenter.user_role`

### Changed

- Normalize group membership description as `User added to '{group.name}' group`

## [1.0.2] - 2026-09-28

### Fixed

- Fix existing ECS fields:
  - `host.ip`: stop populating `host.ip` from `user@IP` session events
  - `source.ip`: parse client IP extracted from `user@IP` session events (login, logout, bad username, SSH session)

## [1.0.1] - 2026-08-14

### Added

- Parse new ECS fields:
  - `service.name`

## [1.0.0] - 2023-10-02

### Changed

- Remove beta flag
