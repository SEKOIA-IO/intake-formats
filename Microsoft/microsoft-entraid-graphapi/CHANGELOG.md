# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-07-29

### Fixed

- Create a dedicated parser stage `set_actor_target_user_fields` to separate actor identity (`user.*`) from impacted target user identity (`user.target.*`) in `UserManagement` events
- Fix target user extraction to populate `user.target.id`, `user.target.name`, and `user.target.email` only when the target user is different from the actor
- Fix `action.properties` enrichment so `targetedUser` entries are added only for impacted users and not duplicated for the actor
- Fix app-initiated scenarios by preserving impacted target user values when no actor user identity is available in top-level fields

## 2026-07-21

### Added

- Add ECS target user fields for `UserManagement` events when the impacted user differs from the actor:
    - `user.target.id`
    - `user.target.name`
    - `user.target.email`

### Changed

- Update `user.name` mapping to prioritize `userPrincipalName` (login identifier) over `displayName`
- Update PIM user override so `user.name` also prefers `targetResources[].userPrincipalName`
- Update `user.email` behavior to keep the actor identity and avoid replacing it with the target user email

## 2026-05-27

### Added

- Added `azuread.properties` aliases matching existing `azure.entraid.properties` mappings:
    - `azuread.properties.appId`
    - `azuread.properties.conditionalAccessStatus`
    - `azuread.properties.resourceId`
    - `azuread.properties.riskDetail`
    - `azuread.properties.riskEventTypes`
    - `azuread.properties.riskLevelAggregated`
    - `azuread.properties.riskLevelDuringSignIn`
    - `azuread.properties.riskState`
    - `azuread.properties.targetServicePrincipalDisplayName`
