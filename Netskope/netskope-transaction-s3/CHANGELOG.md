# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-05

### Changed

- Ignore CSV header rows in parser-specific routing to avoid mapping them as transaction events

### Fixed

- Prevent parsing warnings on CSV header rows by handling them as ignored header-only records

## [1.0.0] - 2025-10-15

#### Added

- initial version of the format
