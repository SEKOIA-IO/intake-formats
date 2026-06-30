# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-06-30 - 1.1.1

### Changed

- Improve firewall log parsing for blocked policy events by supporting additional field variants (`clt_sport`, `srv_dport`, `cip`, `dip`, `locationname`, `nwapp`, `elogin`) and setting `event.outcome` to `failure` when action indicates block/deny/drop.

## 2026-05-04 - 1.1.0
- Add new Zscaler Internet Access (ZIA) fields:
    - zscaler.zia.appclass
    - zscaler.zia.dlpengine
    - zscaler.zia.dlpdictionaries
    - zscaler.zia.fileclass
    - zscaler.zia.pagerisk
    - zscaler.zia.unscannabletype

## 2024-01-30 - 1.0.2

### Changed

- Change the way to handle the Url

### Fixed

- Fix the way to handle the hostname field

## 2023-09-28 - 1.0.1

### Changed

- check ip address before setting them in ECS ip address fields

## 2023-09-13 - 1.0.0

### Added

- Initial version of the format
