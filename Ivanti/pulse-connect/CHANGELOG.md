# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-10-20

### Added

- Parse `agent` into `user_agent.original`
- Parse `sessionID` and `ivs` into `ivanti.connect_secure.session.id` and `ivanti.connect_secure.instant_virtual_system`
- Parse `FBR32068` (bookmark access) and `WEB20174` (web request) events
- Set `event.outcome` for Host Checker events (`AUT24803`, `AUT24804`)

### Fixed

- Remove the trailing escaped carriage return (`#015`) added by rsyslog, which corrupted `event.code` and the parsing of `msg`
- Support Host Checker messages with multiple spaces, email usernames and a trailing session
- Trim leading spaces from `user.roles`

## [1.0.3] - 2026-10-16

### Fixed

- Fix parsing of existing ECS fields:
  - `client.ip`: map from raw field `msg` (NWC23464 `with IPv4 address ...` and NWC23508 `with NCIP ...`)
  - `source.ip`: map from raw field `src` (public source IP on NWC23464 session-start events)
  - `user.id`: map from raw field `msg` (session identifier from `session:...`) and trim when logs include `session: <id>` spacing

## [1.0.2] - 2026-09-28

### Fixed

- Fix NWC23464 grok capture by extracting assigned VPN IP into `ncip` instead of `src`

## [1.0.1] - 2023-10-18

### Changed

- Extract more information from messages
- Categorize the events
