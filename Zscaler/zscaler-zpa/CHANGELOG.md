# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-07

### Added

- Parse new ECS fields:
  - `error.message` (extended with fallback from `InternalReason` when `PRAErrorStatus` is empty)
  - `network.application`
  - `rule.id`
  - `rule.name`
  - `user.target.name`
- Parse new custom fields:
  - `zscaler.zpa.pra.approval_id`
  - `zscaler.zpa.pra.capability_policy_id`
  - `zscaler.zpa.pra.connection_id`
  - `zscaler.zpa.pra.credential_login_type`
  - `zscaler.zpa.pra.credential_policy_id`
  - `zscaler.zpa.pra.file_transfer_list`
  - `zscaler.zpa.pra.recording_status`
  - `zscaler.zpa.pra.session_type`
  - `zscaler.zpa.pra.shared_mode`
  - `zscaler.zpa.pra.shared_users_list`

## [1.0.0] - 2026-02-13

### Added

- Initial version of the format
