# Changelog

All notable changes to this parser will be documented in this file.

## [Unreleased]

## [1.0.0] - 2026-03-17

### Added

- Initial release of the Upwind Security parser
- JSON parsing of Upwind threat detection events from the `message` field
- ECS mapping: `observer`, `event`, `rule`, `cloud`, `threat` (MITRE ATT&CK tactic/technique), `user`, `host`, `related`
- Category-specific routing: `CLOUD_TRAIL` (AWS CloudTrail-based detections) and `API_SECURITY` (API threat detections)
- Custom fields under `upwind.*` namespace: `detection_type`, `status`, `occurrence_count`, `console_link`, `resource.*`, `policy_id`, `policy_name`
- Smart descriptions for alert summarization in Sekoia
- Test cases: `cloud_trail_security_group_0.json`, `api_security_0.json`