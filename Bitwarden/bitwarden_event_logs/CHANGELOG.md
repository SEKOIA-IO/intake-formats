# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Parse HEC event envelopes and nested identity enrichment, including target member IDs and device names, while retaining root event support.
- Ignore empty template values and non-numeric event codes; prefer HEC typeName actions and correct fallback actions.
- Categorize vault and Send events as file activity and organization settings 1610–1628 as configuration changes.
- Improve authentication, vault, export, and Secrets Manager smart descriptions and remove the duplicate member custom field.
- Keep observer.product aligned with the integration specification and use application/authentication data source labels.
- Add synthetic HEC regression fixtures covering template string values and empty enrichment.

## [1.0.0] - 2026-10-21

### Added

- New Bitwarden Event Logs intake format with parsing for authentication, vault, organization, policy, domain, secrets manager, and send events.
- ECS mappings for event taxonomy, source IP, user identities, target user/group context, and organization metadata.
- Bitwarden custom fields for device, collection, item, policy, domain, secret, project, service account, and user role identifiers.
- Smart descriptions for authentication, vault, configuration, and administrative events.
