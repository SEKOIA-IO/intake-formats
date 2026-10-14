# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-14 - 1.1.0

### Changed

- Map assets to ECS `host.*` (`id`, `name`, `type`, `os.name`, `os.version`, `geo.name`) fields instead of `seckiot.assets.*`
- Map the module to `event.provider` and the sensor to `observer.name`
- Map the sniffer to `observer.ingress.interface.id` when it is a UUID, `observer.ingress.interface.name` otherwise
- Map the capture zone to `seckiot.capture_zone.id` when it is a UUID, `observer.ingress.zone` otherwise
- Accept Purdue levels sent as strings
- Rework smart descriptions and add one for vulnerabilities
- Set `event.category` to a valid ECS category according to the module
- Rename `seckiot.assets.perdue_level` to `seckiot.assets.purdue_level` (type `long`)
- No longer pad asset lists with `unknown` values

### Added

- Add `seckiot.session.id`
- Map asset hardware vendor and model to `device.manufacturer` and `device.model.identifier`
- Set `event.action` from the rule name

### Removed

- Remove custom fields `seckiot.module`, `seckiot.sensor.name`, `seckiot.sniffer.name`, `seckiot.catch_area.name`, `seckiot.assets.id`, `seckiot.assets.name`, `seckiot.assets.entity`, `seckiot.assets.system`, `seckiot.assets.version` and `seckiot.assets.localisation`, replaced by the ECS fields above

### Fixed

- Fix `@timestamp`, which was never extracted from the event (now parsed with `date.parse` in UTC)
- Fix `network.protocol` and `network.transport`, which were never extracted
- Fix `observer.name`, which was mapped from `event.outcome`
