# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-11-12

### Added

- Parse new custom fields:
  - `action.properties.ScriptBlockSize`: compute the UTF-8 byte size of `action.properties.ScriptBlockText` from raw field `action.properties.ScriptBlockText` and skip empty values

## [1.0.2] - 2026-10-15

### Changed

- Add the Windows ARM64 download link to the intake description, next to the Windows x86-64 one

## [1.0.1] - 2026-10-02

### Fixed

- Fix existing ECS fields:
  - `event.outcome`:
    - prevent Linux and non-Windows events from inheriting Windows auth outcome rules derived from `action.properties.EventType` or `event.code`
  - `host.os.type`: apply Windows fallback only when host OS type is missing to avoid overriding explicit Linux host context
- Fix existing custom fields:
  - `sekoiaio.server.os.type`: apply Windows fallback only when host OS type is missing to avoid overriding explicit Linux host context

## [1.0.0] - 2024-08-22

### Added

- Add `action.properties.time_without_events` field to taxonomy
