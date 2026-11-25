# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support Prisma Access Browser, Browser Extension and Mobile Browser events.
- Parse ECS fields for Browser events:
  - `event.action`, `event.category`, `event.type`, `event.outcome`
  - `host.name`, `network.application`, `observer.product`, `observer.vendor`
  - `rule.category`, `rule.description`, `url.original`, `user.email`, `user.name`, `user.domain`
  - `threat.framework`, `threat.technique.id`
- Parse custom fields for Browser events:
  - `action.name`: policy action, including protected access and blocking
  - `paloalto.endpoint.serial_number`: browser device serial number
- Add Browser smart descriptions and anonymized tests for the event types and policy actions in the supplied sample.
- Handle null or missing `ClassificationMITRE` and default `observer.product` to `Prisma Access Browser` when `LogSource` is null or missing.
- Classify completed Browser authentication (`loginSuccess`, `loginFail`) with `event.type: end`.

## [1.0.1] - 2026-11-12

### Changed

- Extend parsing of existing ECS fields:
  - `event.outcome`: parse `EventStatus` (`success` or `failure`) for GlobalProtect events in JSON format
- Extend parsing of existing custom fields:
  - `action.name`: parse `EventIDValue` for GlobalProtect events in JSON format
  - `action.outcome`: parse `EventStatus` for GlobalProtect events in JSON format

### Fixed

- Fix parsing of existing ECS fields:
  - `event.reason`: parse `ConnectionError` before `Description` for GlobalProtect events in JSON format
  - `url.original`: no longer set to `https://` when `URL`, `FileName` and `URLFilename` are empty

## [1.0.0] - 2024-10-08

### Added

- Creation of the format
