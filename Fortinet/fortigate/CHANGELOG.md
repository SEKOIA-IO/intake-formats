# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-10

### Added

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
    - `threat.technique.id`
- Parse new custom fields:
    - `fortinet.fortigate.decoy.group`
    - `fortinet.fortigate.decoy.type`
    - `fortinet.fortigate.incident.event_id`
    - `fortinet.fortigate.incident.id`
    - `fortinet.fortigate.loghost`
    - `fortinet.fortigate.operation`
    - `fortinet.fortigate.password`
    - `fortinet.fortigate.tag.id`
    - `fortinet.fortigate.tag.key`
    - `fortinet.fortigate.tzone`
    - `fortinet.fortigate.ui`
    - `fortinet.fortigate.username`

### Changed

- Update ECS fields:
    - `@timestamp`

## [1.0.1] - 2023-10-23

### Added

- Extract the name of the attack from events
