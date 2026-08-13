# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.3] - 2026-08-11

### Added

- Parse new ECS fields in the `network_info` stage:
  - `destination.bytes`
  - `source.bytes`
- Parse new custom fields in the `network_info` stage:
  - `harfanglab.network.kind`

### Changed

- Update DNS resolution parsing to support values under `details_dns_resolution`
- Improve parsing of ECS fields:
  - `dns.question.name`
  - `dns.question.name`
  - `dns.resolved_ip`
- Improve parsing of custom fields:
  - `harfanglab.dns.raw_windows_resolver_results`

## [1.3.2] - 2026-08-11

### Fixed

- Parse ECS fields from raw field `message.event_id` with fallback to `message.eventlog.event_id` for eventlog alerts:
  - `action.id`
  - `event.code`

## [1.3.1] - 2026-08-04

### Fixed

- Parse new ECS fields from `agents[0].agent_hostname` on threat events:
  - `host.hostname`
  - `host.name`

## [1.3.0] - 2024-12-11

### Changed

- Split username into `user.name` and `user.domain`

## [1.2.0] - 2024-10-01

### Added

- Add some extra fields

## [1.1.1] - 2024-01-18

### Fixed

- retrieve file name
- retrieve registry value

## [1.1.0] - 2023-12-04

### Changed

- parse more log types
