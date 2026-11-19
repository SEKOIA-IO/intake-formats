# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add a dedicated parser for Palo Alto Cortex XDR v5 Issues API payloads.
- Document the separate Issues connector, its configuration and collection state.
- Test the minimal connector fixture, issue revisions, excluded issues and omitted optional fields.

### Changed

- Use `modification_time` as the event timestamp and retain its original millisecond value alongside the stable issue ID.
- Limit mappings and smart descriptions to verified Issues fields; remove unsupported assumptions about hosts, cases, status and MITRE labels.
- Preserve severity labels and exclusion booleans without inferring a numeric severity or a resolution status.
- Use the supported Application logs data source category for Issues updates.
