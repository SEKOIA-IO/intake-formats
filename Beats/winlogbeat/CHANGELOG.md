# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-26

### Fixed

- Fix a syntax error in the `file.name` template (`json.event..winlog`)
- Fix `winlog.event_data.Category` and `SubCategory`, which used the JavaScript `toUpperCase()` and printed a character of the GUID instead of the mapped name
- Parse `powershell.command.invocation_details` from `param3` / `Payload`: the templates relied on `re` and `len`, which are not available
- Split `process.args` from the command line, ignoring repeated spaces: the template relied on `range` and `len`, which are not available
- Decode `winlog.event_data.AccessMaskDescription`, `NewUACList` and `TicketOptionsDescription` from their bitmasks: the templates relied on `range`, which is not available, and missed the flags sharing a hex digit (e.g. `0x15`)
- Fix the mask of `STANDARD_RIGHTS_REQUIRED` (`0x000F0000`)
- Drop the empty arguments from the PowerShell `process.args` and `process.args_count`
- Build lists and dicts without mutating them in place (`.append`, `.update`, ...), which not every Jinja engine supports

## [1.0.2] - 2026-11-16

### Added

- Parse new custom fields:
  - `action.properties.ScriptBlockSize`: compute the UTF-8 byte size of `action.properties.ScriptBlockText` from raw field `winlog.event_data.ScriptBlockText` and skip empty values

### Fixed

- Fix smart descriptions:
  - PowerShell 4104 events: do not render `NULL` when `user.id` is missing
  - Windows PowerShell 400, 403, 600 and 800 events and Security 1102 events: use a dedicated description instead of the raw message

## [1.0.1] - 2026-05-27

### Added

- Parse PowerShell event hashes from `hashes.*` into ECS `file.hash.*` fields (`md5`, `sha1`, `sha256`) for Winlogbeat events
- Add dedicated `file.name` extraction (basename) from script/file paths (`Path`, `script_path`, `ScriptName`) to improve analysis when full paths are randomized
- Add a dedicated test case for this behavior in `Beats/winlogbeat/tests/powershell_path_and_hashes.json`

## [1.0.0] - 2026-05-26

### Removed

- Remove unused field `event.origin`
