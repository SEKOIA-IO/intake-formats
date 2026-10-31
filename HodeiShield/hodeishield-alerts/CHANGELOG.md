# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add the HodeiShield Alerts format for alerts delivered through HTTPS push.
- Normalize the alert title, type, severity, status, resolution and timestamps, and map `event_id` to `hodeishield.event_id`.
- Support status-change events (`event_type` `status_change`): `event.action` is `alert-status-changed`, `@timestamp` is the change time and `hodeishield.alert.previous_status` is set.
- Add smart descriptions and synthetic event fixtures.
- Parse the rating, third-party, DORA and endpoint agent alerts (`rating_critical`, `rating_drop`, `nth_party_risk`, `dora_incident_reportable`, `dora_incident_possible_major`, `agent_update_stalled`, `breach`): the `details` object is mapped to `hodeishield.alert.details.*`, with `event.action` taken from the event name, `host.id` from the endpoint identifier and `package.version` from the installed agent version.
- Categorize agent update alerts as `package` events.

### Fixed

- Categorize the `cve_critical` alerts as vulnerabilities, like `cve`.
