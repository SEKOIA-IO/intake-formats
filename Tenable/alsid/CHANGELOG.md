# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-01-15 - 2.0.0

### Added

- Migrate format to Ingest

| Before the update                                                                  | After the update                                                                 |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| (no impact expected) at the parser level `action.properties` is of type list       | `action.properties` is of type dict                                              |
| `action.properties.OperatingSystem: 'Windows'`                                     | `action.properties.OperatingSystem: 'Windows Server 2012 R2 Standard'`           |
| `action.properties.OperatingSystemVersion`: '6.3'                                  | `action.properties.OperatingSystemVersion: '6.3 (9600)'`                         |
| `action.properties.DisplayName`: DSC                                               | `action.properties.DisplayName: TESTnameCNdisplayname`                                  |
| broken value in `action.properties.DangerousAceList`                               | fixed, the field now contains the complete value                                 |
| broken value in `action.properties.DistinguishedName`                              | fixed, the field now contains the complete value                                 |
| `action.properties.ADdevianceID` type float                                        | `action.properties.ADdevianceID` type int                                        |
| `action.id` type float                                                             | `action.id` type int                                                             |
| `action.properties.alsidAttributeValue: ["Microsoft.MicrosoftEdge_8wekyb3d8bbwe"]` | `action.properties.alsidAttributeValue.0: Microsoft.MicrosoftEdge_8wekyb3d8bbwe` |
| Event starting by 2 not parsed                                                     | Event starting by 2 parsed                                                       |
