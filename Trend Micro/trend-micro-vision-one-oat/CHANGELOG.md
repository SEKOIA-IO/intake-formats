# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-26

### Fixed

- Build lists and dicts without mutating them in place (`.append`, `.update`, ...), which not every Jinja engine supports

## [1.0.1] - 2026-11-16

### Added

- Parse new custom fields:
  - `action.properties.ScriptBlockSize`: compute the UTF-8 byte size of `action.properties.ScriptBlockText` from raw field `detail.objectRawDataStr`, keep the largest value when multi-valued and skip empty values

## [1.0.0] - 2026-06-15

### Added

- Parse new ECS fields:
  - `destination.as.organization.name`
  - `destination.domain`
  - `destination.geo.country_name`
  - `destination.ip`
  - `destination.mac`
  - `destination.port`
  - `event.severity`
  - `file.name`
  - `network.application`
  - `observer.name`
  - `source.as.organization.name`
  - `source.geo.city_name`
  - `source.geo.country_name`
  - `source.ip`
  - `source.mac`
  - `source.port`
- Parse new custom fields:
  - `trendmicro.visionone.oat.attackphase.source`
  - `trendmicro.visionone.oat.attackphase.target`
  - `trendmicro.visionone.oat.count`
  - `trendmicro.visionone.oat.filter.id`
  - `trendmicro.visionone.oat.malName`
  - `trendmicro.visionone.oat.malType`
  - `trendmicro.visionone.oat.riskLevel` (extended fallback mapping)
  - `trendmicro.visionone.oat.threatType`

### Changed

- Extend the parsing of existing ECS fields:
  - `event.provider`
  - `host.name`
  - `observer.product`
  - `process.executable`
  - `rule.name`
  - `threat.tactic.id`
  - `url.original`
  - `user.domain`
  - `user.name`
- EXtend the parsing of existing custom fields:
  - `trendmicro.visionone.oat.riskLevel`

### Fixed

- Anonymize JSON test files
  - IP addresses
  - domains
  - hostnames
  - usernames
- Cast some fields with the right type to match the ECS reference
