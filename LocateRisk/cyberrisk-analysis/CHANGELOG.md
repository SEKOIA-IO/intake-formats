# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-06-22

### Added

- Set `event.type` to `["info"]`, `observer.type` to `scanner`, and `event.action` from the scanner finding type
- Add `locaterisk.location` field for scanned locations (URLs / host:port)
- Add a format-level logo

### Changed

- Map `event.category` to valid ECS categories (`vulnerability`, plus `network`/`web`/`threat`); every finding includes `vulnerability`
- Map scanned locations to `locaterisk.location` instead of `host.domain` (values are URLs / host:port, not DNS domain names)
- Move non-ECS custom fields to the vendor/product namespace: `locaterisk.cyberrisk_analysis.cves`, `locaterisk.cyberrisk_analysis.epss`, and `locaterisk.cyberrisk_analysis.false_positive` (previously under `vulnerability.*`), with `epss` typed as `scaled_float`
- Rename the format to `CyberRisk Analysis` and clarify the description as an EASM report

### Fixed

- Set `@timestamp` from the parsed log date instead of the ingestion time (`event.created`)
- Parse EPSS into a probability (0-1) by stripping the `%` before casting, instead of producing `0.0`

## 2026-05-28

### Changed

- Reformat files with linter and prettier
- Update test fixtures

## 2026-05-26

### Changed

- Refactor parser and expand smart descriptions

## 2026-04-22

### Changed

- Change `locaterisk.score` field type to scaled float

## 2026-04-20 - 1.0.0

### Added

- Add parser for LocateRisk CyberRisk Analysis CSV export
- Add module logo
