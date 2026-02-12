# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-10

### Added
- Initial release of the Anozrway Balise Pipeline format.
- Parser for leak detection events from the POST /events endpoint.
- ECS mapping: event.kind=alert, event.category=threat, event.action=leak-detected.
- Custom fields under anozrway.balise.* namespace.
- event.outcome derived from status field (finished/failed/running).
- threat.indicator fields for events with uploaded files.
