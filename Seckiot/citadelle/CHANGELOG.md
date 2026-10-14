# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-14

### Added

- Parse new ECS fields:
  - `device.manufacturer`: map raw field `skt.assets[].hardware_vendor`
  - `device.model.identifier`: map raw field `skt.assets[].modele`
  - `event.category`: derive valid ECS categories from raw field `skt.module` (`Detection Engine` to `intrusion_detection`, `Cartography` to `network`, and `CVE` to `vulnerability`), with unknown-device discovery classified as `host`
  - `event.ingested`: map raw field `event.ingested`
  - `event.provider`: map raw field `skt.module`
  - `host.geo.name`: map raw field `skt.assets[].localisation`
  - `host.id`: map raw field `skt.assets[].id`
  - `host.name`: map raw field `skt.assets[].name`
  - `host.os.name`: map raw field `skt.assets[].system`
  - `host.os.version`: map raw field `skt.assets[].version`
  - `host.type`: map raw field `skt.assets[].entity`
  - `observer.ingress.interface.id`: map raw field `skt.sniffer` when it contains a UUID
  - `observer.ingress.interface.name`: map raw field `skt.sniffer` when it is not a UUID
  - `observer.ingress.zone`: map raw field `skt.capture_zone` when it is not a UUID
- Parse new custom fields:
  - `seckiot.capture_zone.id`: map raw field `skt.capture_zone` when it contains a UUID
  - `seckiot.session.id`: map raw field `skt.session`

### Changed

- Stop padding asset lists with `unknown` values
- Rework smart descriptions for detection, cartography, and vulnerability alerts with richer ECS/custom-field context, stronger fallbacks, and deterministic priority from category-specific variants to generic fallbacks

### Fixed

- Fix existing ECS fields:
  - `@timestamp`: parse raw field `@timestamp` in UTC with `date.parse` instead of using the ingestion time
  - `network.protocol`: parse raw field `network.protocol` and lowercase it
  - `network.transport`: parse raw field `network.transport` and lowercase it
  - `observer.name`: use raw field `observer.name`, falling back to `skt.sensor`, instead of the incorrect `event.outcome` mapping
  - `event.action`: stop duplicating the detection signature from `rule.name`; keep it in `rule.name`
  - `event.category`: classify the unknown-device discovery rule as `host` rather than generic `network`
  - `rule.uuid`: map raw field `rule.uuid` to ECS `rule.uuid` instead of `rule.id`
- Fix existing custom fields:
  - `seckiot.assets.purdue_level`: correct the `perdue_level` typo, set the type to `long`, parse raw field `skt.assets[].level` when sent as a string, and accept level zero

### Removed

- Remove legacy custom fields as a breaking change:
  - `seckiot.assets.entity`: replaced by ECS field `host.type`
  - `seckiot.assets.id`: replaced by ECS field `host.id`
  - `seckiot.assets.localisation`: replaced by ECS field `host.geo.name`
  - `seckiot.assets.name`: replaced by ECS field `host.name`
  - `seckiot.assets.system`: replaced by ECS field `host.os.name`
  - `seckiot.assets.version`: replaced by ECS field `host.os.version`
  - `seckiot.catch_area.name`: replaced by custom field `seckiot.capture_zone.id` for UUIDs or ECS field `observer.ingress.zone` otherwise
  - `seckiot.module`: replaced by ECS field `event.provider`
  - `seckiot.sensor.name`: replaced by ECS field `observer.name`
  - `seckiot.sniffer.name`: replaced by ECS field `observer.ingress.interface.id` for UUIDs or `observer.ingress.interface.name` otherwise
