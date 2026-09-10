# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-10

### Added

- Parse new ECS fields:
  - `event.kind`
  - `http.request.body.bytes`
  - `network.protocol`
  - `rule.id`
  - `rule.name`
  - `rule.ruleset`
  - `source.as.number`
  - `source.geo.country_iso_code`
  - `tls.version`
  - `tls.version_protocol`
- Parse new custom fields:
  - `akamai.http.request.headers.content_type`
- Enrich descriptions of custom fields
- Enrich smart descriptions with bot and request metadata context

### Deprecated

- Keep ECS field `http.request.mime_type` population from request headers (raw field `httpMessage.requestHeaders.Content-Type`) for backward compatibility but deprecate it:
  - indeed, ECS requires MIME type detection from request body content rather than header values
  - for new detections and rules, prefer custom field `akamai.http.request.headers.content_type` for declared header value and keep ECS field `http.request.body.bytes` for payload-size context

### Fixed

- Fix request/response header mix-up by extracting request payload metadata from raw field `httpMessage.requestHeaders`:
  - raw field `httpMessage.requestHeaders.Content-Length` mapped to ECS field `http.request.body.bytes`
  - raw field `httpMessage.requestHeaders.Content-Type` mapped to custom field `akamai.http.request.headers.content_type`
- Extend ECS action classification for all Akamai WAF event variants:
  - ECS field `event.action` now falls back to the first rule action when raw field `attackData.appliedAction` is absent
  - ECS field `event.type` is now derived from effective ECS field `event.action` and correctly returns `denied` for deny-only rule events
- Parse rule metadata consistently across event variants:
  - map raw field `attackData.rules[].ruleTag` into custom field `akamai.rules[].tags`
  - map raw field `attackData.rules[].ruleSelector` into custom field `akamai.rules[].selector`
