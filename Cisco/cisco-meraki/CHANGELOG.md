# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-10-28

### Added

- Parse `security_event` logs for the `ids_alerted` and `security_filtering_file_scanned` subtypes:
  - `cisco_meraki.event_subtype`: the security event subtype
  - `source.ip` / `source.port` and `destination.ip` / `destination.port`: split from `src` / `dst` (`IP:port`)
  - IDS/IPS: `rule.id` (`signature`), `rule.name` (trailing `message:`), `event.severity` (`priority`), `source.mac` (`shost`), `destination.mac` (`dhost`), `network.direction` (`direction`), `action.outcome` (`decision`), `cisco_meraki.ids.action` (`action`)
  - AMP file scanning: `url.original` (`url`), `source.mac` (`mac`), `file.hash.sha256` (`sha256`), `threat.software.name` (`name`), `cisco_meraki.file.disposition` (`disposition`), `action.outcome` (`action`)
- Categorize IDS alerts as `intrusion_detection` and malicious file scans as `malware`, with `event.type` derived from the decision/action

### Fixed

- Accept device hostnames containing non-word characters (e.g. hyphens) in the syslog header
