# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-25

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

## 2026-09-30

### Fixed

- Fix spamming smart descriptions:
  - remove raw-log content to prevent spammy full-log rendering and keep concise field-based summaries
  - require `cloudflare.ActorType` in conditions for templates that render it to avoid incomplete descriptions
