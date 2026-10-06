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
    - `cloud.account.id`
    - `cloud.provider`
    - `cloud.instance.id`
    - `cloud.instance.name`
    - `cloud.service.name`
  - Event related fields from incident and alert metadata:
    - `event.action`
    - `event.provider`
    - `event.start`
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
  - Observer related fields from workspace metadata:
    - `observer.name`
  - Process related fields from Process entities:
    - `process.command_line`
    - `process.pid`
    - `process.start`
  - Rule related fields from incident metadata:
    - `rule.id`
  - Related fields:
    - `related.hash`
    - `related.ip`
  - Source related fields from Ip entities:
    - `source.address`
    - `source.as.number`
    - `source.as.organization.name`
    - `source.geo.city_name`
    - `source.geo.country_iso_code`
    - `source.geo.country_name`
    - `source.geo.region_name`
    - `source.ip`
  - Threat related fields from Malware entities:
    - `threat.software.name`
    - `threat.software.type`
    - `threat.tactic.name`
    - `threat.technique.id`
  - URL related fields from Url entities:
    - `url.original`
- Parse new custom fields:
  - Cloud application related fields from CloudApplication entities:
    - `microsoft.sentinel.cloud_application.instance.name`
  - Azure resource related fields from AzureResource entities:
    - `microsoft.sentinel.resource.id`
    - `microsoft.sentinel.resource.subscription_id`
  - Incident metadata fields:
    - `microsoft.sentinel.provider_incident_id`
    - `microsoft.sentinel.workspace.id`
    - `microsoft.sentinel.workspace.resource_group`
- Add smart descriptions for incidents with related entities

### Changed

- Extend parsing of existing ECS fields to incidents in the `object.properties` format:
  - `@timestamp`
  - `event.end`
  - `event.reason`
  - `event.url`
  - `log.level`
  - `user.email`
- Extend parsing of existing custom fields to incidents in the `object.properties` format:
  - `microsoft.sentinel.classification.comment`
  - `microsoft.sentinel.classification.reason`
  - `microsoft.sentinel.classification.type`
  - `microsoft.sentinel.incident.number`
  - `microsoft.sentinel.status`
  - `microsoft.sentinel.title`
- Derive `cloud.instance.name` from Host entities so it matches the source of `cloud.instance.id`
- Populate `host.ip` only from Host entity address fields
- Map incident Ip entity address and geolocation fields to `source.*` instead of attributing them to `host.*`
- Use `related.ip` in smart descriptions that mention incident IP addresses
- Preserve multiple Process and Url entities by mapping their ECS fields as multi-value when incidents contain more than one related entity
- Enrich smart descriptions with higher-signal summaries for tactic/technique, source context, and workspace context

### Fixed

- Fix the owner email variable in smart descriptions to use `user.email`
