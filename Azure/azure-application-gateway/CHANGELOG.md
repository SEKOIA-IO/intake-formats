# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-22

### Added

- Parse new ECS fields:
  - `event.category`
  - `event.outcome`
  - `http.request.mime_type`
  - `http.version`
  - `network.protocol`
  - `observer.product`
  - `observer.vendor`
  - `rule.id`
  - `rule.ruleset`
  - `rule.version`
  - `tls.cipher`
  - `tls.version`
  - `tls.version_protocol`
  - `url.domain`
  - `url.port`
  - `url.path`
  - `url.query`
- Parse new custom fields:
  - `azure.application_gateway.listener`
  - `azure.application_gateway.metric.average`
  - `azure.application_gateway.metric.count`
  - `azure.application_gateway.metric.maximum`
  - `azure.application_gateway.metric.minimum`
  - `azure.application_gateway.metric.name`
  - `azure.application_gateway.metric.time_grain`
  - `azure.application_gateway.metric.total`
  - `azure.application_gateway.routing_rule`

### Changed

- Extend parsing of existing ECS fields:
  - `destination.*`: derive backend destination from `serverRouted` for access logs, and map firewall `hostname` to `destination.ip`/`destination.port` when `hostname` contains an IP target
  - `event.action`: extend handling across log types
    - performance: `event.action` is populated from `metricName`
  - `event.dataset`: extend handling across log types  
    - performance: `event.dataset="ApplicationGatewayPerformance"`
    - common mapping: use only provided `operationName` to avoid classifying incomplete non-metric events as performance
  - `event.outcome`: extend normalization to all log types
    - access: success/failure from `http.response.status_code`, fallback `unknown`
    - firewall: success/failure from Azure WAF `event.action` values (`Allowed`/`Blocked`), fallback `unknown` for other values (`Matched`/`Detected`/`Log`)
    - performance: `unknown` by design
  - `event.type`: extend handling across log types
    - access: `event.type=["access","connection"]`
    - firewall: base `event.type=["access","connection"]`, overridden by `event.type=["allowed"]` for `Allowed`, `event.type=["denied"]` for `Blocked`, and `event.type=["info"]` for `Matched`/`Detected`
    - performance: `event.type=["info"]`
  - `event.category`: keep `event.category=["network"]` for access/performance logs and classify firewall detections with `event.category=["network","intrusion_detection"]`
  - AGW routing identifiers: map `ruleName` and `listenerName` to custom fields (`azure.application_gateway.routing_rule`, `azure.application_gateway.listener`) to avoid mixing routing metadata with WAF/detection rule semantics in ECS `rule.*`
  - `url.domain`: map request host from `originalHost` when available, with fallback to `host` (port stripped when present), and map firewall `hostname` when the target is a domain name
- Cover access, firewall, and performance log types with dedicated ECS/custom stages
- Keep only high-signal Azure Application Gateway custom fields and metric fields

### Fixed

- Fix parsing of existing ECS fields:
  - `@timestamp`: when `timeStamp` is missing, parse `time` as fallback (including 7-digit fractional timestamps on performance events)
  - `network.bytes`: cast `receivedBytes`/`sentBytes` to integers before addition to avoid string concatenation on legacy payloads
- Fix fixture anonymization:
  - replace environment-specific API paths and identifiers in access/firewall test fixtures with generic values
