# Changelog

All notable changes to this parser will be documented in this file.

## [Unreleased]

## [1.0.0] - 2026-03-17

### Added

- Initial release of the Upwind Security parser
- JSON parsing of Upwind threat detection events from the `message` field
- ECS mapping: `observer`, `event`, `rule`, `cloud`, `threat` (MITRE ATT&CK tactic/technique), `user`, `host`, `related.user`
- Dataset mapping derived from Upwind category (e.g. `CLOUD_TRAIL` -> `event.dataset=cloud_trail`, `API_SECURITY` -> `event.dataset=api_security`)
- Custom fields under `upwind.*` namespace: `upwind.detection.*` (title, type, category, occurrences, status, resource.type, initiator.*) and `upwind.console_link`
- Smart descriptions for alert summarization in Sekoia
- Test cases: `cloud_trail_security_group_0.json`, `api_security_0.json`
