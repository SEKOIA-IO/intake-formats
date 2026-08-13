# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-08-13

### Added

- Parse new ECS fields from `New Anti Virus` events:
  - `event.reason`
  - `event.risk_score`
  - `threat.software.name`
- Parse new custom fields from `New Anti Virus` events:
  - `checkpoint.malware_action_or_attack_information`
  - `checkpoint.malware_family`
  - `checkpoint.protection_name`
  - `checkpoint.protection_type`
  - `checkpoint.threat_prevention_rule_id`
- Parse malware fields from fixed label names (e.g., `Protection Type`, `Protection Name`, `Threat Prevention Rule ID`, `Malware Family`, `Confidence`, `Malware Action`) while tolerating slot reordering across indexes (e.g., `cs1/cs2.../csX`, `cs1Label/cs2Label.../csXLabel`, `flexNumber1/flexNumber2.../flexNumberX`)
- Harden malware extraction filters to target `DeviceProduct=New Anti Virus` and avoid false positives on other events

## [1.0.0] - 2024-02-21

### Changed

- Code migration:

| Before update | After update |
|---|---|
| source.port is a float | source.port is an int |
| source.nat.port is a float | source.nat.port is an int |
| destination.port is a float | destination.port is an int |
| destination.nat.port is a float | destination.nat.port is an int |
| action.properties.originsicname contains escaped separators (ex: CN\\=ertfw01,O=foomgmt.foobar.local.zazgch) | action.properties.originsicname is normalized (ex: CN=ertfw01,O=foomgmt.foobar.local.zazgch) |
| action.properties is a list of objects | action.properties is a dictionary (no impact expected) |
| network.transport may remain a numeric protocol value (ex: 1 => icmp) | network.transport is always translated to protocol string |
| action.properties.encryption_methods, action.properties.ike_ids and action.properties.ike_mode can be truncated | these field values are parsed in full (ex: ESP becomes ESP: AES-256 + SHA1 + PFS (group 5)) |
| user_agent parsing for geo_protection logs is partial | user_agent fields are fully parsed (device/name/original/os/version) |
