# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.4] - 2026-11-09

### Fixed

- Set `event.outcome: failure` and `event.category: authentication` on failed logins `AUT24327`, `AUT30836` and `AUT31985`
- Remove the trailing escaped carriage return (`#015`) added by rsyslog, which corrupted `event.code` and the parsing of `msg`

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
