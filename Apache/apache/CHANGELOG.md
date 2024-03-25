# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [Unreleased]

## 2024-02.22 - 1.0.0

### Added

- Migrate format to Ingest

| Before the update                                                            | After the update                                                  |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| (no impact expected) at the parser level `action.properties` is of type list | `action.properties` is of type dict                               |
| `url.path=/path/plugin-min.js?v=1.12.1`                                      | `url.path=url.path=/path/plugin-min.js` and `url.query=v=1.12.1 ` |
