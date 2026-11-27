# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.1] - 2026-11-23

### Fixed

- Fix existing ECS fields:
  - `event.outcome`:
    - stop setting to `success` by default on every event
    - set to `failure` on connection ends (`Connection closed by`, `Disconnected from`, `Received disconnect from`, `Connection reset by`) that happen before authentication (`[preauth]`) or for an `invalid user` or `illegal user`, set to `failure` on `pam_unix(sshd:auth): check pass; user unknown`, keep `success` on `Accepted` authentications
- Fix existing custom fields:
  - `action.outcome`: set to `failure` on the same events as `event.outcome`

## [2.0.0] - 2024-01-17

### Changed

- Migrate parser

### Fixed

- Fix existing ECS fields:
  - `action.name`: rename `negociate` to `negotiate`
  - `action.outcome_reason`:
    - keep the full disconnect reason (e.g. `Normal Shutdown, Thank you for playing` instead of `Normal Shutdown`)
    - keep the full PAM message (e.g. `pam_unix(sshd:auth): check pass; user unknown` instead of `pam_unix(sshd:auth): check pass`)
  - `event.outcome`: set from the event result instead of the parsing status (e.g. a failed authentication gives `failure`)
