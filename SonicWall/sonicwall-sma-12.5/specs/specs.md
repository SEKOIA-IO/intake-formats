# Specs - SonicWall SMA 100 Series 12.5.0

## Table of Contents

- [Overview](#overview)
- [Specifications](#specifications)
  - [All log types](#all-log-types)
  - [1. System Message Log](#1-system-message-log)
  - [2. Management Message Log](#2-management-message-log)
  - [3. Management Audit Log](#3-management-audit-log)
  - [4. Management Access Log](#4-management-access-log)
  - [5. Network Tunnel Audit Log](#5-network-tunnel-audit-log)
  - [6. Web Proxy Audit Log](#6-web-proxy-audit-log)
  - [7. Unregistered Device Log Messages](#7-unregistered-device-log-messages)
  - [8. WorkPlace Logs](#8-workplace-logs)
- [Notes](#notes)

## Overview

SonicWall Secure Mobile Access (SMA) 100 Series 12.5.0 log types, in the same order as [official documentation](https://www.sonicwall.com/support/technical-documentation/docs/sma_1000-12-5-admin_guide/Content/Appendix/log-file-output-formats.htm):

1. **System Message Log** - Core system/service logs and policy decisions
2. **Management Message Log** - AMC operational logs
3. **Management Audit Log** - Administrative configuration changes
4. **Management Access Log** - Administrative console HTTP access
5. **Network Tunnel Audit Log** - Tunnel and flow records
6. **Web Proxy Audit Log** - Web proxy HTTP access records
7. **Unregistered Device Log Messages** - Exported XML report of unregistered devices
8. **WorkPlace Logs** - WorkPlace portal shortcut and authorization troubleshooting logs

## Specifications

### All log types

#### Fields

##### Static fields

| Field to extract | Value | Log Types |
| --- | --- | --- |
| event.kind | "event" | All |
| observer.vendor | "SonicWall" | All |
| observer.product | "Secure Mobile Access" | All |
| observer.type | "firewall" | All |

---

### 1. System Message Log

#### File

`/var/log/aventail/access_servers.log`  

#### Format

Syslog  

#### Log Format

`[DATESTAMP] [HOSTNAME] [PID] [SOURCE ID] [LEVEL] [TYPE MESSAGE]`

#### Example Log Entry

```
[29/Jul/2025:14:02:38.051761 +0000] wmperry-12-5-0-01740-default-standalone 000000 kp 0000020a Internl Misc <KERNEL> created channel (pid=6268):0000000021ce9936
```

##### Additional Information from System Message Sub-Docs

- **Access Policy Decision Example**

```
[6/3/2025 00:32:36.115] E-Class SMASSLVPN 002421 ps 100004b3 Info EWACL User ' (192.168.136.70 (Dominique Daba)@(Students)' connecting from '192.168.136.70:37975' matched rule 'accessRule(AV1091719670706:preauth access rule)', access to '127.0.0.1:455' is permitted.
```

- **EPC Interrogation Example**

```
[6/3/2025 00:32:36.115 +0000] E-Class SMASSLVPN 027186 uk 00000001 Verbose System ::API::QAABA145dFYNZimCKNWHB7p2q2Y=::(timwillis)@(Students)::CLIENT:: Interrogation: Evaluation of OPSWATAV AV1128462569762A [NortonAV.dll,Symantec Corp.,Symantec Client Security,>=,9.x,,,,,FALSE] results: FALSE
```

- **Client Certificate Error Example**

```
[02/Jul/2025:18:47:29.113075 +0000] SMAnode 013581 ps 00000000 Info System Auth: CRL-CERT: Cert verification status = 0, err = 19, reason = 'self-signed certificate in certificate chain', subject='/C=US/ST=Washington/L=Seattle/O=SonicWall/OU=Engineering/CN=Untrusted CA'
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["host"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.system" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | DATESTAMP | RFC 3339 format |
| event.severity | LEVEL | Error->3, Warning->4, Info->6, Verbose->7, Internal->0 |
| message | TYPE MESSAGE | Full message text |
| observer.hostname | HOSTNAME | Appliance hostname |
| process.name | TYPE MESSAGE | App ID (`ap`, `cp`, `dc`, `ev`, `ew`, `fm`, `kp`, `ks`, `kt`, `ls`, `ps`, `pt`, `uk`, `up`, `us`) |
| process.pid | PID | Process ID |
| source.address | SOURCE ID | Source identifier as logged |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.app_id | TYPE MESSAGE | Application/service identifier |
| sonicwall.sma.certificate.error_code | TYPE MESSAGE | Certificate verification error code |
| sonicwall.sma.certificate.error_reason | TYPE MESSAGE | Certificate verification reason |
| sonicwall.sma.epc.query_result | TYPE MESSAGE | EPC evaluation result |
| sonicwall.sma.policy.log_type | TYPE MESSAGE | Access policy log type (`CSACL`, `EWACL`, `WPACL`, `NEACL`) |

---

### 2. Management Message Log

#### File

`/var/log/aventail/management.log`  

#### Format

Management service operational log  

#### Log Format

`[DATESTAMP] [SERVICE@HOSTNAME] [local4.LEVEL] [AMC:] [DATE] [TIME] [TIMEZONE] [LEVEL] [MESSAGE]`

#### Example Log Entry

```
2025-07-25T12:31:06+00:00 AMC@wmperry-12-5-0-dev-gf048f7ae-default-standalone.sma local4.info AMC: 2025-07-25 12:31:06 +0000 INFO com.aventail.mgmt.rest.console.centralmanagement.managed.sharedstate.TrafficOptimizerConfigurationResource12_2 - Clearing traffic optimizer configuration
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["host"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.management_message" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | DATESTAMP | RFC 3339 timestamp at line start |
| event.provider | AMC: | Provider marker |
| event.severity | LEVEL | Severity mapping |
| event.start | DATE | Optional internal date |
| event.start | TIME | Optional internal time |
| event.timezone | TIMEZONE | Internal timezone |
| log.level | local4.LEVEL | Syslog level part after `.` |
| message | MESSAGE | Full message text |
| observer.hostname | SERVICE@HOSTNAME | Hostname part after `@` |
| service.name | SERVICE@HOSTNAME | Service part before `@` |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.management.class_name | MESSAGE | Java class extraction (if needed) |
| sonicwall.sma.syslog_facility | local4.LEVEL | Syslog facility (`local4`) |

---

### 3. Management Audit Log

#### File

`/var/log/aventail/consoleaudit.log`  

#### Format

Custom text log  

#### Log Format

`[level] [date] [time] [username] [message]`

#### Example Log Entry

```
Info 6/3/2025 00:31:02 admin Applied configuration changes
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["configuration"] |
| event.type | ["change"] |
| event.dataset | "sonicwall.sma.management_audit" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | date | Combined with `time` |
| @timestamp | time | Combined with `date` |
| event.severity | level | Error->3, Warning->4, Info->6, Verbose->7 |
| message | message | Change description |
| user.name | username | Admin username |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.change_type | message | Derived change category |

---

### 4. Management Access Log

#### File

`/var/log/aventail/management_access.log`  

#### Format

Common Log Format (CLF) for HTTP  

#### Log Format

`[SOURCE] [USERNAME] [DATETIME TIMEZONE] [HTTP REQUEST LINE] [STATUS] [BYTESOUT]`

#### Example Log Entry

```
127.0.0.1 - admin [25/Jul/2025:05:30:52 -0700] "GET /Console/PendingChanges HTTP/1.1" 200 308
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["network"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.management_access" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | DATETIME TIMEZONE | RFC 3339 format |
| http.request.method | HTTP REQUEST LINE | Method extraction |
| http.response.bytes | BYTESOUT | Body bytes |
| http.response.status_code | STATUS | HTTP status |
| http.version | HTTP REQUEST LINE | HTTP version extraction |
| source.ip | SOURCE | Source IP |
| url.path | HTTP REQUEST LINE | URI extraction |
| user.name | USERNAME | Admin user |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.console_action | HTTP REQUEST LINE | Derived action |
| sonicwall.sma.http_status_class | STATUS | Status class derivation |

---

### 5. Network Tunnel Audit Log

#### File

`/var/log/aventail/extranet_access.log`  

#### Format

Custom tunnel/flow records  

#### Log Format

`[source ip] [username @ realm] [date/time] [tunnel protocol version] ["tunnel"] [client vip4, client vip6] [error code] [bytes received] [bytes sent] [duration] [platform prefix] [equipment id]`  
`[source ip] [username @ realm] [date/time] [tunnel protocol version] ["flow:"protocol] [destination ip] [error code] [bytes received] [bytes sent] [duration] [platform prefix] [equipment id]`

#### Example Log Entries

```
[::ffff:10.5.105.197]:59234 - "(demo2)@(CT)" "31/Jul/2025:14:41:23.073 +0530" 1.2 tunnel 172.24.35.34 -1 112639 137450 165 W"42 1a 69 3a 6c 75 ac eb-be 8a 0b 90 9b 13 c6 24"
172.24.35.34:59260 - "(demo2)@(CT)" "31/Jul/2025:14:40:47.815 +0530" 1.2 flow:tcp 10.5.252.168:443 0 5436 129963 125 W"42 1a 69 3a 6c 75 ac eb-be 8a 0b 90 9b 13 c6 24"
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["network"] |
| event.type | ["connection"] |
| event.dataset | "sonicwall.sma.network_tunnel" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | date/time | Timestamp |
| client.bytes | bytes received | Client->server bytes |
| client.ip | client vip4, client vip6 | Tunnel-assigned VIP |
| client.user.domain | username @ realm | Realm extraction |
| client.user.name | username @ realm | Username extraction |
| destination.ip | destination ip | Destination IP |
| destination.port | destination ip | Destination port extraction |
| event.duration | duration | Seconds -> ns |
| event.outcome | error code | Success/failure mapping |
| network.protocol | “flow:”protocol | Flow protocol extraction |
| process.name | platform prefix | Platform code |
| server.bytes | bytes sent | Server->client bytes |
| sonicwall.sma.equipment_id | equipment id | Device/session ID |
| sonicwall.sma.tunnel_version | tunnel protocol version | Custom version |
| source.ip | source ip | Source IP |
| source.port | source ip | Source port extraction |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.connection_type | “tunnel” | tunnel |
| sonicwall.sma.connection_type | “flow:”protocol | flow:tcp/udp/icmp... |

---

### 6. Web Proxy Audit Log

#### File

`/var/log/aventail/extraweb_access.log`  

#### Format

W3C Common Log Format (CLF)  

#### Log Format

`[Status] [date/time] [source ip] [bytes-sent] [username@realm] [identity] [request] [HTTP-return-code]`

#### Example Log Entry

```
192.168.2.69 - (jsmith)@(AD) [6/3/2025 00:32:36.115 +0000] "GET /workplace/access/home HTTP/1.1" 200 15424
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["network"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.web_proxy" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | date/time | RFC 3339 |
| client.user.domain | username@realm | Realm extraction |
| client.user.name | username@realm | Username extraction |
| http.request.method | request | Method extraction |
| http.response.bytes | bytes-sent | Body bytes |
| http.response.status_code | HTTP-return-code | Response code |
| http.version | request | HTTP version extraction |
| source.ip | source ip | Source client IP |
| url.path | request | URI path extraction |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.api_endpoint | request | API endpoint extraction |
| sonicwall.sma.http_status_class | HTTP-return-code | 2xx/3xx/4xx/5xx class |

---

### 7. Unregistered Device Log Messages

#### File

XML export (not line-based syslog)  

#### Format

HTTP endpoint exporting XML content  

#### Log Format

`https://<internal address>:8443/UnregisteredDevices.xml`  
`https://<internal address>:8443/UnregisteredDevices.xml?parameter=value&parameter=value`

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["iam"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.unregistered_device" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | lastLoginTime (URL parameter) | Relative period selector (`hour`, `day`, `week`, ...) |
| host.os.type | platform (URL parameter) | Enumerated platform filter |
| user.domain | realm (URL parameter) | Case-insensitive realm filter |
| user.name | username (URL parameter) | Case-insensitive username filter |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.export_state | exported (URL parameter) | Exported/unexported selector |
| sonicwall.sma.registered_device_count | deviceCount (URL parameter) | Registered device count filter |
| sonicwall.sma.unregistered_device.limit | limit (URL parameter) | Max entries to export |

---

### 8. WorkPlace Logs

#### File

`/var/log/aventail/workplace.log`

Related files:
- `/var/log/aventail/wp_init.log`
- `/var/log/aventail/extraweb_access.log`

#### Format

WorkPlace troubleshooting logs (syslog-style prefixes)  

#### Log Format

`[DATESTAMP] [SERVICE@HOSTNAME] [local7.LEVEL] [WP:] [MESSAGE]`  
`[DATESTAMP] [CLIENT_IP/PROXY_IP] [local7.LEVEL] [LEVEL] [MESSAGE]`

#### Example Log Entries

```
2025-06-30T14:17:23+05:30 WP@ma34.sma local7.debug WP: 2025-06-30 14:17:24 +0530 DEBUG - GOT: CredentialsManager[teamSessionId=/bV+kF/p7QuQWL3BGdokQA==,teamcredentials={username=udbhav} ,credentials={}]
2025-06-30T14:17:23+05:30 WP@ma34.sma local7.debug WP: 2025-06-30 14:17:23 +0530 DEBUG - PolicyClientSession: <authorize:exit> uri=http://127.0.0.1:8085/ctdownload/ status=PCL_STATUS_SUCCESa
2025-06-30T14:17:23+05:30 127.0.0.1/127.0.0.1 local7.debug DEBUG [22:03:03,617] pcsession: <authorize:exit> uri=smb://marshare01/marketing status=SUCCESS
2025-06-30T14:17:23+05:30 127.0.0.1/127.0.0.1 local7.debug DEBUG [22:12:15,043] pcsession: <authorize:exit> uri=http://wemmet.internal.net status=FAILURE
```

#### Fields

##### Static Fields

| Field | Value |
| --- | --- |
| event.category | ["network", "authentication"] |
| event.type | ["info"] |
| event.dataset | "sonicwall.sma.workplace" |

##### Dynamic Fields

| ECS Field | Log Element | Comment |
| --- | --- | --- |
| @timestamp | DATESTAMP | Start timestamp |
| event.action | MESSAGE | `<authorize:exit>` extraction |
| event.outcome | MESSAGE | SUCCESS/FAILURE mapping |
| event.provider | WP: | Provider marker |
| log.level | local7.LEVEL | Log level extraction |
| message | MESSAGE | Full message text |
| observer.hostname | SERVICE@HOSTNAME | Hostname when service-prefix format is used |
| service.name | SERVICE@HOSTNAME | Service name (`WP`) |
| source.ip | CLIENT_IP/PROXY_IP | Source/proxy IP in alternate prefix format |
| url.original | MESSAGE | `uri=...` extraction |
| user.name | MESSAGE | `username=...` extraction |

##### Custom Fields

| Custom Field | Log Element | Comment |
| --- | --- | --- |
| sonicwall.sma.workplace.policy_status | MESSAGE | `PCL_STATUS_*` raw value |
| sonicwall.sma.workplace.shortcut_type | MESSAGE | URI-scheme derived type (`web`/`network`) |
| sonicwall.sma.workplace.team_session_id | MESSAGE | `teamSessionId` extraction |

---

## Notes

### Event Severity Mapping (SonicWall → ECS)

| SonicWall Level | ECS Severity | Description |
| --- | --- | --- |
| Error | 3 | System error, shutdown |
| Warning | 4 | Unexpected event, minor impact |
| Info | 6 | Normal event, informational |
| Verbose | 7 | Detailed information |
| Internal | 0 | Internal use only |

### Event Outcome Mapping

| Scenario | ECS Value |
| --- | --- |
| HTTP 2xx, 3xx | success |
| HTTP 4xx, 5xx | failure |
| Tunnel/Flow error code -1 | success |
| Tunnel/Flow error code > 0 | failure |
| WorkPlace status SUCCESS | success |
| WorkPlace status FAILURE | failure |
| Auth success | success |
| Auth failure | failure |

### Time Conversion

- All timestamps should be converted to RFC 3339 format for `@timestamp`
- Duration fields (in seconds) should be converted to nanoseconds for `event.duration`
  - Formula: `seconds * 1_000_000_000`
  - Example: 165 seconds = 165000000000 nanoseconds

# Authors

- [Clement Burtscher](https://github.com/clement-burtscher-sekoia)
