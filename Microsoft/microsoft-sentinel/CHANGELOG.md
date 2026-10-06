# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-06

### Added

- Add a dedicated stage to parse incidents in the `object.properties` format with their related entities
- Parse new ECS fields:
  - Cloud related fields from CloudApplication and Host entities:
    - `cloud.instance.id`
    - `cloud.instance.name`
    - `cloud.service.name`
  - File related fields from File and FileHash entities:
    - `file.directory`
    - `file.hash.md5`
    - `file.hash.sha1`
    - `file.hash.sha256`
    - `file.name`
  - Host related fields from Host and Ip entities:
    - `host.domain`
    - `host.geo.city_name`
    - `host.geo.country_iso_code`
    - `host.geo.country_name`
    - `host.geo.region_name`
    - `host.ip`
    - `host.name`
    - `host.os.type`
    - `host.os.version`
  - Process related fields from Process entities:
    - `process.command_line`
    - `process.pid`
    - `process.start`
  - Related fields:
    - `related.hash`
    - `related.ip`
  - Threat related fields from Malware entities:
    - `threat.software.name`
    - `threat.software.type`
  - URL related fields from Url entities:
    - `url.original`
- Parse new custom fields:
  - Azure resource related fields from AzureResource entities:
    - `microsoft.sentinel.resource.id`
    - `microsoft.sentinel.resource.subscription_id`
- Add smart descriptions for incidents with related entities

### Changed

- Extend parsing of existing ECS/custom fields to incidents in the `object.properties` format:
  - `@timestamp`
  - `event.end`
  - `event.reason`
  - `event.url`
  - `log.level`
  - `microsoft.sentinel.classification.comment`
  - `microsoft.sentinel.classification.reason`
  - `microsoft.sentinel.classification.type`
  - `microsoft.sentinel.incident.number`
  - `microsoft.sentinel.status`
  - `microsoft.sentinel.title`
  - `user.email`

### Fixed

- Fix the owner email variable in smart descriptions to use `user.email`

