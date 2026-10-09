# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.3] - 2026-10-09

### Fixed

- Replace non-reserved domains in `refererURL` and `user.email` with reserved `example.*` domains in web event fixtures
- Replace public routable IP addresses with TEST-NET addresses in `test_event_web*.json` fixtures
- Update expected URL/domain derivations in web event tests after host anonymization

## [1.1.2] - 2026-08-19

### Changed

- Map `observer.vendor`, `observer.product` and `observer.type` for all events.
- Remove the non-ECS-compliant `server.ip` mapping (the value is already available in `destination.ip`).

## [1.1.1] - 2026-06-30

### Changed

- Improve firewall log parsing for blocked policy events by supporting additional field variants (`clt_sport`, `srv_dport`, `cip`, `dip`, `locationname`, `nwapp`, `elogin`) and setting `event.outcome` to `failure` when action indicates block/deny/drop.

## [1.1.0] - 2026-05-04
- Add new Zscaler Internet Access (ZIA) fields:
  - `zscaler.zia.appclass`
  - `zscaler.zia.dlpengine`
  - `zscaler.zia.dlpdictionaries`
  - `zscaler.zia.fileclass`
  - `zscaler.zia.pagerisk`
  - `zscaler.zia.unscannabletype`

## [1.0.2] - 2024-01-30

### Changed

- Change the way to handle the Url

### Fixed

- Fix the way to handle the hostname field

## [1.0.1] - 2023-09-28

### Changed

- check ip address before setting them in ECS ip address fields

## [1.0.0] - 2023-09-13

### Added

- Initial version of the format
