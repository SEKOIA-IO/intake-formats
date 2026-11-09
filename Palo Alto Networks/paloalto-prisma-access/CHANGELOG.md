# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-03

### Fixed

- Fix GlobalProtect events in the JSON format:
  - `event.outcome` and `action.outcome`: parse `EventStatus`
  - `action.name`: parse `EventIDValue`
  - `event.reason`: parse `ConnectionError` before `Description`
- `url.original`: do not set `https://` when the URL, file name and URL file name are empty

## 2024-10-08

### Added

- Creation of the format
