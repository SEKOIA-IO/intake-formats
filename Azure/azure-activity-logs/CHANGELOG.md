# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Parse ECS fields `event.outcome` and `http.request.body.content` from the operation status and request body.
- Parse custom fields `azure.activity_logs.status`, `azure.activity_logs.role_assignment.principal_id`, `azure.activity_logs.role_assignment.principal_type` and `azure.activity_logs.role_assignment.role_definition_id`.
- Add anonymized regression tests for operation statuses, role assignments and missing or invalid request bodies.

### Changed

- Prioritize role assignment details over generic administrative descriptions when a source IP is present.
- Default `event.outcome` to `unknown` for unmapped, non-empty operation statuses.
- Include operation statuses and role assignment details in smart descriptions.
