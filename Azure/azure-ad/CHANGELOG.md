# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2026-11-24

### Added

- Parse new custom fields:
  - `azuread.properties.targetRoleDisplayName`: from raw field `properties.targetResources[].displayName` of the single `Role` target (e.g. the role requested in a PIM activation)

### Changed

- Extend parsing of existing ECS fields:
  - `event.type`: set `["change", "user"]` instead of `["info"]` for PIM role management audit logs (`loggedByService` = `PIM`, category `RoleManagement`, with a `Role` target)
  - `network.type`: derive `ipv4` or `ipv6` from the first valid `ipaddr` entry of `additionalDetails` in audit logs
  - `source.ip`: map the first valid `ipaddr` entry of `additionalDetails` in audit logs (e.g. PIM role activation requests where `initiatedBy.user.ipAddress` is null) when neither `callerIpAddress`, `ipAddress` nor `properties.ipAddress` is a valid IP, ignoring invalid values and duplicate entries

## [1.0.2] - 2026-11-12

### Fixed

- Fix existing ECS fields:
  - `user.email`: stop filling it with the initiating application in audit logs initiated by an application, the targeted user staying in `user.target.*`
  - `user.full_name`: stop filling it with the initiating application in audit logs initiated by an application, the targeted user staying in `user.target.*`
  - `user.id`: stop filling it with the initiating application in audit logs initiated by an application, the targeted user staying in `user.target.*`
  - `user.name`: stop filling it from raw field `identity` in audit logs, which could hold an application name such as "My Signins" next to the id of the user who acted through it, and with the initiating application in audit logs initiated by an application
- Fix existing custom fields:
  - `azuread.properties.appDisplayName`: map raw field `properties.initiatedBy.app.displayName` in audit logs initiated by an application instead of `user.*`
  - `azuread.properties.appId`: map raw field `properties.initiatedBy.app.appId` in audit logs initiated by an application instead of `user.*`
  - `azuread.properties.servicePrincipalId`: map raw field `properties.initiatedBy.app.servicePrincipalId` in audit logs initiated by an application instead of `user.*`
  - `azuread.properties.servicePrincipalName`: map raw field `properties.initiatedBy.app.servicePrincipalName` in audit logs initiated by an application instead of `user.*`

### [1.0.1] - 2026-11-02

### Added

- Parse new custom fields from raw events `targetResources.modifiedProperties` when target resource type is `ServicePrincipal`:
  - array:
    - `azuread.properties.targetServicePrincipals`: from raw field `targetResources` (ServicePrincipal target display names)
    - `azuread.properties.targetServicePrincipalDisplayNames`: from raw field `targetResources[].displayName`
    - `azuread.properties.targetServicePrincipalIds`: from raw field `targetResources[].id`
  - keyword:
    - `azuread.properties.targetServicePrincipalAppIdNewValue`: from raw field `ServicePrincipal.AppId`
    - `azuread.properties.targetServicePrincipalAppRoleAssignmentCreatedDateTimeNewValue`: from raw field `AppRoleAssignment.CreatedDateTime`
    - `azuread.properties.targetServicePrincipalAppRoleAssignmentLastModifiedDateTimeNewValue`: from raw field `AppRoleAssignment.LastModifiedDateTime`
    - `azuread.properties.targetServicePrincipalAppRoleNewDisplayValue`: from raw field `AppRole.DisplayName` (legacy compatibility)
    - `azuread.properties.targetServicePrincipalAppRoleDisplayNameNewValue`: from raw field `AppRole.DisplayName`
    - `azuread.properties.targetServicePrincipalAppRoleIdNewValue`: from raw field `AppRole.Id`
    - `azuread.properties.targetServicePrincipalAppRoleValueNewValue`: from raw field `AppRole.Value`
    - `azuread.properties.targetServicePrincipalDisplayNameNewValue`: from raw field `ServicePrincipal.DisplayName`
    - `azuread.properties.targetServicePrincipalNameNewValue`: from raw field `ServicePrincipal.Name`
    - `azuread.properties.targetServicePrincipalNamesNewValue`: from raw field `TargetId.ServicePrincipalNames`
    - `azuread.properties.targetServicePrincipalObjectIdNewValue`: from raw field `ServicePrincipal.ObjectID`
- Enrich smart descriptions using `azuread.properties.target*` custom fields

### Changed

- Extend parsing of existing ECS fields:
  - `event.category`: map `UserRiskEvents` to `["authentication"]`
  - `event.type`: keep `["info"]` for `UserRiskEvents`
- Extend parsing of existing custom fields:
  - `azuread.properties.targetServicePrincipalDisplayName`: populate even when multiple `ServicePrincipal` targets are present

## [1.0.0] - 2026-10-23

### Added

- Parse new ECS fields:
  - `host.domain`: derive domain when host name is FQDN-like
  - `host.name`: map explicit host name from device display name
  - `network.type`: infer IPv4 or IPv6 from parsed source IP candidates
  - `related.user`: populate user identifiers from normalized user identity context
  - `source.address`: set explicit source address alongside source IP
  - `source.geo.country_iso_code`: map country code from location country
- Parse new custom fields:
  - `azuread.properties.ipAddress`: preserve raw IP address from Microsoft Entra ID event properties

### Changed

- Extend parsing of existing ECS fields:
  - `related.ip`: aggregate and deduplicate all valid source IP values seen in the event
  - `source.ip`: add a fallback to map `properties.ipAddress` when `callerIpAddress` is missing or invalid
  - `user.name`: prioritize nested `properties.userPrincipalName` before display identity fallback
- Split ECS mappings into dedicated parser stages sorted by ECS category:
  - `set_ecs_host_fields`
  - `set_ecs_network_fields`
  - `set_ecs_related_fields`
  - `set_ecs_source_fields`

### Fixed

- Fix parsing of existing ECS fields:
  - `event.reason`: set an explicit metric summary to prevent smart-description fallback to raw message payload
  - `host.os.name`: preserve top-level operating system mapping when display name is absent
  - `source.geo.location`: guard mapping when `location` and `geoCoordinates` are not structured objects
  - `source.ip`: prevent missing source IP on risk events that could cause incorrect cross-tenant alert grouping
