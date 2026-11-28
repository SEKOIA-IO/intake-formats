# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-10-14

### Removed

- Remove deprecated custom fields as an acceptable breaking change:
  - `seckiot.assets.entity`: replaced by ECS field `host.type`
  - `seckiot.assets.id`: replaced by ECS field `host.id`
  - `seckiot.assets.localisation`: replaced by ECS field `host.geo.name`
  - `seckiot.assets.name`: replaced by ECS field `host.name`
  - `seckiot.assets.perdue_level`: replaced by custom field `seckiot.assets.purdue_level`
  - `seckiot.assets.system`: replaced by ECS field `host.os.name`
  - `seckiot.assets.version`: replaced by ECS field `host.os.version`
  - `seckiot.catch_area.name`: replaced by custom field `seckiot.capture_zone.id` for UUIDs or ECS field `observer.ingress.zone` otherwise
  - `seckiot.module`: replaced by ECS field `event.provider`
  - `seckiot.sensor.name`: replaced by ECS field `observer.name`
  - `seckiot.sniffer.name`: replaced by ECS field `observer.ingress.interface.id` for UUIDs or `observer.ingress.interface.name` otherwise

## [1.0.0] - 2026-10-14

### Added

- Parse new ECS fields:
  - `device.manufacturer`: map raw field `skt.assets[].hardware_vendor`
  - `device.model.identifier`: map raw field `skt.assets[].modele`
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

- Migrate custom fields from `text` to `keyword` (breaking full-text queries in favor of exact-match behavior):
  - `seckiot.alert.id`
  - `seckiot.assets.category`
  - `seckiot.assets.description`
- Rework smart descriptions for detection, cartography, and vulnerability alerts with richer context and a deterministic priority, each specific variant having strictly more conditions than its fallback
- Stop padding asset lists with `unknown` values

### Deprecated

- Keep populating deprecated ECS fields for backward compatibility, to be removed after a customer announcement:
  - `rule.id`: use ECS field `rule.uuid`
- Keep populating deprecated custom fields for backward compatibility, to be removed after a customer announcement:
  - `seckiot.assets.entity`: use ECS field `host.type`
  - `seckiot.assets.id`: use ECS field `host.id`
  - `seckiot.assets.localisation`: use ECS field `host.geo.name`
  - `seckiot.assets.name`: use ECS field `host.name`
  - `seckiot.assets.perdue_level`: use custom field `seckiot.assets.purdue_level`
  - `seckiot.assets.system`: use ECS field `host.os.name`
  - `seckiot.assets.version`: use ECS field `host.os.version`
  - `seckiot.catch_area.name`: use custom field `seckiot.capture_zone.id` for UUIDs or ECS field `observer.ingress.zone` otherwise
  - `seckiot.module`: use ECS field `event.provider`
  - `seckiot.sensor.name`: use ECS field `observer.name`
  - `seckiot.sniffer.name`: use ECS field `observer.ingress.interface.id` for UUIDs or `observer.ingress.interface.name` otherwise

### Fixed

- Fix existing ECS fields:
  - `@timestamp`: parse raw field `@timestamp` in UTC with `date.parse` instead of using the ingestion time
  - `event.category`: derive valid ECS categories from raw field `skt.module` (`Detection Engine` to `intrusion_detection`, `Cartography` to `network`, `CVE` to `vulnerability`, and the unknown-device discovery rule to `host`) instead of copying the vendor value `["info"]`, which is not a valid ECS category
  - `network.protocol`: parse raw field `network.protocol` and lowercase it
  - `network.transport`: parse raw field `network.transport` and lowercase it
  - `observer.name`: use raw field `observer.name`, falling back to `skt.sensor`, instead of the incorrect `event.outcome` mapping
  - `rule.uuid`: map raw field `rule.uuid` to ECS field `rule.uuid` (`rule.id` is kept with the same value for backward compatibility)
- Fix existing custom fields:
  - `seckiot.assets.purdue_level`: correct the `perdue_level` typo, set the type to `long`, parse raw field `skt.assets[].level` when sent as a string, accept level zero, and keep only levels between 0 and 6
