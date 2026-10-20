# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-30

### Added

- Parse new custom fields from raw events `targetResources.modifiedProperties` when target resource type is `ServicePrincipal`:
  - array:
    - `azuread.properties.targetServicePrincipals` from raw field `targetResources` (ServicePrincipal target display names)
    - `azuread.properties.targetServicePrincipalDisplayNames` from raw field `targetResources[].displayName`
    - `azuread.properties.targetServicePrincipalIds` from raw field `targetResources[].id`
  - keyword:
    - `azuread.properties.targetServicePrincipalAppIdNewValue` from raw field `ServicePrincipal.AppId`
    - `azuread.properties.targetServicePrincipalAppRoleAssignmentCreatedDateTimeNewValue` from raw field `AppRoleAssignment.CreatedDateTime`
    - `azuread.properties.targetServicePrincipalAppRoleAssignmentLastModifiedDateTimeNewValue` from raw field `AppRoleAssignment.LastModifiedDateTime`
    - `azuread.properties.targetServicePrincipalAppRoleNewDisplayValue` from raw field `AppRole.DisplayName` (legacy compatibility)
    - `azuread.properties.targetServicePrincipalAppRoleDisplayNameNewValue` from raw field `AppRole.DisplayName`
    - `azuread.properties.targetServicePrincipalAppRoleIdNewValue` from raw field `AppRole.Id`
    - `azuread.properties.targetServicePrincipalAppRoleValueNewValue` from raw field `AppRole.Value`
    - `azuread.properties.targetServicePrincipalDisplayNameNewValue` from raw field `ServicePrincipal.DisplayName`
    - `azuread.properties.targetServicePrincipalNameNewValue` from raw field `ServicePrincipal.Name`
    - `azuread.properties.targetServicePrincipalNamesNewValue` from raw field `TargetId.ServicePrincipalNames`
    - `azuread.properties.targetServicePrincipalObjectIdNewValue` from raw field `ServicePrincipal.ObjectID`
- Enrich smart descriptions using `azuread.properties.target*` custom fields
### Changed

- Populate `azuread.properties.targetServicePrincipal*` keyword fields for both single and multiple `ServicePrincipal` targets using the first `ServicePrincipal` containing `modifiedProperties`.
- Keep `azuread.properties.targetServicePrincipalDisplayName` populated for multiple `ServicePrincipal` targets (no loss of searchable field in multi-target events).
- Make `azuread.properties.targetServicePrincipals` query-friendly by storing a flat array of display names instead of serialized JSON blobs.
