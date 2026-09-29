# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-29

### Added

- Parse new ECS fields:
  - `event.code` from Entra sign-in status error code
  - `user_agent.original` from `additionalDetails[].key == "User-Agent"` for audit events without `deviceDetail.browser`
- Add field descriptions in fields metadata:
  - `action.properties`
  - `azure.entraid.properties.*`
  - `azuread.properties.*`

### Changed

- Extend parsing of existing ECS fields:
  - generalize `targetResources` matching (position-independent, supports both `type` and `Type`) across event families:
    - `host.id`
    - `host.name`
    - `host.os.name`
    - `service.id`
    - `service.name`
  - extend fallback mapping with `initiatedBy.app.ipAddress` when present:
    - `source.ip`
  - extend actor fallback mapping for app-initiated events when user actor fields are absent:
    - `user.id` from `initiatedBy.app.servicePrincipalId`
    - `user.name` from `initiatedBy.app.displayName`
- Extend parsing of existing custom fields:
  - extend fallback mapping with `message.appId` when `additionalDetails[].key == "AppId"` is absent:
    - `azure.entraid.properties.appId`
    - `azuread.properties.appId`
  - extend backward-compatibility aliases for existing Entra ID custom fields:
    - `azuread.properties.appliedConditionalAccessPolicies`
    - `azuread.properties.clientAppUsed`
    - `azuread.properties.conditionalAccessPolicy.displayName`
    - `azuread.properties.conditionalAccessPolicy.newState`
    - `azuread.properties.conditionalAccessPolicy.oldState`
    - `azuread.properties.isInteractive`
    - `azuread.properties.operationType`
  - generalize `targetResources` matching (position-independent):
    - `azure.entraid.properties.modifiedProperties`
    - `azure.entraid.properties.targetServicePrincipalDisplayName`
    - `azuread.properties.modifiedProperties`
    - `azuread.properties.targetServicePrincipalDisplayName`
  - add forward-compatibility alias for existing Azure AD custom field:
    - `azure.entraid.properties.status.errorCode`
- Reorganize parser stages for readability while preserving field population chronology and outputs:
  - rename `set_common_fields` to `set_ecs_fields`
  - split custom mappings into dedicated stages:
    - `set_custom_fields_action`
    - `set_custom_fields_azure`
    - `set_custom_fields_azuread`
  - rename `set_target_user_fields_from_action_properties` to `set_ecs_user_target_fields`
  - rename `set_ecs_category` to `normalize_ecs_event_classification`

## 2026-07-29

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
