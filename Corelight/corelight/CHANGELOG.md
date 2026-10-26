# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-10-26 - 1.1.0

### Added

- Parse the 47 other log types a Corelight sensor exports: `conn_long`, `ssh`, `kerberos`, `ntlm`, `ldap`, `ldap_search`, `dce_rpc`, `smtp`, `smtp_links`, `smb_files`, `smb_mapping`, `ftp`, `x509`, `pe`, `dhcp`, `rdp`, `quic`, `ntp`, `snmp`, `mysql`, `tunnel`, `ipsec`, `ocsp`, `encrypted_dns`, `software`, `known_users`, `weird`, `dnp3`, `modbus`, `s7comm`, `known_hosts`, `known_services`, `known_certs`, `known_domains`, `known_names`, `known_devices`, `modbus_detailed`, `modbus_read_device_identification`, `cotp`, `s7comm_read_szl`, `dnp3_objects`, `dnp3_control`, `enip`, `etc_viz`, `analyzer`, `unknown_protocols`, `generic_dns_tunnels`
- Parse new ECS fields:
  - every log type: `observer.hostname`
  - `conn` and `conn_long`: `destination.as.number`, `destination.as.organization.name`, `destination.geo.city_name`, `destination.geo.country_iso_code`, `destination.geo.country_name`, `destination.mac`, `destination.packets`, `network.iana_number`, `source.as.number`, `source.as.organization.name`, `source.geo.city_name`, `source.geo.country_name`, `source.mac`, `source.packets`
  - `dns`: `dns.header_flags`, `dns.id`, `dns.question.class`, `event.outcome`, `network.protocol`, `network.transport`
  - `http`: `destination.domain`, `http.request.mime_type`, `http.request.referrer`, `http.response.mime_type`, `http.version`, `network.transport`, `source.user.name`
  - `ssl`: `destination.domain`, `event.outcome`, `network.transport`, `tls.client.issuer`, `tls.client.subject`, `tls.next_protocol`, `tls.resumed`, `tls.server.issuer`, `tls.server.subject`
  - `files`: `destination.ip`, `event.duration`, `file.name`, `network.protocol`, `source.ip`
  - `suricata_corelight`: `rule.version`
  - `intel`: `threat.indicator.provider`
  - `notice`: `destination.ip`, `destination.port`, `event.severity`, `file.mime_type`, `network.transport`, `source.ip`
  - `ssh`: `destination.geo.city_name`, `destination.geo.country_iso_code`, `destination.geo.region_name`, `event.category`, `event.outcome`, `event.type`, `network.direction`, `network.protocol`, `network.transport`, `source.geo.city_name`, `source.geo.country_iso_code`, `source.geo.region_name`
  - `kerberos`: `error.code`, `error.message`, `event.action`, `event.category`, `event.outcome`, `event.type`, `network.protocol`, `source.user.domain`, `source.user.name`, `tls.client.x509.subject.distinguished_name`, `tls.server.x509.subject.distinguished_name`
  - `ntlm`: `destination.domain`, `event.category`, `event.outcome`, `event.type`, `network.protocol`, `network.transport`, `source.domain`, `source.user.domain`, `source.user.name`
  - `ldap`: `event.action`, `event.category`, `event.outcome`, `event.type`, `network.protocol`
  - `ldap_search`: `event.action`, `event.type`, `network.protocol`
  - `dce_rpc`: `event.action`, `event.type`, `network.protocol`
  - `smtp`: `email.cc.address`, `email.from.address`, `email.message_id`, `email.origination_timestamp`, `email.reply_to.address`, `email.sender.address`, `email.subject`, `email.to.address`, `event.category`, `event.type`, `network.protocol`, `tls.established`, `user_agent.original`
  - `smtp_links`: `event.category`, `event.type`, `network.protocol`, `url.domain`, `url.original`
  - `smb_files`: `event.action`, `event.category`, `event.type`, `file.accessed`, `file.created`, `file.ctime`, `file.directory`, `file.mtime`, `file.name`, `file.size`, `network.protocol`, `network.transport`
  - `smb_mapping`: `event.type`, `network.protocol`, `network.transport`
  - `ftp`: `event.action`, `event.outcome`, `event.type`, `file.directory`, `file.mime_type`, `file.size`, `network.protocol`, `source.user.name`
  - `x509`: `event.category`, `event.type`, `file.hash.sha256`, `file.x509.alternative_names`, `file.x509.issuer.distinguished_name`, `file.x509.not_after`, `file.x509.not_before`, `file.x509.public_key_algorithm`, `file.x509.public_key_curve`, `file.x509.public_key_exponent`, `file.x509.public_key_size`, `file.x509.serial_number`, `file.x509.signature_algorithm`, `file.x509.subject.distinguished_name`, `file.x509.version_number`
  - `pe`: `event.category`, `event.type`, `file.pe.architecture`
  - `dhcp`: `destination.ip`, `event.duration`, `event.type`, `host.hostname`, `network.protocol`, `network.transport`, `source.ip`, `source.mac`
  - `rdp`: `event.outcome`, `event.type`, `network.protocol`, `tls.established`
  - `quic`: `event.type`, `network.protocol`, `network.transport`, `tls.client.server_name`, `user_agent.original`
  - `ntp`: `event.type`, `network.protocol`, `network.transport`
  - `snmp`: `event.duration`, `event.type`, `network.protocol`, `network.transport`
  - `mysql`: `event.action`, `event.outcome`, `event.type`, `network.protocol`
  - `tunnel`: `event.type`
  - `ipsec`: `event.type`, `network.protocol`, `network.transport`
  - `ocsp`: `event.category`, `event.type`
  - `encrypted_dns`: `destination.ip`, `event.category`, `event.type`, `network.protocol`, `tls.client.server_name`, `tls.server.x509.alternative_names`, `tls.server.x509.subject.common_name`
  - `software`: `event.type`, `host.ip`, `package.name`, `package.version`, `url.original`
  - `known_users`: `destination.ip`, `event.duration`, `event.type`, `host.ip`, `network.protocol`, `user.name`
  - `weird`: `event.action`, `event.type`
  - `dnp3`: `event.type`, `network.protocol`, `network.transport`
  - `modbus`: `event.action`, `event.type`, `network.protocol`, `network.transport`
  - `s7comm`: `event.type`, `network.protocol`
  - `known_hosts`: `event.category`, `event.duration`, `event.type`, `host.ip`
  - `known_services`: `destination.ip`, `destination.port`, `event.duration`, `event.type`, `host.ip`, `network.protocol`, `network.transport`
  - `known_certs`: `destination.ip`, `destination.port`, `event.category`, `event.duration`, `event.type`, `file.hash.sha1`, `file.x509.issuer.distinguished_name`, `file.x509.serial_number`, `file.x509.subject.distinguished_name`, `host.ip`, `network.transport`
  - `known_domains`: `destination.domain`, `event.category`, `event.duration`, `event.type`, `host.ip`, `network.protocol`
  - `known_names`: `event.category`, `event.duration`, `event.type`, `host.hostname`, `host.ip`, `host.name`, `network.protocol`
  - `known_devices`: `event.category`, `event.duration`, `event.type`, `host.ip`, `host.mac`, `network.protocol`
  - `modbus_detailed`: `event.action`, `event.type`, `network.protocol`
  - `modbus_read_device_identification`: `event.action`, `event.type`, `network.protocol`
  - `cotp`: `event.action`, `event.type`, `network.protocol`
  - `s7comm_read_szl`: `event.action`, `event.outcome`, `event.type`, `network.protocol`
  - `dnp3_objects`: `event.action`, `event.type`, `network.protocol`
  - `dnp3_control`: `event.action`, `event.outcome`, `event.type`, `network.protocol`
  - `enip`: `event.action`, `event.outcome`, `event.type`, `network.protocol`
  - `etc_viz`: `destination.ip`, `destination.port`, `event.type`
  - `analyzer`: `error.message`, `event.outcome`, `event.type`, `network.protocol`, `network.transport`
  - `unknown_protocols`: `event.type`
  - `generic_dns_tunnels`: `dns.question.registered_domain`, `event.category`, `event.kind`, `event.type`, `network.protocol`, `source.ip`
- Parse new custom fields, under one `corelight.<log type>.*` namespace per log type, plus the `corelight.fuid`, `corelight.kuid` and `corelight.uids` join keys; each one is declared with its type and description in `_meta/fields.yml`
- Add a smart description for every dataset, with a fallback that needs no optional field

### Changed

- `http` and `ssl`: `destination.domain` is now set from the `Host:` header and from the SNI, so the platform derives `destination.address` from that domain instead of the destination IP
- `intel`: the intelligence sources move from `corelight.intel.sources` to `threat.indicator.provider`
- `notice`: keep the raw event in the top-level `message` field; the notice text is exposed as `corelight.notice.message`
- `suricata_corelight`: also map `alert.action` to `event.action`, in addition to `action.name`
- `conn`: `source.user.roles` is emitted as an array and `event.duration` as an integer (nanoseconds)
- Detection rules reference the relevant Zeek and Suricata documentation instead of a generic integration link

### Fixed

- Parse the events wrapped in a one-element JSON array (`[{...}]`); an array holding several events is still rejected as a whole
- `conn`: report the volume of a connection that carries no payload, from `orig_ip_bytes` / `resp_ip_bytes` when Zeek omits `orig_bytes` / `resp_bytes`
- `dns`: keep `dns.answers` when an answer contains double quotes, as TXT records do

## 2026-06-17 - 1.0.0

### Added

- Initial Corelight Open NDR intake format.
- Parsing of Zeek/Corelight logs: `conn`, `dns`, `http`, `ssl`, `files`, `notice` and the Zeek Intelligence Framework (`intel`).
- Parsing of Suricata IDS alerts (`suricata_corelight`).
- Mapping of Corelight entity enrichment (`enrichment_orig.user`, `enrichment_orig.role`, `enrichment_orig.city_location`) to ECS.
