# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-29

### Added

- New Bitwarden Event Logs intake format for events pushed by the Bitwarden HEC event integrations
- Support for the 2026-01-23, 2026-02-23 and current HEC templates
- Event action from the HEC `typeName`, with a fallback on the Bitwarden EventType enum names
- Event taxonomy and outcome for authentication, vault, collection, group, member, organization, policy, domain, Secrets Manager, Send and PAM events
- ECS mappings for the acting user, target member, organization, group and source IP
- Bitwarden custom fields for device, system actor, membership, item, collection, policy, installation, provider, domain, secret, project and service account identifiers
- Smart descriptions for authentication, vault, administration, configuration and Secrets Manager events
