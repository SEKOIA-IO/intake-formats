# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-12

### Added

- Parse new ECS fields for Cloud WAF access and security events:
  - `client.geo.country_iso_code` from raw field `ccode`
  - `destination.ip` from raw field `sip`
  - `destination.port` from raw field `spt`
  - `http.request.body.content` from raw field `postbody`
  - `http.response.body.bytes` from raw field `in`
  - `organization.id` from raw field `suid`
  - `rule.category` from raw field `Name` (CEF header, excluding `Normal`)

### Changed

- Extend parsing of existing ECS fields:
  - `event.reason`: describe challenges reported as `REQ_CHALLENGE_*` as well as `REQ_CHALLENGED_*`
  - `event.type`: classify `REQ_CHALLENGE_*` requests as denied connections
- Extend parsing of existing custom fields:
  - `imperva.attack.id`: accept raw field `filePermission` in addition to `filepermission`
  - `imperva.attack.type`: accept raw field `fileType` in addition to `filetype`

### Fixed

- Fix existing ECS fields:
  - `destination.ip`: omit unspecified IPv4 and IPv6 addresses from raw field `sip`
  - `destination.port`: omit port zero from raw field `spt`
  - `http.request.bytes`: remove the incorrect mapping of `in`, which represents response body bytes, and use `http.response.body.bytes` instead
  - `network.forwarded_ip`: extract and validate the first trimmed address from the `X-Forwarded-For` chain
