# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-09

### Added

- Parse new ECS fields:
  - `event.kind`
  - `network.protocol`
  - `rule.id`
  - `rule.name`
  - `rule.ruleset`
  - `source.as.number`
  - `source.geo.country_iso_code`
  - `tls.version`
  - `tls.version_protocol`
  - `http.request.body.bytes`
- Parse new custom fields:
  - `akamai.http.request.headers.content_type`
- Enrich descriptions of custom fields
- Enrich smart descriptions with bot and request metadata context

### Fixed

- Fix request/response header mix-up by extracting request payload metadata from `httpMessage.requestHeaders`:
  - `httpMessage.requestHeaders.Content-Length` raw field mapped to `http.request.body.bytes` ECS field
  - `httpMessage.requestHeaders.Content-Type` raw field mapped to `akamai.http.request.headers.content_type` custom field
- Extend ECS action classification for all Akamai WAF event variants:
  - `event.action` now falls back to the first rule action when `attackData.appliedAction` is absent
  - `event.type` is now derived from effective `event.action` and correctly returns `denied` for deny-only rule events
- Parse rule metadata consistently across event variants:
  - map `attackData.rules[].ruleTag` into `akamai.rules[].tags`
  - map `attackData.rules[].ruleSelector` into `akamai.rules[].selector`

### Removed

- Remove ECS fields:
  - `http.request.mime_type` mapping from `httpMessage.requestHeaders.Content-Type` raw field, because ECS requires MIME type detection from request body content rather than header values
