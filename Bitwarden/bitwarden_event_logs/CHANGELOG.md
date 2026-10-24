# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-21

### Added

- New Bitwarden Event Logs intake format with parsing for authentication, vault, organization, policy, domain, secrets manager, and send events.
- ECS mappings for event taxonomy, source IP, user identities, target user/group context, and organization metadata.
- Bitwarden custom fields for device, collection, item, policy, domain, secret, project, service account, and user role identifiers.
- Smart descriptions for authentication, vault, configuration, and administrative events.