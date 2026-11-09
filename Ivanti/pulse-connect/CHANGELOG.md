# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.4] - 2026-11-09

### Fixed

- Fix parsing of existing ECS fields:
  - `action.name`: remove the leading quote left when rsyslog appends an escaped carriage return (`#015`) to the log (e.g. `"AUT30836` -> `AUT30836`)
  - `event.category`: no longer fall back to `network` when the log ends with `#015`
  - `event.code`: remove the leading quote left when the log ends with `#015` (e.g. `"AUT30836` -> `AUT30836`)
  - `event.dataset`: translate the event code prefix again when the log ends with `#015` (e.g. `"AU` -> `Authenticate`)
  - `event.outcome`: categorize failed logins `AUT24327`, `AUT30836` and `AUT31985` as `authentication` events with `event.outcome: failure`
  - `event.reason`: remove the trailing `"#015` and the escaped quotes when the log ends with `#015`

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
