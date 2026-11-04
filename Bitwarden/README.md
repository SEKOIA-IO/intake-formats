# Bitwarden

## Description

Bitwarden provides open-source, zero-knowledge password and secrets management solutions for individuals, teams, and enterprise organizations.

## Intakes

- [Bitwarden Event Logs](./bitwarden_event_logs/CHANGELOG.md)

The Event Logs parser only supports events pushed by the Bitwarden HEC event
integrations (Generic HEC, Splunk, Huntress...): one JSON object per event,
rendered from the HEC template stored with the integration configuration.
Stored templates are not migrated, so all the template versions are supported:

- 2026-07-28 and later (current): `event` object with the `type` id,
  `typeName`, `deviceName`, `device` id, `systemUser`, `providerId` and
  `enrichment_details` (acting user, member, group and organization)
- 2026-02-23 to 2026-07-28: same fields, with `deviceType` instead of
  `deviceName`, and without `enrichment_details` before 2026-05-12
- 2026-01-23: `type` as the EventType name, `device` as the device name, flat
  `actingUserName`, `actingUserEmail`, `actingUserType`, `userName`,
  `userEmail`, `userType` and `groupName`
- before 2026-01-23: serialized event message in a string `Event` (or `event`)
  field, with PascalCase keys and numeric enums

Empty template values are ignored and device enum names are normalized to
their display names. The target user is taken from `memberId`, except for
self actions (such as logins) where it equals `actingUserId`, and for service
account member events (2300/2301) where it is a membership id.
