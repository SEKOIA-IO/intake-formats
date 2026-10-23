# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-23

### Added

- Parse new ECS fields:
  - `host.domain`: derive domain when host name is FQDN-like
  - `host.name`: map explicit host name from device display name
  - `network.type`: infer IPv4 or IPv6 from parsed source IP candidates
  - `related.user`: populate user identifiers from normalized user identity context
  - `source.address`: set explicit source address alongside source IP
  - `source.geo.country_iso_code`: map country code from location country
- Parse new custom fields:
  - `azuread.properties.ipAddress`: preserve raw IP address from Microsoft Entra ID event properties

### Changed

- Extend parsing of existing ECS fields:
  - `related.ip`: aggregate and deduplicate all valid source IP values seen in the event
  - `source.ip`: add a fallback to map `properties.ipAddress` when `callerIpAddress` is missing or invalid
- Split ECS mappings into dedicated parser stages sorted by ECS category:
  - `set_ecs_host_fields`
  - `set_ecs_network_fields`
  - `set_ecs_related_fields`
  - `set_ecs_source_fields`

### Fixed

- Fix parsing of existing ECS fields:
  - `event.reason`: set an explicit metric summary to prevent smart-description fallback to raw message payload
  - `host.os.name`: preserve top-level operating system mapping when display name is absent
  - `source.geo.location`: guard mapping when `location` and `geoCoordinates` are not structured objects
  - `source.ip`: prevent missing source IP on risk events that could cause incorrect cross-tenant alert grouping
