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
  - `destination.port`: map from `winlog.event_data.DestPort` for Security event 5156
  - `file.directory`: derive from `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName`
  - `file.drive_letter`: derive from `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName`
  - `file.extension`: derive from `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName`
  - `file.name`: derive basename from `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName`
  - `file.path`: apply the same path decomposition for `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName` when present
  - `network.direction`: derive from `winlog.event_data.Direction` (`%%14592`/`%%14593`) for Security event 5156
  - `network.transport`: map from `winlog.event_data.Protocol` to known transport names for Security event 5156
  - `process.name`: map from `winlog.event_data.Application` for Security event 5156
  - `source.ip`: duplicate `winlog.event_data.SourceAddress` when it is a valid IP for Security event 5156
  - `source.port`: map from `winlog.event_data.SourcePort` for Security event 5156

### Fixed

- Fix parsing of existing ECS fields:
  - `file.name`:
    - make basename extraction robust for PowerShell events by handling `winlog.event_data.Path`, top-level `script_path`, and `winlog.event_data.ScriptName` with safe conditions
    - correct `ScriptName` mapping typo in PowerShell-specific stage (`json.event..winlog` -> `json.event.winlog`)
  - `file.directory`: keep backslash separators when deriving directory from `winlog.event_data.ScriptName` in the PowerShell 4103 stage

## [1.0.1] - 2026-05-27

### Fixed

- Fix parsing of existing ECS fields:
  - `file.hash.*`: parse PowerShell event hashes from `hashes.*` into ECS fields (`md5`, `sha1`, `sha256`)

## [1.0.0] - 2026-05-26

### Removed

- Remove unused ECS fields:
  - `event.origin`
