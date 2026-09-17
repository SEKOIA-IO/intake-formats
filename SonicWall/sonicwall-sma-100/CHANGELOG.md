# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2026-08-20

### Changed

- Deprecate _SonicWall/sonicwall-sma-100_ and recommend _SonicWall/sonicwall-sma-1000_ as replacement
- Align _SonicWall/sonicwall-sma-100_ manifest wording and naming conventions with _SonicWall/sonicwall-sma-1000_
- Replace legacy `data_sources` entry with normalized taxonomy keys:
  - `Authentication logs`
  - `Network device logs`
- Update ECS fields parsing:
  - `@timestamp`: add an explicit date format for `vp_time` parsing to improve timestamp parsing robustness
  - `event.dataset`: set value to `sonicwall.sma.100.sslvpn` for consistent event categorization
- Scope smart-descriptions to `event.dataset = sonicwall.sma.100.sslvpn` to avoid over-broad matching

## [1.1.0] - 2026-08-19

### Changed

- Rename _SonicWall/sonicwall-sma_ integration to _SonicWall/sonicwall-sma-100_

## [1.0.0] - 2023-10-11

### Added

- Initial version of the format
