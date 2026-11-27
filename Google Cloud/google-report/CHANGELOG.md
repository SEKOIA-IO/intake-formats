# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix parsing of existing ECS fields:
  - `user.name`: use the actor's full email address instead of its local part to prevent merging accounts from different domains; keep the actor's `user.email`, `user.id`, and `user.domain`. Explicit ChromeOS usernames from `DEVICE_USER` remain supported.

## [1.17.4] - 2026-11-02

### Added

- Parse new custom fields:
  - `google.report.meet.organizer_email`: map from raw field `organizer_email` to store the Google Meet organizer email separately from the participant identity

### Fixed

- Fix parsing of existing ECS fields:
  - `user.email`: stop populating with the Google Meet organizer email

## [1.17.3] - 2023-03-14

### Changed

- Add stages to improve the parser
