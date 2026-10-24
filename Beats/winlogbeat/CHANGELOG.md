# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2026-10-22

### Added

- Parse new ECS fields:
  - `destination.address`: map from `winlog.event_data.DestAddress` for Security event 5156
  - `network.iana_number`: map from `winlog.event_data.Protocol` for Security event 5156
  - `source.address`: map from `winlog.event_data.SourceAddress` for Security event 5156

### Changed

- Extend parsing of existing ECS fields:
  - `destination.ip`: duplicate `winlog.event_data.DestAddress` when it is a valid IP for Security event 5156
  - `destination.port`: map numeric `winlog.event_data.DestPort` for Security event 5156
  - `network.direction`: map `winlog.event_data.Direction` (`%%14592`/`%%14593`) to `ingress` and `egress` for Security event 5156
  - `network.transport`: map from `winlog.event_data.Protocol` to known transport names for Security event 5156
  - `process.name`: map basename from `winlog.event_data.Application` for Security event 5156
  - `process.pid`: map numeric `winlog.event_data.ProcessID` for Security event 5156
  - `source.ip`: duplicate `winlog.event_data.SourceAddress` when it is a valid IP for Security event 5156
  - `source.port`: map numeric `winlog.event_data.SourcePort` for Security event 5156

### Fixed

- Fix existing ECS fields:
  - `file.directory`:
    - keep backslash separators when deriving directory from `winlog.event_data.ScriptName` in the PowerShell 4103 stage
    - clear carried values when `Path`, `script_path`, or `ScriptName` is selected as the replacement source
  - `file.drive_letter`: preserve incoming values when no replacement source path is selected, and clear carried values before deriving from the selected path source
  - `file.extension`: preserve incoming values when no replacement source path is selected, and clear carried values before deriving from the selected path source
  - `file.hash.*`: preserve derived hash precedence by applying incoming `file` passthrough before hash extraction from `winlog.event_data.Hashes` and `hashes.*`
  - `file.name`: map basename from the selected source and fix the `json.event..winlog` typo in the PowerShell 4103 stage
  - `file.path`: keep one non-empty source with `Path` > `script_path` > `ScriptName` precedence as the authoritative source for PowerShell events
- Ignore empty-string and `-` placeholder values globally (`ignored_values`) to reduce placeholder-driven mapping artifacts
- Reduce verbose fallback outputs in smart descriptions to prevent noise

## [1.0.1] - 2026-05-27

### Fixed

- Fix parsing of existing ECS fields:
  - `file.hash.*`: parse PowerShell event hashes from `hashes.*` into ECS fields (`md5`, `sha1`, `sha256`)

## [1.0.0] - 2026-05-26

### Removed

- Remove unused ECS fields:
  - `event.origin`
