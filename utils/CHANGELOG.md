# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [Unreleased] - 2026-05-29

### Fixed

- Fix smart description rendering to handle nested and non-string list values without crashing

## [Unreleased] - 2026-05-21

### Fixed

- Update taxonomy tests to correctly handle module-level and format-level field scopes when checking missing and unused fields, to prevent false failures caused by module-level entries being asserted against format-level files
