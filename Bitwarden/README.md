# Bitwarden

## Description

Bitwarden provides open-source, zero-knowledge password and secrets management solutions for individuals, teams, and enterprise organizations.

## Intakes

- [Bitwarden Event Logs](./bitwarden_event_logs/CHANGELOG.md)

The Event Logs parser only supports events pushed by the Bitwarden HEC event
integration (Generic HEC, Splunk...). Each event is an envelope whose `event`
object follows the official Bitwarden HEC template: numeric `type`, `typeName`,
identifiers, `date`, `device`/`deviceName`, `ipAddress`, `systemUser` and
`enrichment_details` (acting user, member, group and organization). Empty
template values are ignored. Events without `typeName` or enrichment (integer
`type`, `null` values, flat `actingUserEmail`) are also accepted.
