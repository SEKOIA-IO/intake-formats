# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
