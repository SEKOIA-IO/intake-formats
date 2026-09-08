# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2026-08-11

### Added

- Harmonize parsing of related custom detection fields across event types
- Parse custom fields:
  - `crowdstrike.detect_description`:
    - from `DetectionSummaryEvent` events
    - from `EppDetectionSummaryEvent` events
  - `crowdstrike.detect_name`:
    - from `DetectionSummaryEvent` events
    - from `EppDetectionSummaryEvent` events
  - `crowdstrike.event_objective`:
    - from `DetectionSummaryEvent` events
    - from `EppDetectionSummaryEvent` events
    - from `IdpDetectionSummaryEvent` events

## [1.0.4] - 2024-06-10

### Added

- Support of EppDetectionSummaryEvent
- Extract AssociatedFile from DetectionSummaryEvent

### Fixed

- Convert host.ip and host.mac into array

## [1.0.3] - 2024-01-18

### Added

- Support of MobileDetectionSummaryEvent

## [1.0.2] - 2023-09-26

### Changed

- Fix the way to define timestamp for IDP events

## [1.0.1] - 2023-08-15

### Added

- Support of IDP events

## [1.0.0] - 2022-07-15

### Added

- New format for CrowdStrike Falcon events
