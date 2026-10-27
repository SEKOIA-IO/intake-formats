# Bitwarden

## Description

Bitwarden provides open-source, zero-knowledge password and secrets management solutions for individuals, teams, and enterprise organizations.

## Intakes

- [Bitwarden Event Logs](./bitwarden_event_logs/CHANGELOG.md)

The Event Logs parser accepts Generic HEC payloads with an `event` envelope and
`enrichment_details`, as well as public API events at the root. HEC `typeName`
is used as the event action when available. `observer.product` remains
`Password Manager`, including for Secrets Manager activity, in line with the
integration specification.

The HEC test fixtures are synthetic examples of the template payload, including
string values and empty strings for absent fields; they are not production captures.
