# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.1] - 2026-10-07

### Fixed

- Accept CRLF, tab, and space as field separators, for forwarders that flatten line breaks
- Accept `Subject :` with a space before the colon
- Add a fallback pattern for unsupported events to extract the action name from the first line instead of raising a parsing warning

## [2.0.0] - 2024-03-14

### Added

- Migrate format to Ingest

| Before the update                                                            | After the update                                                                                  |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| (no impact expected) at the parser level `action.properties` is of type list | `action.properties` is of type dict                                                               |
| `action.name: Démarrage`                                                     | is no more truncated for `Self-Service Plug-in` startup logs                                      |
| `user.name: domain\user`                                                     | `user.name: user` is now split between username and domain for events type `Self-Service Plug-in` |
| targeted user in `user`                                                      | targeted user in `user.target`                                                                    |
