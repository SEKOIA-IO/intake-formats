# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-11-26

### Added

- Parse new custom fields:
  - `sekoiaio.activity.client.name`: extract the API key name and display it in the smart descriptions of actions performed with an API key

## [1.0.0] - 2026-06-05

### Changed

- Do not populate `user.full_name` for API key profiles, since the value is the internal API key label rather than a real user name
