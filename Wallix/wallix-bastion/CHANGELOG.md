# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-06-15

### Added

- Parse additional ECS fields from `sessionintegrity` logs:
    - event.end
    - event.start
    - file.extension
    - file.path
- Extract session recording metadata from unquoted `file` and `files` values in `sessionintegrity` logs

## [1.0.2] - 2023-11-02

### Added

- Extract more data from `cron` and `sudo` events

## [1.0.1] - 2023-10-23

### Added

- Extract the data from the keyboard input
