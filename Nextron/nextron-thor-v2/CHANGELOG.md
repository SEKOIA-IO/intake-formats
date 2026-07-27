# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Detection rule fields: `rule.name` now holds the bare rule identifier
  (`reasons[0].signature.rulename`) instead of the composite reason name; `rule.id`
  keeps that same identifier (for Sigma, `rule.name` is still overridden by the
  engine's rule title while `rule.id` retains the rulename). `rule.description` is
  recovered from the composite reason name (the part after the first ` / `) for
  plain YARA/Sigma matches where `signature.description` is empty.

### Added

- Initial parser for Nextron THOR APT scanner JSON logs (log_version v2.x)
- Linux field coverage (validated against THOR 10.7.31 `--jsonv2` output):
    - ServiceCheck: systemd units (`unit`, `unit_path`, `executable`+`sha1` → `file.*`,
      `command`, `exe_magic` → `thor.file.type`, `exe_mode`/`unit_mode`/`unit_group`/`run_as_group`)
    - Cron module: executed-file objects → `file.*`, crontab entries (`schedule`/`command`)
      and environment settings (`variable`/`value`)
    - Users: `home`, `shell`, `groupid`; UserDir profile `created`/`modified` timestamps
    - Startup: `kernel_version` → `host.os.kernel`, `kernel_name`
    - Hosts: mapped address → `related.ip`
    - Process image: `type`, `size`, `firstbytes`, `changed` (ctime)
    - File objects: `changed` → `file.ctime` (Linux ctime)
    - Findings: top match content (`reasons[0].matched`) → `thor.matched`, `signature.ruledate`
