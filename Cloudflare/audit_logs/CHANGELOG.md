# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-11-25

### Fixed

- Fix existing ECS fields:
  - `source.ip` no longer keeps the `::ffff:` IPv4-mapped prefix when both `ActorIP` and `ActorIPAddress` are present (the two IP normalization stages shared the same name, so one overwrote the other)

## [1.0.1] - 2026-11-25

### Added

- Parse new custom fields:
  - `cloudflare.ActionDescription`
  - `cloudflare.ActorContext`

### Changed

- Extend parsing of existing ECS fields:
  - `source.ip` from `ActorIPAddress`

### Fixed

- Fix existing custom fields:
  - `cloudflare.ActionResult` set to `true` when the action result is `success`

## [1.0.0] - 2026-09-30

### Fixed

- Fix spamming smart descriptions:
  - remove raw-log content to prevent spammy full-log rendering and keep concise field-based summaries
  - require `cloudflare.ActorType` in conditions for templates that render it to avoid incomplete descriptions
