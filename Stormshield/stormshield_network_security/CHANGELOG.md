# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Full support for `monitor` log type including:
  - System and security status indicators
  - CPU usage metrics (user, kernel, interrupts)
  - PVM (Patch and Vulnerability Manager) metrics with vulnerability counts and classifications
  - Network interface statistics for up to 10 Ethernet interfaces (ethernet0-9)
  - Network interface statistics for up to 10 Aggregate interfaces (agg0-9)
  - Network interface statistics for up to 10 VLAN interfaces (vlan0-9)
  - QoS queue statistics for up to 20 queues (qid0-19)
  - Each interface extracts 7 metrics: name, ingress_bps, ingress_bps_max, egress_bps, egress_bps_max, packets_accepted, packets_blocked
- Smart descriptions for monitor logs covering system status, PVM vulnerabilities, and network interface traffic
