# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2024-02-26 - 1.0.0

### Added

- Migrate format to Ingest

| Before the update                                                            | After the update                    |
| ---------------------------------------------------------------------------- | ----------------------------------- |
| some empty fields can have the values `N/A` or `None`                        | these values are now ignored        |
| (no impact expected) at the parser level `action.properties` is of type list | `action.properties` is of type dict |
| `file.size` is a string                                                      | `file.size` is an int               |
| `http.request.bytes` is a float                                              | `http.request.bytes` is an int      |
