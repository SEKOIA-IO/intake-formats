# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-11-26

### Added

- Support Cloudflare Audit Logs v2 (`audit_logs_v2` dataset) alongside v1 (`audit_logs` dataset)
- Parse new ECS fields:
  - `cloud.account.name`: map from `AccountName`
  - `cloud.provider`: set to `cloudflare`
  - `event.kind`: set to `event`
  - `event.outcome`: map from `ActionResult` (`success` or `failure`)
  - `http.request.id`: map from `Raw.cf_ray_id`
  - `http.request.method`: map from `Raw.method`
  - `http.response.status_code`: map from `Raw.status_code`
  - `url.original`: map from `Raw.uri`
  - `user_agent.original`: map from `Raw.user_agent`
- Add a test from the Cloudflare documentation example of an Audit Logs v2 record

### Changed

- Split the pipeline into stages for fields common to v1 and v2, v1-only fields and v2-only fields (v2 values take precedence)
- Extend parsing of existing ECS fields:
  - `@timestamp`: map from `ActionTimestamp`
  - `cloud.account.id`: map from `AccountID`
- Extend parsing of existing custom fields:
  - `cloudflare.ID`: map from `AuditLogID`
  - `cloudflare.zone_name`: map from `ZoneName`
  - `cloudflare.zone_tag`: map from `ZoneID`
- Rework smart descriptions to use `event.outcome`, `user.email` and `cloudflare.ActionDescription`
- Rename test fixtures as `test_v1_<theme>_00X` and `test_v2_<theme>_00X` to clearly identify Audit Logs v1 and v2 records

### Fixed

- Fix existing ECS fields:
  - `event.category` set to `configuration` instead of `network`
  - `event.type` set from the action type (`creation`, `change`, `deletion`, `access`, fallback `info`) instead of always `access`
  - `source.ip`: rename the two IPv4-mapped normalization stages that shared the same name, so `ActorIPAddress` takes precedence over `ActorIP`
  - `user.email` and `user.id` are no longer set from empty values
- Fix existing custom fields:
  - `cloudflare.ActionDescription`: no longer set from empty values
  - `cloudflare.ActorContext`: no longer set from empty values

## [1.0.1] - 2026-11-25

### Added

- Parse new custom fields:
  - `cloudflare.ActionDescription`
  - `cloudflare.ActorContext`

### Changed

- Extend parsing of existing ECS fields:
  - `source.ip`: map from `ActorIPAddress`

### Fixed

- Fix existing custom fields:
  - `cloudflare.ActionResult` set to `true` when the action result is `success`

## [1.0.0] - 2026-09-30

### Fixed

- Fix spamming smart descriptions:
  - remove raw-log content to prevent spammy full-log rendering and keep concise field-based summaries
  - require `cloudflare.ActorType` in conditions for templates that render it to avoid incomplete descriptions
