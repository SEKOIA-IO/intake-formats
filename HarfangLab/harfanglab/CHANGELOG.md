# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.7] - 2026-11-12

### Added

- Parse new custom fields:
  - `action.properties.ScriptBlockSize`: compute the UTF-8 byte size of `action.properties.ScriptBlockText` from raw fields `script_block`, `event_data.ScriptBlockText` or `eventlog.event_data.ScriptBlockText` and skip empty values

## [1.3.6] - 2026-11-04

### Added

- Parse new ECS fields:
  - `destination.domain`: map from raw field `outgoing_protocol.tls.client_hello_sni` (outbound connections only)
  - `tls.client.ja3`: map from raw field `outgoing_protocol.tls.ja3_fingerprint`
  - `tls.client.server_name`: map from raw field `outgoing_protocol.tls.client_hello_sni`
  - `tls.server.ja3s`: map from raw field `incoming_protocol.tls.ja3s_fingerprint` (outbound connections only)
  - `tls.version`: map from raw field `outgoing_protocol.tls.tls_version` (normalize recognized TLS versions)
  - `tls.version_protocol`: map from raw field `outgoing_protocol.tls.tls_version`
- Parse new custom fields:
  - `harfanglab.harfanglab.outgoing_protocol.tls.client_hello_alpn`: map from raw field `outgoing_protocol.tls.client_hello_alpn` (preserve the array of protocols offered by the client)

### Changed

- Extend parsing of existing ECS fields:
  - `network.protocol`: map from raw field `outgoing_protocol.name` (lowercase for network events)

## [1.3.5] - 2026-08-17

### Fixed

- Generalize `connection_successful` handling with a dedicated stage so it is parsed whenever present in raw logs, regardless of event dataset (`network`, `connectionlog`, etc.)
- Update `event.outcome` from `connection_successful` in the same dedicated stage for consistent behavior across datasets

## [1.3.4] - 2026-08-14

### Added

- Parse new custom fields:
  - `harfanglab.connection_successful`
  - `harfanglab.event_data.new_value`
  - `harfanglab.event_data.old_value`

### Changed

- Update ECS fields:
  - `event.outcome`:
    - update mapping from `connection_successful` in `connectionlog` events
    - harden mapping for event IDs `4624` and `4625` by supporting mixed raw value types
- Update custom fields:
  - `action.properties.SourceName`: populate from top-level `source_name` for Windows Defender event logs

## [1.3.3] - 2026-08-11

### Added

- Parse new ECS fields in the `network_info` stage:
  - `destination.bytes`
  - `source.bytes`
- Parse new custom fields in the `network_info` stage:
  - `harfanglab.network.kind`

### Changed

- Update DNS resolution parsing to support values under `details_dns_resolution`
- Improve parsing of ECS fields:
  - `dns.question.name`
  - `dns.question.name`
  - `dns.resolved_ip`
- Improve parsing of custom fields:
  - `harfanglab.dns.raw_windows_resolver_results`

## [1.3.2] - 2026-08-11

### Fixed

- Parse ECS fields from raw field `message.event_id` with fallback to `message.eventlog.event_id` for eventlog alerts:
  - `action.id`
  - `event.code`

## [1.3.1] - 2026-08-04

### Fixed

- Parse new ECS fields from `agents[0].agent_hostname` on threat events:
  - `host.hostname`
  - `host.name`

## [1.3.0] - 2024-12-11

### Changed

- Split username into `user.name` and `user.domain`

## [1.2.0] - 2024-10-01

### Added

- Add some extra fields

## [1.1.1] - 2024-01-18

### Fixed

- retrieve file name
- retrieve registry value

## [1.1.0] - 2023-12-04

### Changed

- parse more log types
