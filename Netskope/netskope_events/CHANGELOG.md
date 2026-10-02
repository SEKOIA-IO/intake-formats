# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-25

### Added

- Parse new ECS fields:
  - `url.domain` from `details.diff.added` raw field key `exception/Domain` to normalize exception domain values into a standard ECS field for cross-source search and correlation
- Parse new custom fields:
  - `netskope.events.domain_notes` from `details.diff.added` raw field key `exception/Domain/Notes` to preserve exception-specific note context that has no direct ECS equivalent

## 2026-08-14

### Added

- Parse new custom fields:
  - `netskope.events.record_type`
