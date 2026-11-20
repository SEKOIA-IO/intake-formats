# HodeiShield

## Description

HodeiShield is a supply-chain risk platform that monitors the vendors of an organization and raises alerts about breaches, vulnerabilities and rating changes.

## Intakes

- **HodeiShield Alerts**: supply-chain alerts delivered through HTTPS push.

The parser receives the alert JSON object as the event message. It is the alert
object of the HodeiShield public API (`/v1/alerts`) plus an `event_id` field, a
delivery identifier that stays the same when an alert is retried. The intake key
is a transport credential and is not part of the event or its test fixtures.

`hodeishield.event_id` carries the delivery identifier; `event.id` remains the
Sekoia.io event identifier. Delivery is at least once, so `hodeishield.event_id`
can be used to drop duplicates.

## Fixture identifiers

The test events are synthetic. Identifiers are random UUIDs and URLs use `example.com`.
