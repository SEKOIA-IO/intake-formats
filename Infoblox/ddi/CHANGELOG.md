# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-08-03

### Added

- Add DHCP smart descriptions

### Changed

- Update definition of IP-related ECS fields:
    - `destination.ip`: add a DHCP fallback mapping from `infoblox.dhcp.router_ip` when no native destination IP is parsed, to keep destination context available in DHCP events
    - `observer.ip`: add a DHCP fallback mapping from `infoblox.dhcp.interface_ip` (when relay interface IP is absent), because this IP represents the reporting Infoblox interface
    - `related.ip`: enrich with deduplicated IPs from `client_ip`, `infoblox.dhcp.router_ip`, and `infoblox.dhcp.interface_ip`, in line with ECS guidance to include all IPs seen in the event

### Fixed

- Improve JSON test files anonymization
