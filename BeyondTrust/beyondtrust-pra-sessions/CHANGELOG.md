# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-04

### Added

- Parse new ECS fields for participant identity and endpoint context in session events:
  - `destination.ip`
  - `destination.nat.ip`
  - `destination.nat.port`
  - `destination.user.full_name`
  - `destination.user.id`
  - `user.id`

- Parse new custom fields for the session representative and the session counters:
  - `beyondtrust.pra.destination_gsnumber`
  - `beyondtrust.pra.file_delete_count`
  - `beyondtrust.pra.file_move_count`
  - `beyondtrust.pra.file_transfer_count`
  - `beyondtrust.pra.primary_rep.gsnumber`
  - `beyondtrust.pra.primary_rep.name`

- Resolve the primary participants from the session-level `customer_list` and `rep_list` when the event references them by `gsnumber` only

### Changed

- Extend parsing of existing ECS fields for events carrying participant `public_ip`:
  - `source.nat.ip`
  - `source.nat.port`
- Anchor the grok pattern extracting the NAT address and port, to reject partial matches
- Filter the literal `Unknown` locally for `host.os.full`, instead of ignoring that value globally
