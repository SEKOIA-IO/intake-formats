# Blue41

## Description

Blue41 secures AI agents at runtime. It observes agent traffic, raises detections on agent behaviour and keeps an audit trail of its own platform.

## Intakes

- **Blue41 Detections and Audit**: Blue41 detections and platform audit records delivered through HTTPS push.

Detections arrive as `event.kind: alert` when they fire and as `event.kind: event` when they resolve, so a resolve never raises a second alert. Full trace history stays in Blue41; `event.url` links each event back to it: the trace and span for a detection, the rule overview when no single span applies, or the audit log for an audit record.

`blue41.event_id` carries Blue41's own event identifier; `event.id` remains Sekoia's.
