# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.2] - 2026-10-16

### Added

- Parse group management events (member added/removed, group created/changed/deleted, membership enumerated)
- Parse new ECS fields:
  - `event.category` (`iam`)
  - `event.type` (`group` with `creation`, `change`, `deletion` or `info` depending on the event ID) for group management raw events (`member added/removed`, `group created/changed/deleted`, `membership enumerated`)
  - `group.domain` for group creation/deletion and membership raw events
  - `group.id` for group creation/deletion and membership raw events
  - `group.name` for group creation/deletion and membership raw events
- Parse new custom fields:
  - `action.properties.member_name` for group membership raw events (`member added/removed`)
  - `action.properties.subject_logon_id`

### Changed

- Extend parsing of existing ECS fields:
  - `event.code`: parse localized French group-event titles
  - `event.type`: extend lifecycle typing on additional group-event families (`creation` for 4744, 4749, 4759 and `deletion` for 4748, 4753, 4763), and extend group-change typing when groups are identified through `Target Account` / `Compte cible` (4745, 4750, 4760)
  - `group.domain`: extend parsing to group-change events identified through `Target Account` / `Compte cible` (4735, 4737, 4745, 4750, 4755, 4760)
  - `group.id`: extend parsing to group-change events identified through `Target Account` / `Compte cible` (4735, 4737, 4745, 4750, 4755, 4760)
  - `group.name`: extend parsing to group-change events identified through `Target Account` / `Compte cible` (4735, 4737, 4745, 4750, 4755, 4760)
  - `user.target.domain`: extend parsing on group membership events
  - `user.target.id`: extend parsing on group membership events
  - `user.target.name`: extend parsing on group membership events
  - `user.target.sid`: extend parsing on group membership events
- Extend parsing of existing custom fields:
  - `action.id`: parse localized French group-event titles
  - `action.type`: classify group management events as `Security`, including security-disabled group-management IDs (4744 to 4753 and 4759 to 4763)

### Fixed

- Fix parsing of existing ECS fields:
  - `event.outcome`: set to `failure` for failed logon and authentication events (4625, 4766, 4771, 4772, 4773, 4777, 4820 to 4824)
  - `process.name`: parse when the process information block ends the message
    - preserve full process paths containing spaces for group-membership enumeration events, both at end of message and before a following section header
  - `user.domain`: map to the subject (actor) for non-logon events instead of `user.target.*`
  - `user.id`: map to the security identifier (SID) for non-logon events instead of the logon ID
  - `user.name`: map to the subject (actor) for non-logon events instead of `user.target.*`
  - `user.sid`: map to the subject (actor) SID for non-logon events instead of `user.target.*`
  - `user.target.domain`:
    - extract `DC` components case-insensitively without transformed-string offsets, including mixed-case `Dc=` and Unicode distinguished names
    - ignore escaped commas inside distinguished-name values (for example `CN=User\,DC=Test,...`) and keep only real `DC=` components
    - map logon events to New Logon / Account For Which Logon Failed domain values, and fallback to Subject domain for subject-only logoff events
  - `user.target.id`:
    - map to the security identifier (SID) instead of the logon ID
    - map logon events to New Logon / Account For Which Logon Failed SID values, and fallback to Subject SID for subject-only logoff events
  - `user.target.name`:
    - keep full distinguished-name CN values when member names contain spaces or escaped commas (for example `CN=User\,One,...`)
    - handle escaped backslashes correctly (for example `CN=User\\,OU=...` resolves to `User\`)
    - decode escaped RFC4514 special characters in CN values (for example `CN=Test\+User,...` resolves to `Test+User`)
    - decode hexadecimal RFC4514 escapes in CN values, including case-insensitive UTF-8 multibyte escapes (for example `CN=User\2COne,...` resolves to `User,One`, `CN=Us\C3\A9r,...` and `CN=Us\C3\a9r,...` resolve to `Usér`, `CN=Us\C3\B6r,...` resolves to `Usör`)
    - preserve escaped backslashes before hexadecimal text so `CN=User\\2COne,...` resolves to `User\2COne` and `CN=User\5C20,...` resolves to `User\20`
    - map logon events to New Logon / Account For Which Logon Failed account names, and fallback to Subject account name for subject-only logoff events
  - `user.target.sid`: map logon events to New Logon / Account For Which Logon Failed SID values, and fallback to Subject SID for subject-only logoff events
- Fix parsing of existing custom fields:
  - `action.properties.domain`: stop truncating at the first dot for target account events
  - `action.properties.id`: use a synthetic SID in account-modification fixture data instead of a production-looking domain SID
  - `action.properties.member_name`: exclude encoded CRLF separators when blank encoded lines appear before `Group:`

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
