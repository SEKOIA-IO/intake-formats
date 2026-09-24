# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [Unreleased] - 2026-05-27

### Added

- Parse PowerShell event hashes from `hashes.*` into ECS `file.hash.*` fields (`md5`, `sha1`, `sha256`) for Winlogbeat events
- Add dedicated `file.name` extraction (basename) from script/file paths (`Path`, `script_path`, `ScriptName`) to improve analysis when full paths are randomized
- Add a dedicated test case for this behavior in `Beats/winlogbeat/tests/powershell_path_and_hashes.json`

## [Unreleased] - 2026-05-26
### Added

- Parse scheduled task XML `TaskContent` and expose command and arguments from its `Exec` block
- Map `dll.name` and `dll.path` for image-load (Sysmon event code 7) events
- Map `destination.ip` and `destination.port` for network-related Sysmon and Security events
- Map Defender threat name to `action.properties.ThreatName` and `threat.software.name`

### Fixed

- Emit `registry.data.strings` as an array
- Improve `action.name` fallback for event code 8 with defensive access and type-safe comparison
- Normalize command-line tokenization handling by removing redundant duplicate blocks

## [Unreleased] - 2025-05-26

### Removed

- Remove unused field `event.origin`
