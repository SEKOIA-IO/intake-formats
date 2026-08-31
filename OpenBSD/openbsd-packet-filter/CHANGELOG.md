# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-31 - 1.0.2

### Added

- Parse new ECS fields:
  - `network.transport` for IPv6 ICMP filterlog events
  - `network.type` for IPv4/IPv6 TCP, UDP, ICMP, CARP, and ICMP error-like events
- Parse new custom fields:
  - `openbsd.pf.icmp.datalength` for IPv6 ICMP filterlog events
- Add descriptions for all `openbsd.pf.*` custom fields in metadata
- Enrich smart-descriptions with specific ICMP request and ICMP unreachable templates

### Changed

- Parse existing custom fields more consistently:
  - `openbsd.pf.transport.options` for TCP events
- Change `openbsd.pf.carp.advbase` and `openbsd.pf.carp.advskew` field types from `keyword` to `integer` to match their numeric semantics

### Fixed

- Fix IPv6 ICMP parsing by accepting hyphenated IPv6 protocol tokens in PF IPv6 logs
- Anonymize test fixtures with RFC 5737 TEST-NET IPv4 ranges

## 2023-08-29 - 1.0.1

### Changed

- fix the format in order to apply smart-descriptions for the UDP events
