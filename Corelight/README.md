# Corelight

## Description

Corelight is an Open NDR (Network Detection and Response) platform built on Zeek
and Suricata. Corelight sensors transform raw network traffic into rich,
structured logs (connections, DNS, HTTP, SSL/TLS, files, notices) and Suricata
IDS alerts, providing network ground-truth evidence for threat detection,
threat hunting and incident response.

Corelight sensors push their logs as JSON to Sekoia.io over HTTP(S) or Syslog
(TLS). No automation connector is required for this integration — the sensor
sends the events directly to the Sekoia.io intake.

## Intakes

- [Corelight](corelight) — Parses Corelight/Zeek logs (`conn`, `dns`, `http`,
  `ssl`, `files`, `notice`, `intel`) and Suricata IDS alerts
  (`suricata_corelight`), normalizing them to the Sekoia Extended ECS format.
  Ships 8 smart descriptions and 7 detection rules.
