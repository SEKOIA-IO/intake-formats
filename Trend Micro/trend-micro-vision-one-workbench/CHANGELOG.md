# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-12

### Added

- Parse new custom fields:
  - `action.properties.ScriptBlockSize`: compute the UTF-8 byte size of `action.properties.ScriptBlockText` from the first `objectRawDataStr` indicator value and skip empty values

### Fixed

- Fix parsing of existing ECS fields:
  - `user.domain`: set only when `user.id` contains a domain prefix
