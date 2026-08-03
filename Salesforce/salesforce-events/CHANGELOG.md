# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 1.0.3 - 2026-08-03

### Added

- Parse new custom fields:
	- `salesforce.dml.type`
	- `salesforce.document.id`
	- `salesforce.entity.id`
	- `salesforce.transaction.type`

### Changed

- Update ECS field `event.action`:
    - use `DML_TYPE` as fallback source when `UI_EVENT_TYPE` and `ACTION` are not present
    - use `TRANSACTION_TYPE` as fallback source when `UI_EVENT_TYPE`, `ACTION` and `DML_TYPE` are not present

## 1.0.2 - 2023-07-20

### Changed

- Extract more fields
- Improve smart-descriptions

## 1.0.1 - 2023-07-11

### Changed

- Fix the UUID of the format

## 1.0.0 - 2023-07-05

### Added

- Initial version of the Salesforce Event format
