# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-02 - 1.1.0

### Changed

- Map assets to ECS `host.*` (`id`, `name`, `type`, `os.name`, `os.version`, `geo.name`) and `device.*` (`manufacturer`, `model.identifier`) fields instead of `seckiot.assets.*`
- Map the module to `event.provider`, the sensor to `observer.name`, the capture zone to `observer.ingress.zone` and the sniffer to `observer.ingress.interface.name`
- Set `event.category` to a valid ECS category according to the module
- Rename `seckiot.assets.perdue_level` to `seckiot.assets.purdue_level` (type `long`)
- No longer pad asset lists with `unknown` values

### Added

- Add `seckiot.session.id`

### Fixed

- Fix `@timestamp`, which was never extracted from the event
- Fix `network.protocol` and `network.transport`, which were never extracted
- Fix `observer.name`, which was mapped from `event.outcome`
