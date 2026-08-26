# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.4] - 2026-08-10

### Added

- Parse new ECS fields: 
    - `email.attachments`: parse attachment names and sizes from `Exchange Item` data, including entries without size metadata
    - `email.to.address`: parse `Exchange Item` recipients into the ECS email recipient address list

### Changed

- Update ECS fields:
    - `email.message_id`: normalize `InternetMessageId` values by removing surrounding angle brackets when present
    - `email.subject`: set the subject only when `Item.Subject` is present to avoid empty or invalid values

## [1.0.3] - 2026-07-03

### Changed

- Do not populate `user.target.name` when `TargetUserOrGroupType` is `SharePointGroup`, since the value is a SharePoint group name rather than a person
- Parse Microsoft 365 Copilot `CopilotInteraction` audit events (RecordType `261`) from the `Audit.General` feed

## [1.0.2] - 2023-12-08

### Added

- improve parsing of Automated Investigation and Response events

## [1.0.1] - 2023-09-28

### Added

- improve parsing

## [1.0.0] - 2022-06-09

### Added

- initial version of the format
