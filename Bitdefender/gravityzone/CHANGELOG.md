# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2026-11-16

### Added

- Parse new fields `bitdefender.gravityzone.detection_technique` and `bitdefender.gravityzone.driver_path`
- Adding `event.category` for `antitampering` events

## [1.1.0]

### Added

- Map `agent.id` from `deviceExternalId`, the unique GravityZone computer identifier expected by EDR actions (e.g. isolation), so agent identifiers are attached to host assets

### Fixed

- `host.name` now holds the short hostname taken from `BitdefenderGZComputerFQDN`, and the remaining
  labels go to `host.domain`. The full FQDN in `host.name` was rejected by asset discovery, which
  expects a bare hostname, so no asset was created for those events.
