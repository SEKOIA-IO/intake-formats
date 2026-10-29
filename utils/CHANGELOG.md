# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-29

### Added

- Allow overriding the format validation endpoint with the `SEKOIA_VALIDATION_URL` environment variable

### Changed

- Compute the files checked by `mise run fix` and `mise run validate` against `origin/develop`, as the CI does
- Run the compliance checks of `mise run validate` with the same options as the CI

### Fixed

- Stop `mise run fix` and `mise run validate` when `origin/develop` is missing or when format files are untracked
- Prevent the linter and `mise run validate` from checking every format when no format changed
- Fail the linter with `--changes` when the diff against `origin/develop` fails, instead of reporting no changes

## 2026-10-13

### Fixed

- Accept domain-like anonymized values used in fixtures, including `example.*` subdomains and IP values in domain fields
- Accept additional anonymized username patterns used in fixtures, including user and the Microsoft service principal `Administrator` (`Microsoft.Office.Datacenter.Torus.PowerShellWorker`)
- Prevent pytest from collecting the single smart description CLI utility as a test module
- Prevent pytest from collecting validator utility classes named `Test*` as tests

## 2026-08-10

### Fixed

- Fix smart description rendering to handle nested and non-string list values without crashing

## 2026-05-21

### Fixed

- Update taxonomy tests to correctly handle module-level and format-level field scopes when checking missing and unused fields, to prevent false failures caused by module-level entries being asserted against format-level files
