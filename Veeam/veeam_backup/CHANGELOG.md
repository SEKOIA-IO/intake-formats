# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-23

### Added

- Parse new ECS fields:
  - `observer.hostname`: identify the Veeam backup server host from `VbrHostName`
  - `observer.version`: identify the Veeam Backup & Replication version from `VbrVersion`

### Fixed

- Ensure `DateTime` is parsed reliably without `parsed_date` errors:
  - unwrap JSON-encapsulated syslog events before KV parsing
  - strip optional syslog/origin prefixes with a dedicated transport grok stage
  - feed the extracted bracket payload to KV/date parsing
