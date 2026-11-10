# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.7] - 2026-11-06

### Added

- Parse new custom fields:
  - `action.properties.SessionKeyEncryptionType`: expose the native Kerberos session key encryption code as a keyword, independently of `TicketEncryptionType`

## [1.0.6] - 2026-11-06

### Added

- Parse new ECS fields:
  - `source.user.domain`: map from raw field `DomainName`
  - `source.user.name`: map from raw field `Username`
- Parse new custom fields:
  - `action.properties.NtlmVersion`: map from raw field `NtlmVersion`
  - `action.properties.StatusMsg`: map from raw field `StatusMsg`

### Changed

- Extend parsing of existing ECS fields for NTLM Operational events:
  - `source.domain`: identify the remote client machine using raw field `RemoteClientMachine`
  - `source.ip`: populate the remote client address from raw field `ClientIP` when it is a valid IPv4 or IPv6 address
- Extend parsing of existing custom fields:
  - `action.properties.Status`: explicitly preserve the NTLM status code from raw field `Status`, including success values such as `0x0`, without deriving an authentication outcome

### Fixed

- Fix parsing of existing ECS fields for NTLM Operational events:
  - `user.domain`: use raw field `DomainName` when raw field `Username` is present, clearing the inherited system domain when no remote domain is provided
  - `user.name`: use raw field `Username` instead of the logging system account, clearing the inherited system SID to keep the identity consistent

## [1.0.5] - 2026-11-06

### Added

- Parse new ECS fields:
  - `error.code`: map from certificate request denial dispositions (4888) and translated SMB authentication errors (551)
- Parse new custom fields:
  - `action.properties.AccountExpires`
  - `action.properties.AuthenticationLevel`
  - `action.properties.AuthenticationService`
  - `action.properties.CertificateTemplate`
  - `action.properties.ConnectionGUID`
  - `action.properties.DCOMorRPC`
  - `action.properties.LogonHours`
  - `action.properties.RequestClientInfo`
  - `action.properties.RequestId`
  - `action.properties.SPN`
  - `action.properties.SPNValidationPolicy`
  - `action.properties.SessionGUID`
  - `action.properties.SessionId`
  - `action.properties.SubjectAlternativeName`
  - `action.properties.SubjectKeyIdentifier`

### Changed

- Prioritize usable dedicated JSON fields over extraction from `Message`, retaining `Message` as a fallback for historical formats when the corresponding JSON data is unavailable or unusable
- Extend parsing of existing ECS fields:
  - `event.reason`: map from dedicated failure reasons, prioritizing populated `FailureReasonResolved` over `Description` for Security-Auditing event 4625 and retaining historical message fallbacks
  - `process.name`: map from dedicated `RequestClientInfo` before extraction from `Message`
  - `process.pid`: map from decimal or hexadecimal `ProcessId` for Security-Auditing events 4625 and 4663 when `ProcessID` is absent
  - `source.domain`: map from SMB event 551 client names
  - `source.ip`: map from SMB event 551 client data, preferring valid `ClientAddress`, `EventData.ClientAddress`, `ClientName` and `EventData.ClientName` in that order before historical message extraction
  - `source.port`: map from validated IPv4 socket addresses in SMB event 551
  - `user.target.id`: map from `TargetSid` for events 4720 and 4738 when `TargetUserSid` is absent
- Extend parsing of existing custom fields:
  - `action.properties.Accesses`: map from dedicated resolved or readable access lists, retaining historical message fallbacks before unresolved resource codes
  - `action.properties.PasswordLastSet`: map from resolved JSON values when available
  - `action.properties.UserAccountControl`: map from resolved or readable JSON values, retaining the normalized list type and historical message fallbacks, and ignoring empty entries and `"-"` placeholders

### Fixed

- Fix existing ECS fields by no longer populating them with the Windows `"-"` placeholder (raw values in `action.properties` are kept as-is):
  - `dll.name`
  - `event.reason`
  - `process.executable`
  - `process.name`
  - `process.working_directory`
  - `related.user`
  - `rule.name`
  - `user.domain`
  - `user.name`
  - `user.target.domain`
  - `user.target.name`
- Fix existing custom fields:
  - `action.properties.Task`: prefer numeric `TaskValue` over textual `Task`, preventing conversion errors from discarding other event properties

## [1.0.4] - 2026-10-20

### Changed

- Extend parsing of existing custom fields:
  - `action.properties.Path`: map from PowerShell event message payloads when top-level `Path` is absent or empty

## [1.0.3] - 2026-09-30

### Added

- Parse new custom fields:
  - `action.properties.DnsHostName`: map for computer account change events
  - `action.properties.PasswordLastSet`: map for account-management events

## [1.0.2] - 2026-09-10

### Added

- Parse new custom fields:
  - `action.properties.ImpersonationLevel`: map for Windows 4624 events (`An account was successfully logged on`)

## [1.0.1] - 2024-02-29

### Add

- Parse new ECS fields:
  - `registry.path`
