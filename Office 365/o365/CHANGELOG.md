# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Do not populate `user.target.name` when `TargetUserOrGroupType` is `SharePointGroup`, since the value is a SharePoint group name rather than a person

## 2026-05-29 - 1.0.3

### Added

- Parse Exchange `RecordType: 2` `Item.Recipients` into `email.to.address`
- Parse Exchange `RecordType: 2` `Item.Attachments` into `email.attachments` (including degraded attachment format without size)
- Parse Exchange `RecordType: 2` `Item.Subject` and robust `Item.InternetMessageId` normalization
- Add Exchange email smart descriptions using subject, recipients, message id, and attachments
- Add anonymized Exchange test fixtures for recipient and attachment parsing, including an edge case with attachments without size

## 2023-12-08 - 1.0.2

### Added

- improve parsing of Automated Investigation and Response events

## 2023-09-28 - 1.0.1

### Added

- improve parsing

## 2022-06-09 - 1.0.0

### Added

- initial version of the format
