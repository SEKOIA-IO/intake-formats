# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `notice.log`: keep the raw event in the top-level `message` field; the notice text is now exposed as `corelight.notice.message`.
- `suricata_corelight`: also map `alert.action` to `event.action` (in addition to `action.name`).
- `conn.log`: `source.user.roles` is now emitted as an array; `event.duration` is now emitted as an integer (nanoseconds).
- Detection rules now reference the relevant Zeek/Suricata documentation instead of a generic integration link.

## 2026-06-17 - 1.0.0

### Added

- Initial Corelight Open NDR intake format.
- Parsing of Zeek/Corelight logs: `conn`, `dns`, `http`, `ssl`, `files`, `notice` and the Zeek Intelligence Framework (`intel`).
- Parsing of Suricata IDS alerts (`suricata_corelight`).
- Mapping of Corelight entity enrichment (`enrichment_orig.user`, `enrichment_orig.role`, `enrichment_orig.city_location`) to ECS.
