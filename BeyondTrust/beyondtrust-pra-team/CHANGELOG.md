# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 2026-09-04

### Fixed

- Parse robustly the following ECS fields from the `data.public_ip` raw field, for both IPv4 and bracketed IPv6 values, replacing naive splitting on colon:
  - `source.nat.ip`
  - `source.nat.port`
