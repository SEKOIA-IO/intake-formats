# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-08-25

### Fixed

- Anonymize all JSON test fixtures by replacing non-example email domains and non-reserved IP values with RFC 5737 test ranges, while preserving parsing-relevant value shapes

### Removed

- Remove parsing of credential-like password values from incident payloads to prevent high-risk exposure of raw secrets in normalized events
- Remove custom fields:
  - `fortinet.fortigate.password`

## [1.0.2] - 2026-08-14

### Added

- Improve Incident Detection parsing coverage by extracting nested incident payload values into ECS and Fortinet-specific fields for better investigation context
- Parse new ECS fields:
  - `action.outcome_reason`
  - `destination.ip`
  - `destination.port`
  - `event.action`
  - `event.reason`
  - `network.protocol`
  - `observer.hostname`
  - `observer.version`
  - `source.ip`
  - `source.mac`
  - `source.port`
  - `source.user.email`
  - `threat.technique.id`
  - `user.email`
- Parse new custom fields:
  - `fortinet.fortigate.decoy.group`
  - `fortinet.fortigate.decoy.type`
  - `fortinet.fortigate.incident.event_id`
  - `fortinet.fortigate.incident.id`
  - `fortinet.fortigate.loghost`
  - `fortinet.fortigate.operation`
  - `fortinet.fortigate.tag.id`
  - `fortinet.fortigate.tag.key`
  - `fortinet.fortigate.tzone`
  - `fortinet.fortigate.ui`
  - `fortinet.fortigate.username`
  - `fortinet.fortigate.xauth.group`
  - `fortinet.fortigate.xauth.user`
- Add VPN XAuth identity support to preserve authenticated user/group values and improve identity fidelity in VPN events

### Changed

- Update ECS fields:
  - `@timestamp`
- Refine VPN identity mapping logic to prefer XAuth user data when `user` is missing, placeholder, or IP-based, while keeping existing mappings for valid usernames

### Fixed

- Fix inconsistent VPN identity rendering where `user` can contain an IP address while the authenticated identity is only present in `xauthuser`

## [1.0.1] - 2023-10-23

### Added

- Extract the name of the attack from events
