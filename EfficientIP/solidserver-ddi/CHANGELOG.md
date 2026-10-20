# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-09-03

### Added

- Parse new ECS fields:
  - `event.action` for DNS "received notify" events
  - `event.outcome` for DNS zone transfer allowed/denied events
  - `source.address` when RPZ source is logged as a hostname

### Changed

- Anonymize and harmonize JSON test fixtures naming

### Fixed

- Support signed DNS update logs with TSIG key suffix in the DNS header

## [1.0.1] - 2024-06-10

### Fixed

- Remove syslog header from the tests and the grok pattern
- Add support for DNS Guardian list logs
