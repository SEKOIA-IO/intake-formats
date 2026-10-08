# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.10] - 2026-10-08

### Added

- Parse new ECS fields by cross-checking [Microsoft Defender XDR official documentation](https://learn.microsoft.com/en-us/defender-xdr/) with [ECS official documentation](https://www.elastic.co/docs/reference/ecs)
  - `event.action`: map from raw field `ActionType` in `DeviceLogonEvents` events
  - `event.sequence`: map from raw field `ReportId` in `Device tables` events
  - `file.code_signature.exists`: map from raw field `IsSigned`
  - `file.code_signature.subject_name`: map from raw field `Signer`
  - `file.code_signature.trusted`: map from raw field `IsTrusted`
  - `process.entity_id`: map from raw fields `InitiatingProcessUniqueId` and `ProcessUniqueId` when available
  - `source.domain`: map from raw field `RemoteDeviceName` in device event/logon contexts
  - `source.port`: map from raw field `RemotePort` in `DeviceLogonEvents` events
  - `user.id`: map from raw fields `AccountSid` or `RequestAccountSid` when available
  - `user.target.id`: map from raw field `AccountSid` in `DeviceLogonEvents` events when available

### Changed

- Extend existing ECS fields by cross-checking [Microsoft Defender XDR official documentation](https://learn.microsoft.com/en-us/defender-xdr/) with [ECS official documentation](https://www.elastic.co/docs/reference/ecs)
  - `event.category`: map from raw field `category` to include `library` for `DeviceImageLoadEvents` events and `registry` for `DeviceRegistryEvents` events

### Fixed

- Normalize existing ECS fields by cross-checking [Microsoft Defender XDR official documentation](https://learn.microsoft.com/en-us/defender-xdr/) with [ECS official documentation](https://www.elastic.co/docs/reference/ecs)
  - `destination.ip`: skip generic mapping from raw field `RemoteIP` for `DeviceLogonEvents` events
  - `source.address`: map from raw fields `RemoteAddress` or `RemoteIP` as source endpoint in `DeviceLogonEvents` events
  - `source.ip`: map from raw field `RemoteIP` as source endpoint in `DeviceLogonEvents` events

## [1.0.9] - 2026-10-01

### Fixed

- Normalize existing ECS fields:
  - `email.message_id`: remove surrounding angle brackets from Microsoft Defender XDR `InternetMessageId` values when present

## [1.0.8] - 2026-08-12

### Added

- Parse new custom fields:
  - `microsoft.defender.url_chain`

## [1.0.7] - 2026-08-12

### Fixed

- Fix `TypeError` on `email.from.address` ECS field parsing, caused by attempting to read sender values from `Entities` when `Entities` is absent/empty
- Harden `Entities`-based field extraction with null/empty checks

## [1.0.6] - 2026-07-20

### Added

- Parse new custom fields:
  - `microsoft.defender.threat.last_verdict`
  - `microsoft.defender.threat.verdict`

## [1.0.5] - 2025-09-01

### Fixed

- Add remote device name in `DeviceLogonEvents`

## [1.0.4] - 2025-08-06

### Fixed

- Fix url domain when uri is present

## [1.0.3] - 2025-07-18

### Fixed

- Fix process fields in some categories

### Changed

- Add more fields and tests

## [1.0.2] - 2023-12-07

### Fixed

- Fix process fields in some categories

## [1.0.1] - 2023-12-07

### Changed

- Extract more data
