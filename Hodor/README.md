# Hodor

## Description

Hodor governs AI agent access to business applications through identities, contracts and policies.

## Intakes

- **Hodor Activity**: version 1 MCP tool-call activity events delivered through HTTPS push.

The parser receives the Hodor JSON envelope extracted by the HTTPS intake from the
transport's `json` field. The intake key is a transport credential and is not part
of the event or its test fixtures.

The format preserves the human actor separately from the AI agent, and records
the provider, workspace, contract and outcome. `hodor.event_id` is the original
delivery identifier; `event.id` remains Sekoia's event identifier.

Hodor's `result.is_error` determines the outcome. A failed call is not necessarily
a policy denial. `hodor.status_code` carries Hodor's fault-attributing status,
which can differ from the provider's HTTP response status.

The format covers the activity feed. Configuration-change and authentication
audit events from Hodor's separate audit pipeline are outside this integration.

## Fixture identifiers

The test events are synthetic and use numeric workspace and profile IDs, as emitted by Hodor. The anonymization exception for `organization.id = "11111111"` preserves that numeric workspace ID instead of substituting the checker's text-only organization placeholder.
