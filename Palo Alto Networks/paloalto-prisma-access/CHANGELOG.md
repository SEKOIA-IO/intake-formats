# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-11-12

### Changed

- Extend parsing of existing ECS fields:
  - `event.outcome`: parse `EventStatus` (`success` or `failure`) for GlobalProtect events in JSON format
- Extend parsing of existing custom fields:
  - `action.name`: parse `EventIDValue` for GlobalProtect events in JSON format
  - `action.outcome`: parse `EventStatus` for GlobalProtect events in JSON format

### Fixed

- Fix parsing of existing ECS fields:
  - `event.reason`: parse `ConnectionError` before `Description` for GlobalProtect events in JSON format
  - `url.original`: no longer set to `https://` when `URL`, `FileName` and `URLFilename` are empty

## [1.0.0] - 2024-10-08

### Added

- Creation of the format
