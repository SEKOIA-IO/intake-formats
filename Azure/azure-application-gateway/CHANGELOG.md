# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-21

### Added

- Parse new ECS fields:
  - `event.outcome`
  - `http.response.mime_type`
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
  - `@timestamp`: normalize performance timestamp from `time` (including fractional-second values) so metric events consistently emit `@timestamp`
  - `destination.*`: derive backend destination from `serverRouted` only, to keep `destination.ip`/`destination.port` aligned with the routed backend endpoint
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
    - firewall: `event.type=["allowed"]` for `Allowed`, `event.type=["denied"]` for `Blocked`, fallback `event.type=["access","connection"]`
    - performance: `event.type=["info"]`
  - `network.bytes`: set only when `receivedBytes` or `sentBytes` exists, and cast both to integers before addition to preserve correct totals on legacy string payloads
  - `rule.name`: remove AGW routing identifiers from ECS rule naming to avoid mixing routing and WAF detection semantics
  - `url.domain`: map request host from `originalHost` when available, with fallback to `host` (port stripped when present)
- Extend parsing of existing custom fields:
  - `azure.application_gateway.details.message`: extend extraction for firewall events when nested WAF details are present (`properties.details.message`)
  - `azure.application_gateway.error_info`: extend extraction across access events (including legacy payload variants) when `properties.error_info` is present
  - `azure.application_gateway.message`: extend extraction across access and firewall events from `properties.message`
  - `azure.application_gateway.serverStatus`: extend extraction for access/backend-routing events from `properties.serverStatus`
  - `azure.application_gateway.sslClientVerify`: extend extraction for TLS-enabled access events from `properties.sslClientVerify`
  - `azure.application_gateway.transactionId`: extend extraction for access and firewall correlation from `properties.transactionId`
- Cover access, firewall, and performance log types with dedicated ECS/custom stages
- Keep only high-signal Azure Application Gateway custom fields and metric fields
