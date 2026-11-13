# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-11-06

### Added

- Parse `gatewatcher.type` (type of analysis) from `event.module`, as in the Gatewatcher AionIQ v102 format; modules without a v102 equivalent keep the raw `event.module` value

## [1.0.0] - 2026-11-05

### Added

- Initial release of the format, parsing events exported from GCenter version 2.5
- Parse new ECS fields:
  - `destination.bytes`
  - `destination.packets`
  - `event.action`
  - `http.request.referrer`
  - `network.bytes`
  - `network.packets`
  - `process.name`
  - `rule.category`
  - `rule.id`
  - `rule.version`
  - `source.bytes`
  - `source.packets`
  - `threat.framework`
  - `threat.tactic.id`
  - `threat.tactic.name`
  - `threat.technique.id`
  - `threat.technique.name`
  - `tls.client.ja3`
  - `tls.server.ja3s`
  - `tls.server.x509.serial_number`
- Parse new custom fields:
  - `gatewatcher.http.http_response_body`
  - `gatewatcher.ioc.type`
  - `gatewatcher.malcore.engines`
  - `gatewatcher.tls.ja3.string`
  - `gatewatcher.tls.ja3s.string`
- Add smart descriptions for AD Guardian alerts and for DNS, HTTP, SMTP and TLS metadata

### Changed

- Extend parsing of existing ECS fields:
  - `dns.id`, `dns.op_code` and `dns.type` (from the first query item of DNS query records)
  - `dns.question.name` and `dns.question.type` (from DNS answer records)
  - `email.from.address` and `email.to.address` (from the SMTP envelope when the email headers are absent)
  - `event.kind` (set on every event)
  - `event.start` (from the flow start when the event has no start date)
- Run each mapping stage only when the matching raw object is present
- Guard every smart description placeholder with presence conditions

### Fixed

- Fix existing ECS fields:
  - `dns.answers` (no longer swap name and type, and no longer build an empty answer without data)
  - `email.from.address`, `email.reply_to.address` and `email.to.address` (set as arrays of bare addresses)
  - `event.type` (use values allowed for the event categories: `allowed`/`denied` from the Sigflow action, `indicator` for threat events, `protocol` for network metadata, `info` otherwise)
  - `http.response.body.content` (use the printable body instead of the base64-encoded one)
  - `threat.indicator.marking.tlp` (normalize to the ECS uppercase values, unset when unknown)
  - `threat.indicator.type` (normalize to the ECS expected values, unset when unknown)
  - `tls.server.hash.md5`, `tls.server.hash.sha1` and `tls.server.hash.sha256` (uppercase, without colons)
- Fix existing custom fields:
  - `gatewatcher.file.sid`, `gatewatcher.ike.payload`, `gatewatcher.metadata.flowbits`, `gatewatcher.smb.client_dialects`, `gatewatcher.smtp.rcpt_to` and the other list fields (declare as `array`)
  - Declare identifiers, hashes, enumerations and names as `keyword` instead of `text`
  - Declare boolean fields as `boolean` and date fields as `date`
- Fix the smart descriptions of Beacon, NBA and Sigflow alerts, which referenced fields that are not parsed

### Removed

- Remove ECS fields:
  - `dns.question.class` (was filled with the record type)
  - `ecs.version`
  - `network.application` (was filled with the syslog application name, now in `process.name`)
  - `related.hash`, `related.hosts` and `related.ip` (computed by the ingestion pipeline)
- Remove custom fields:
  - `gatewatcher.flow.bytes_toclient` and `gatewatcher.flow.bytes_toserver` (now in `source.bytes` and `destination.bytes`)
  - `gatewatcher.flow.pkts_toclient` and `gatewatcher.flow.pkts_toserver` (now in `source.packets` and `destination.packets`)
  - `gatewatcher.flow.start` (now in `event.start`)
  - `gatewatcher.http.http_refer` (now in `http.request.referrer`)
  - `gatewatcher.http.http_response_body_printable` (now in `http.response.body.content`)
  - `gatewatcher.malcore.engine_id0` to `gatewatcher.malcore.engine_id15` (now in `gatewatcher.malcore.engines`)
  - `gatewatcher.sigflow.action` (now in `event.action`)
  - `gatewatcher.sigflow.category` (now in `rule.category`)
  - `gatewatcher.sigflow.rev` (now in `rule.version`)
  - `gatewatcher.sigflow.signature_id` (now in `rule.id`)
  - `gatewatcher.threat` and `gatewatcher.threat.techniques` (now in `threat.*`)
  - `gatewatcher.tls.ja3.hash` (now in `tls.client.ja3`)
  - `gatewatcher.tls.ja3s.hash` (now in `tls.server.ja3s`)
  - `gatewatcher.tls.serial` (now in `tls.server.x509.serial_number`)
