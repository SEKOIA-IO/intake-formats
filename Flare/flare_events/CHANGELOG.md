# Changelog

## [Unreleased]

## 2026-11-26

### Fixed

- Build lists and dicts without mutating them in place (`.append`, `.update`, ...), which not every Jinja engine supports

## 2026-11-24

### Changed

- Read a missing field like a `null` one, so that events keep the same parsing when the connector stops sending the fields set to `null`

## 2026-11-18

### Added

- Add `flare.events.truncated_fields`: the fields the connector cut to fit the intake size limit (from 0.6.7)

## 2026-11-17

### Changed

- Date events by when Flare matched the item to the tenant (`metadata.matched_at`, added by the connector from 0.6.5), as in Flare's feed, instead of the item's own date, which can be years old. Events without it keep the item's date

### Added

- Parse the item's own date in `flare.events.created_at`

## 2026-11-02

### Added

- Add support for Flare `cc` events (stolen credit card listings, source `TXN`) through a dedicated parsing stage
- Parse new custom fields:
  - `flare.events.cc.bank`
  - `flare.events.cc.bin`
  - `flare.events.cc.brand`
  - `flare.events.cc.country`
  - `flare.events.cc.expiration`
  - `flare.events.cc.has_cvv`
  - `flare.events.cc.has_date_of_birth`
  - `flare.events.cc.has_mother_maiden_name`
  - `flare.events.cc.has_phone`
  - `flare.events.cc.has_pin`
  - `flare.events.cc.has_ssn`
  - `flare.events.cc.has_track_1`
  - `flare.events.cc.has_vbv`
  - `flare.events.cc.state`
  - `flare.events.cc.zip`
- Add smart descriptions for stolen credit card events
- Add a generic fallback smart description for events without a title (for example leaked credentials, or stealer logs without host details)

## 2026-08-03

### Added

- Add new Flare detection rules for:
    - high-severity exposure
    - leaked credentials with exposed passwords
    - stealer-log malware infection

## 2026-06-08

- Create initial Flare Events intake format.
- Add parser for common Flare envelope and major event subtypes.
- Add custom taxonomy and parsing tests.
