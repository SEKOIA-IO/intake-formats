# Changelog

This update introduces the SonicWall SMA 1000 integration.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-09-03

### Added

- Support parsing of additional SonicWall SMA 1000 raw log families observed in customer exports:
  - Management Message Log cron-command variant (`(user) CMD (...)`)
  - Network Tunnel Audit Log bracketed variant (`[...] ... Audit Src=... Command=... Dest=...`)
  - Resource Access Log (`EventMessage: Resource Access`)

### Changed

- Harmonize log-type naming across format assets:
  - Changelog entries now use canonical log type names
  - Parser stage names follow `parse_<log_type>` and `set_<log_type>` conventions for new variants
  - Manifest `data_sources` descriptions align with the same naming, without changing existing keys
- Extend ECS fields extraction for the new Resource Access Log and Network Tunnel Audit Log variants:
  - `destination.domain`
  - `process.command_line`
  - `source.user.domain`
  - `source.user.email`
  - `source.user.name`
  - `user.email`

## [1.0.0] - 2026-08-19

### Added

- Integrate SonicWall SMA 1000 Series logs:
  - Management Access Log
  - Management Audit Log
  - Management Message Log
  - Network Tunnel Audit Log
  - System Message Log
  - Unregistered Device Log Messages
  - Web Proxy Audit Log
  - WorkPlace Logs
- Parse new ECS fields:
  - `@timestamp`
  - `destination.address`
  - `destination.bytes`
  - `destination.ip`
  - `destination.port`
  - `event.action`
  - `event.category`
  - `event.dataset`
  - `event.duration`
  - `event.kind`
  - `event.outcome`
  - `event.provider`
  - `event.severity`
  - `event.start`
  - `event.timezone`
  - `event.type`
  - `group.name`
  - `host.os.type`
  - `http.request.method`
  - `http.response.bytes`
  - `http.response.status_code`
  - `http.version`
  - `log.level`
  - `message`
  - `network.protocol`
  - `observer.hostname`
  - `observer.product`
  - `observer.type`
  - `observer.vendor`
  - `process.name`
  - `process.pid`
  - `related.hosts`
  - `related.ip`
  - `related.user`
  - `rule.id`
  - `rule.name`
  - `service.name`
  - `source.address`
  - `source.bytes`
  - `source.ip`
  - `source.port`
  - `source.user.domain`
  - `source.user.name`
  - `url.domain`
  - `url.full`
  - `url.original`
  - `url.path`
  - `url.port`
  - `url.registered_domain`
  - `url.scheme`
  - `url.subdomain`
  - `url.top_level_domain`
  - `user.domain`
  - `user.name`
- Parse new custom fields:
  - `sonicwall.sma.1000.api_endpoint`
  - `sonicwall.sma.1000.app_id`
  - `sonicwall.sma.1000.certificate.error_code`
  - `sonicwall.sma.1000.certificate.error_reason`
  - `sonicwall.sma.1000.change_type`
  - `sonicwall.sma.1000.connection_type`
  - `sonicwall.sma.1000.console_action`
  - `sonicwall.sma.1000.epc.query_result`
  - `sonicwall.sma.1000.equipment_id`
  - `sonicwall.sma.1000.export_state`
  - `sonicwall.sma.1000.http_status_class`
  - `sonicwall.sma.1000.management.class_name`
  - `sonicwall.sma.1000.management.address_pool.id`
  - `sonicwall.sma.1000.management.address_pool.name`
  - `sonicwall.sma.1000.policy.log_type`
  - `sonicwall.sma.1000.registered_device_count`
  - `sonicwall.sma.1000.source_id`
  - `sonicwall.sma.1000.syslog_facility`
  - `sonicwall.sma.1000.tunnel_version`
  - `sonicwall.sma.1000.unix_auth.context_type`
  - `sonicwall.sma.1000.unregistered_device.limit`
  - `sonicwall.sma.1000.workplace.policy_status`
  - `sonicwall.sma.1000.workplace.shortcut_type`
  - `sonicwall.sma.1000.workplace.team_session_id`
