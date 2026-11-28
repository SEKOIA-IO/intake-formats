# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Extract Guardian Air wireless context from asset events (network.name, network.protocol, region, activation, channel, and numeric RSSI, SNR, and noise).
- Extract asset mobility, location source, geofencing area, zones, technology category, and risk.
- Map asset coordinates to host.geo.location.lat and host.geo.location.lon only when both coordinates are present.
- Add a smart description for wireless assets.
