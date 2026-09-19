# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for the authentication and lateral movement logs the sensor already sends: `ssh.log`, `kerberos.log`, `ntlm.log`, `ldap.log`, `ldap_search.log` and `dce_rpc.log`. They were received but left unparsed, so only the envelope (timestamps, addresses, `event.dataset`) reached the events.
- `ssh.log`: map the client and server version strings, the negotiated algorithms, the HASSH fingerprints and the host key, plus `network.direction` and `event.outcome` from `auth_success`.
- `kerberos.log`: split the `client` principal into `source.user.name` and `source.user.domain`, and map the request type, the requested service, the ticket flags and the KDC error.
- `ntlm.log`: map the account to `source.user.name` / `source.user.domain`, the client and server names to `source.domain` / `destination.domain`, and `event.outcome` from `success`.
- `ldap.log` and `ldap_search.log`: map the operation, its result, the search base, scope and filter. Only a bind is reported under the `authentication` event category; the other operations stay directory operations.
- `dce_rpc.log`: map the endpoint, the operation and the named pipe, which is how SMB-carried RPC abuse (`samr`, `svcctl`, `drsuapi`) becomes visible.

### Changed

- `notice.log`: keep the raw event in the top-level `message` field; the notice text is now exposed as `corelight.notice.message`.
- `suricata_corelight`: also map `alert.action` to `event.action` (in addition to `action.name`).
- `conn.log`: `source.user.roles` is now emitted as an array; `event.duration` is now emitted as an integer (nanoseconds).
- Detection rules now reference the relevant Zeek/Suricata documentation instead of a generic integration link.

## 2026-06-17 - 1.0.0

### Added

- Initial Corelight Open NDR intake format.
- Parsing of Zeek/Corelight logs: `conn`, `dns`, `http`, `ssl`, `files`, `notice` and the Zeek Intelligence Framework (`intel`).
- Parsing of Suricata IDS alerts (`suricata_corelight`).
- Mapping of Corelight entity enrichment (`enrichment_orig.user`, `enrichment_orig.role`, `enrichment_orig.city_location`) to ECS.
