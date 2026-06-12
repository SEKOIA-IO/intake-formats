# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [Unreleased] - 2026-06-12

### Added

- Parse new dynamic fields:
    - destination.as.organization.name
    - destination.domain
    - destination.geo.country_name
    - destination.ip
    - destination.mac
    - destination.port
    - event.severity
    - file.name
    - network.application
    - observer.name
    - rule.id
    - source.as.organization.name
    - source.geo.city_name
    - source.geo.country_name
    - source.ip
    - source.mac
    - source.port
- Parse new custom fields:
    - trendmicro.visionone.oat.attackphase.source
    - trendmicro.visionone.oat.attackphase.target
    - trendmicro.visionone.oat.count
    - trendmicro.visionone.oat.malName
    - trendmicro.visionone.oat.malType
    - trendmicro.visionone.oat.riskLevel (extended fallback mapping)
    - trendmicro.visionone.oat.threatType

### Changed

- Complete the parsing of existing dynamic fields:
    - event.provider
    - host.name
    - observer.product
    - process.executable
    - rule.name
    - threat.tactic.id
    - url.original
    - user.domain
    - user.name
- Complete the parsing of existing custom fields:
    - trendmicro.visionone.oat.riskLevel

### Fixed

- Anonymize JSON test files
