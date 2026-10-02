# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-02

### Fixed

- Fix existing ECS fields:
  - `host.os.type`: apply Windows fallback only when host OS type is missing to avoid overriding explicit Linux host context
  - `event.outcome`:
    - prevent Linux and non-Windows events from inheriting Windows auth outcome rules derived from `action.properties.EventType` or `event.code`
    - normalize to ECS values (`success`, `failure`, `unknown`) and fallback to `unknown` when deterministic success/failure mapping is not possible
- Fix existing custom fields:
  - `sekoiaio.server.os.type`: apply Windows fallback only when host OS type is missing to avoid overriding explicit Linux host context

## 2024-08-22

### Added

- Add `action.properties.time_without_events` field to taxonomy
