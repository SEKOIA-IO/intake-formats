# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.2] - 2026-10-15

### Added

- Parse group management events (member added/removed, group created/changed/deleted, membership enumerated)
- Parse new ECS fields:
  - `event.category` (`iam`)
  - `event.type` (`group` with `creation`, `change`, `deletion` or `info` depending on the event ID)
  - `group.domain`
  - `group.id`
  - `group.name`
- Parse new custom fields:
  - `action.properties.member_name`
  - `action.properties.subject_logon_id`

### Changed

- Extend parsing of existing ECS fields to group membership events:
  - `user.target.domain` (built from the `DC=` components of the member distinguished name)
  - `user.target.id`
  - `user.target.name`
  - `user.target.sid`
- Classify group management events as `Security` in `action.type`

### Fixed

- Fix parsing of existing ECS fields:
  - `event.outcome` is now `failure` for failed logon and authentication events (4625, 4766, 4771, 4772, 4773, 4777, 4820 to 4824)
  - `process.name` is now parsed when the process information block ends the message
  - `user.domain` now holds the subject (actor) for non-logon events, which was previously mapped to `user.target.*`
  - `user.id` now holds the security identifier (SID) for non-logon events instead of the logon ID
  - `user.name` now holds the subject (actor) for non-logon events, which was previously mapped to `user.target.*`
  - `user.sid` now holds the subject (actor) SID for non-logon events, which was previously mapped to `user.target.*`
  - `user.target.id` now holds the security identifier (SID) instead of the logon ID
- Fix parsing of existing custom fields:
  - `action.properties.domain` is no longer truncated at the first dot for target account events
  - `action.properties.subject_logon_id` now holds the moved subject logon ID

## [2.0.1] - 2026-10-07

### Fixed

- Accept CRLF, tab, and space as field separators, for forwarders that flatten line breaks
- Accept `Subject :` with a space before the colon
- Add a fallback pattern for unsupported events to extract the action name from the first line instead of raising a parsing warning

## [2.0.0] - 2024-03-14

### Added

- Migrate format to Ingest

| Before the update                                                            | After the update                                                                                  |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| (no impact expected) at the parser level `action.properties` is of type list | `action.properties` is of type dict                                                               |
| `action.name: Démarrage`                                                     | is no more truncated for `Self-Service Plug-in` startup logs                                      |
| `user.name: domain\user`                                                     | `user.name: user` is now split between username and domain for events type `Self-Service Plug-in` |
| targeted user in `user`                                                      | targeted user in `user.target`                                                                    |
