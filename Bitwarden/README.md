# Bitwarden

## Description

Bitwarden provides open-source, zero-knowledge password and secrets management solutions for individuals, teams, and enterprise organizations.

## Intakes

- [Bitwarden Event Logs](./bitwarden_event_logs/CHANGELOG.md)

The Event Logs parser only supports events pushed by the Bitwarden HEC event
integrations (Generic HEC, Splunk, Huntress...): one JSON object per event,
whose `event` object is rendered from the HEC template stored with the
integration configuration. Stored templates are not migrated, so all the
template versions are supported:

- 2026-07-28 and later (current): `type` id, `typeName`, `deviceName`, `device`
  id, `systemUser`, provider identifiers and `enrichment_details` (acting user,
  member, group and organization)
- 2026-02-23 to 2026-07-28: same fields, with `deviceType` instead of
  `deviceName` and without `enrichment_details` before 2026-05-12
- 2026-01-23: `type` and `device` as enum names, flat `actingUserName`,
  `actingUserEmail`, `actingUserType`, `userName`, `userEmail`, `userType` and
  `groupName`

Empty template values are ignored. When `memberId` equals `actingUserId`
(self actions such as logins), no target user is set.
