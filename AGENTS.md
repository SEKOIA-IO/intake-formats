# Instructions for agents

## Overview

This project groups all SEKOIA.io intake formats. An intake format aims to define how to parse and normalize a specific data source. Each format is defined in a module, which is a directory containing the format definition and its tests.
Read doc/ for more details.

## Environment Setup

- Install mise-en-place: `curl https://mise.run | sh`

## Commands

- Create a new module: `mise run create-module`
- Create a new format: `mise run create-format <module-directory>`
- Create a new test: `mise run create-test <format-directory>/tests/test_<test_name>.json <content of the test>`
- Run tests: `mise run test --format <format-slug>`
- Validate changes: `mise run validate`
- Fix some issues: `mise run fix`
