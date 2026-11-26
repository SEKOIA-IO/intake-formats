# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-25

### Added

- Initial version of the Aruba ClearPass parser (Session Logs, Insight Logs, Audit Records, ClearPass System Events)
- Parse new ECS fields:
  - `error.code`
  - `error.message`
  - `host.hostname`
  - `host.ip`
  - `host.mac`
  - `network.vlan.id`
  - `observer.hostname`
  - `service.name`
- Parse new custom fields:
  - `aruba.clearpass.authentication.protocol`
  - `aruba.clearpass.authentication.source`
  - `aruba.clearpass.login_status`
  - `aruba.clearpass.nad.name`
  - `aruba.clearpass.nad.network_device`
  - `aruba.clearpass.privilege_level`
  - `aruba.clearpass.radius.calling_station_id`
  - `aruba.clearpass.radius.framed_ip_address`
  - `aruba.clearpass.radius.nas_ip_address`
  - `aruba.clearpass.radius.termination_cause`
  - `aruba.clearpass.radius.user_name`
  - `aruba.clearpass.tacacs.authentication.action`
  - `aruba.clearpass.tacacs.command`
  - `aruba.clearpass.tacacs.service`
  - `aruba.clearpass.user.authentication.source`

### Changed

- Extend parsing of existing ECS fields to TACACS and RADIUS authentication events:
  - `destination.ip`
  - `event.action`
  - `event.outcome`
  - `event.type`
  - `user.name`
- Extend parsing of existing custom fields to TACACS and RADIUS authentication events:
  - `aruba.clearpass.enforcement_profile`
