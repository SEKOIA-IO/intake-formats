# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-11-04

### Added

- Parse new ECS fields:
  - `destination.domain`: extract the destination hostname from raw field `deliveredTo`
  - `destination.ip`: extract and validate the destination IP from raw field `deliveredTo`
  - `destination.port`: extract the destination port from raw field `deliveredTo` as an integer
  - `email.attachments.file.extension`: derive the extension without the leading dot from raw field `attachments[].fileName`
  - `event.reason`: map the non-empty raw field `details` for `Bounced` events only
- Parse new custom fields:
  - `trendmicro.email.recipient`: map raw field `recipient` to preserve the envelope recipient independently of `headerTo`

## [1.0.2] - 2026-09-29

### Added

- Parse new ECS fields:
  - `destination.address`
  - `email.delivery_timestamp`
  - `email.direction`
  - `source.ip`

## [1.0.1] - 2023-10-27

### Changed

- Change data source description

## [1.0.0] - 2023-10-17

### Added

- Initial version of the format
