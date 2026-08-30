# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-19

### Added
- Initial release of the unified Anozrway intake format.
- Parser for Balise Pipeline leak detection events (POST /events endpoint).
- Parser for Domain Search intelligence records (LEAK and RANSOMWARE types).
- ECS mapping: event.category=threat, event.type=indicator for all event types.
- Balise Pipeline: event.kind=alert, event.action=leak-detected, event.outcome from status field.
- Domain Search LEAK: event.kind=enrichment, event.action=leak-detected.
- Domain Search RANSOMWARE: event.kind=alert, event.action=ransomware-detected.
- threat.indicator.url.domain mapped from source domain for Domain Search events.
- threat.indicator file fields for Balise Pipeline events with uploaded files.
- Custom fields under anozrway.balise.* (Balise Pipeline) and anozrway.record.*/anozrway.source.* (Domain Search).
