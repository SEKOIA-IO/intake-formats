# Corelight

## Description

Corelight is an Open NDR (Network Detection and Response) platform built on Zeek
and Suricata. Corelight sensors transform raw network traffic into rich,
structured logs and Suricata IDS alerts, providing network ground-truth evidence
for threat detection, threat hunting and incident response.

Corelight sensors push their logs as JSON to Sekoia.io over HTTP(S) or Syslog
(TLS). No automation connector is required for this integration — the sensor
sends the events directly to the Sekoia.io intake.

## Intakes

- [Corelight](corelight) — Parses the 55 log types a Corelight sensor exports and
  normalizes them to the Sekoia Extended ECS format. Ships 111 smart
  descriptions and 7 detection rules.
  - Connections and core protocols: `conn`, `conn_long`, `dns`, `http`, `ssl`,
    `files`, `quic`, `ntp`, `snmp`, `mysql`, `dhcp`, `rdp`, `tunnel`, `ipsec`,
    `ocsp`, `etc_viz`, `analyzer`, `unknown_protocols`, `weird`.
  - Detections: Suricata IDS alerts (`suricata_corelight`), `notice`, `intel`,
    `encrypted_dns`, `generic_dns_tunnels`.
  - Authentication and lateral movement: `ssh`, `kerberos`, `ntlm`, `ldap`,
    `ldap_search`, `dce_rpc`, `smb_files`, `smb_mapping`.
  - Mail, file transfer and file metadata: `smtp`, `smtp_links`, `ftp`, `x509`,
    `pe`.
  - Entity inventory: `known_hosts`, `known_services`, `known_certs`,
    `known_domains`, `known_names`, `known_devices`, `known_users`, `software`.
  - Industrial control: `modbus`, `modbus_detailed`,
    `modbus_read_device_identification`, `dnp3`, `dnp3_objects`,
    `dnp3_control`, `s7comm`, `s7comm_read_szl`, `cotp`, `enip`.
