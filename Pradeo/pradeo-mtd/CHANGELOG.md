# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-21

### Added

- Parse new ECS fields:
  - `device.id`:
    - mapped from raw field `device.id` for device synchronization events without explicit `type`
    - mapped from raw field `deviceApplicationCompliance.deviceApplication.device.id` for `DeviceApplicationComplianceUpdated` events
    - mapped from raw field `deviceCompliance.device.id` for `DeviceComplianceUpdated` events
    - mapped from raw field `deviceCorrelation.device.id` for `DeviceCorrelationUpdated` events
    - mapped from raw field `deviceSystemStatusRecord.device.id` for `DeviceSystemStatusRecordUpdated` events
  - `event.reason`: mapped from raw field `deviceSystemStatusRecord.deviceSystemStatus.name` for `DeviceSystemStatusRecordUpdated` events
  - `host.name`: mapped from raw field `deviceSystemStatusRecord.device.name` for `DeviceSystemStatusRecordUpdated` events

### Changed

- Extend parsing of existing ECS fields:
  - `@timestamp`: keep `creationDate` for wrapped events and map from raw field `deviceSystemStatusRecord.device.enrollmentStatus.lastConnection` only for root-level events
  - `event.category`: mapped from raw field `type` when value is `DeviceSystemStatusRecordUpdated` (`["host", "configuration"]`)
  - `host.os.type`:
    - mapped from raw field `deviceApplicationCompliance.deviceApplication.device.declaredOperatingSystem` for `DeviceApplicationComplianceUpdated` events
    - mapped from raw field `deviceCompliance.device.declaredOperatingSystem` for `DeviceComplianceUpdated` events
    - mapped from raw field `deviceCorrelation.device.declaredOperatingSystem` for `DeviceCorrelationUpdated` events
    - mapped from raw field `deviceNetworkStatusRecord.device.declaredOperatingSystem` for `DeviceNetworkStatusRecordUpdated` events
    - mapped from raw field `deviceSystemStatusRecord.device.declaredOperatingSystem` for `DeviceSystemStatusRecordUpdated` events
  - `host.os.version`:
    - mapped from raw field `deviceApplicationCompliance.deviceApplication.device.declaredOperatingSystemVersion` for `DeviceApplicationComplianceUpdated` events
    - mapped from raw field `deviceCompliance.device.declaredOperatingSystemVersion` for `DeviceComplianceUpdated` events
    - mapped from raw field `deviceCorrelation.device.declaredOperatingSystemVersion` for `DeviceCorrelationUpdated` events
    - mapped from raw field `deviceNetworkStatusRecord.device.declaredOperatingSystemVersion` for `DeviceNetworkStatusRecordUpdated` events
    - mapped from raw field `deviceSystemStatusRecord.device.declaredOperatingSystemVersion` for `DeviceSystemStatusRecordUpdated` events
  - `user.email`:
    - mapped from raw field `device.email` for `DeviceCorrelationUpdated` events
    - mapped from raw field `device.email` for `DeviceApplicationComplianceUpdated` events
    - mapped from raw field `device.email` for `DeviceComplianceUpdated` events
    - mapped from raw field `deviceSystemStatusRecord.device.email` for `DeviceSystemStatusRecordUpdated` events
- Extend parsing of existing custom fields:
  - `pradeo.device.serialNumber`: mapped from raw field `deviceSystemStatusRecord.device.serialNumber` for `DeviceSystemStatusRecordUpdated` events
  - `pradeo.device.imei`: mapped from raw field `deviceSystemStatusRecord.device.imei` for `DeviceSystemStatusRecordUpdated` events

## [1.0.0] - 2024-07-26

### Added

- Add `compliance` parsing stage to capture compliance decisions for a device or an application
- Add `correlation` parsing stage to capture threat level for a device configuration
- Add `detection` parsing stage to capture status changes in device configuration
- Add `initiator` parsing stage to capture information about the user or device that performs the action
- Add `metadata` parsing stage to capture event metadata
- Add `permission` parsing stage to capture acceptance or rejection of Pradeo agent permissions
