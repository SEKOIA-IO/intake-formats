# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-02

### Added

- Parse new ECS fields:
  - `destination.address`
  - `destination.domain`
  - `destination.ip`
  - `destination.port`
  - `event.outcome`
  - `http.response.mime_type`
  - `http.version`
  - `network.protocol`
  - `observer.product`
  - `observer.vendor`
  - `rule.id`
  - `rule.name`
  - `rule.ruleset`
  - `rule.version`
  - `tls.cipher`
  - `tls.version`
  - `tls.version_protocol`
  - `url.path`
  - `url.query`
- Parse new custom fields:
  - `azure.application_gateway.details.message`
  - `azure.application_gateway.error_info`
  - `azure.application_gateway.message`
  - `azure.application_gateway.metric.average`
  - `azure.application_gateway.metric.count`
  - `azure.application_gateway.metric.maximum`
  - `azure.application_gateway.metric.minimum`
  - `azure.application_gateway.metric.name`
  - `azure.application_gateway.metric.time_grain`
  - `azure.application_gateway.metric.total`
  - `azure.application_gateway.serverStatus`
  - `azure.application_gateway.sslClientVerify`
  - `azure.application_gateway.transactionId`

### Changed

- Extend parsing of existing ECS fields:
  - `@timestamp`: normalize performance timestamp from `time` (including fractional-second values) so metric events consistently emit `@timestamp`
  - `destination.*`: enrich firewall events when `hostname` is provided without port by setting `destination.address` and `destination.domain`/`destination.ip`
  - `event.action`: extend handling across log types
    - performance: `event.action` is populated from `metricName`
  - `event.dataset`: extend handling across log types  
    - performance: `event.dataset="ApplicationGatewayPerformance"`
    - common mapping: use only provided `operationName` to avoid classifying incomplete non-metric events as performance
  - `event.outcome`: extend normalization to all log types
    - access: success/failure from `http.response.status_code`, fallback `unknown`
    - firewall: success/failure from `event.action` semantic values, fallback `unknown`
    - performance: `unknown` by design
  - `event.type`: extend handling across log types
    - access/firewall: `event.type=["access","connection"]`
    - performance: `event.type=["info"]`
  - `network.bytes`: cast `receivedBytes` and `sentBytes` to integers before addition to preserve correct totals on legacy string payloads
  - `rule.name`: prefer top-level `ruleName` and use `listenerName` as fallback
- Cover access, firewall, and performance log types with dedicated ECS/custom stages
- Keep only high-signal Azure Application Gateway custom fields and metric fields
- Extend fixture coverage for outcome/timestamp branches and anonymization edge cases
