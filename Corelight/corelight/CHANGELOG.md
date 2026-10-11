# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Support for the authentication and lateral movement logs the sensor already sends: `ssh.log`, `kerberos.log`, `ntlm.log`, `ldap.log`, `ldap_search.log` and `dce_rpc.log`. They were received but left unparsed, so only the envelope (timestamps, addresses, `event.dataset`) reached the events.
- `ssh.log`: map the client and server version strings, the negotiated algorithms, the HASSH fingerprints and the host key, plus `network.direction` and `event.outcome` from `auth_success`.
- `kerberos.log`: split the `client` principal into `source.user.name` and `source.user.domain`, and map the request type, the requested service, the ticket flags and the KDC error.
- `ntlm.log`: map the account to `source.user.name` / `source.user.domain`, the client and server names to `source.domain` / `destination.domain`, and `event.outcome` from `success`.
- `ldap.log` and `ldap_search.log`: map the operation, its result, the search base, scope and filter. Only a bind is reported under the `authentication` event category; the other operations stay directory operations.
- `dce_rpc.log`: map the endpoint, the operation and the named pipe, which is how SMB-carried RPC abuse (`samr`, `svcctl`, `drsuapi`) becomes visible.
- Support for the mail, file transfer and file metadata logs: `smtp.log`, `smtp_links.log`, `smb_files.log`, `smb_mapping.log`, `ftp.log`, `x509.log` and `pe.log`.
- `smtp.log`: map the `From:` and `To:` headers to `email.from.address` and `email.to.address`, the envelope `MAIL FROM` to `email.sender.address`, the subject, and the STARTTLS state to `tls.established`. ECS defines no field for the envelope recipients, so they stay under `corelight.smtp.rcptto`. The `Date:` header is emitted verbatim in its RFC 5322 form rather than coerced onto a date field.
- `smtp_links.log`: map each URL found in a message body to `url.original`, which lets the platform derive the whole `url.*` set.
- `smb_files.log`: map the share to `file.directory`, the four Zeek timestamps to `file.mtime` / `file.accessed` / `file.created` / `file.ctime`, and derive `event.action` and `event.type` from the SMB action, so a write is reported as a `change` and a delete as a `deletion`.
- `smb_mapping.log`: map the mapped share, its service, its file system and its type.
- `ftp.log`: map the command to `event.action`, the account to `source.user.name`, the data channel, and `event.outcome` from the reply code. The password Zeek also logs is deliberately left unmapped.
- `x509.log`: map the certificate onto the ECS `x509.*` fields and the fingerprint to `file.hash.sha256`. This log carries no connection tuple; it joins `ssl.log` through the fingerprint.
- `pe.log`: map the target architecture, the compilation timestamp, the section names and the hardening flags (ASLR, DEP, SEH, code integrity). Zeek exposes none of the fields ECS defines under `file.pe`, so they stay namespaced.
- Support for the remaining protocol and observation logs the sensor sends: `dhcp.log`, `rdp.log`, `quic.log`, `ntp.log`, `snmp.log`, `mysql.log`, `tunnel.log`, `ipsec.log`, `ocsp.log`, `encrypted_dns.log`, `software.log`, `known_users.log` and `weird.log`.
- `dhcp.log`: map the lease exchange to `source.ip` / `destination.ip`, the client hardware address to `source.mac` and its name to `host.hostname`, plus the assigned and requested addresses and the lease duration. The domain name option offered in the lease is not mapped onto `source.domain`: it describes the lease, not the client.
- `rdp.log`: map the negotiated security protocol, the connection result and the cookie (which usually carries the account being used), and derive `event.outcome` from `auth_success`.
- `quic.log`: map the SNI to `tls.client.server_name`, the negotiated application protocol and the connection identifiers.
- `ntp.log`: map the association mode, the stratum, the reference clock and the four protocol timestamps.
- `snmp.log`: map the community string, the `sysDescr` returned by the agent and the per-operation counters, which is how SNMP writes (`set_requests`) become visible.
- `mysql.log`: map the command to `event.action`, the statement, the row count and `event.outcome`.
- `tunnel.log`: map the encapsulation and what Zeek observed about the tunnel.
- `ipsec.log`: map the IKE exchange, the security parameter indexes, the proposed transforms and the vendor identification payloads.
- `ocsp.log`: map the revocation status returned for a certificate and the issuer hashes. Like `x509.log`, this log carries no connection tuple.
- `encrypted_dns.log`: report DNS resolution hidden inside TLS (DoH, DoT) under the `intrusion_detection` event category, and map the resolver to `tls.client.server_name`.
- `software.log`: map the detected software to `package.name` and keep the version components as Zeek reports them, rather than recomposing a version string.
- `known_users.log`: map the observed account to `user.name`, the host it was seen on to `host.ip` and the protocol it was seen over to `network.protocol`.
- `weird.log`: map the protocol anomaly to `event.action`, with the Zeek worker that reported it and the additional context.
- Support for the industrial control logs `modbus.log`, `dnp3.log` and `s7comm.log`, and for the entity inventory logs `known_hosts.log`, `known_services.log` and `known_certs.log`.
- `modbus.log`: map the function to `event.action`, the exception returned by the device, and the register Corelight tracks together with its value before and after a write. The function is read from either `func` or `function`, since sensors differ on the name.
- `dnp3.log`: map the request and reply function codes and the internal indications the outstation returned.
- `s7comm.log`: map the message class, the function and subfunction, the PDU reference that pairs a request with its reply, and the error the PLC returned.
- `known_hosts.log`: map the observed host to `host.ip`, the role Corelight inferred for it, the connection counters, and the criticality, description, source and status the entity inventory holds for it.
- `known_services.log`: map the pair the service answers on to `destination.ip` / `destination.port`, the first application protocol recognised on it to `network.protocol`, and the application and the software banner observed.
- `known_certs.log`: map the certificate fingerprint to `file.hash.sha1` and the issuer and serial onto `x509.*`.
- Smart descriptions for `x509`, `rdp`, `dhcp`, `encrypted_dns`, `known_users`, `weird`, `modbus`, `dnp3`, `s7comm`, `known_hosts`, `known_services` and `known_certs`.

- `ssh.log`: map the HASSH inputs (`hasshAlgorithms`, `hasshServerAlgorithms`, `hasshVersion`), the host key algorithms each side offers, the behavioural inferences, and the geolocation of the remote endpoint onto `source.geo.*` or `destination.geo.*` depending on the direction of the session.
- `dce_rpc.log`: map the round-trip time of the call.
- `smtp.log`: map the `Cc:`, `Reply-To:` and `Message-ID:` headers and the mail user agent, plus the `In-Reply-To:`, `X-Originating-IP:` and the first two `Received:` headers.
- `ftp.log`: map the size and the MIME type of the transferred file, and the directory the session is in.
- `quic.log`: map the user agent the client advertised.
- `kerberos.log`: map the numeric KDC error code, the start of the requested validity window, the hashes of the presented and issued tickets, and the PKINIT certificate subjects.
- `ldap_search.log`: map the requested attributes and the diagnostic message the directory returned.
- `smb_files.log`: map the previous name of a renamed file.
- `dhcp.log`: map the relay agent options (circuit ID, remote ID, subscriber ID), the address the message was relayed from, and the software both ends identify themselves with.
- `rdp.log`: map the Corelight RDP fingerprint (RDFP), the requested colour depth, the client product identifier and the TLS state.
- `x509.log`: map the email, address and URI subject alternative names, and the path length constraint.

- Support for the fifteen remaining log types the sensor sends: `conn_long.log`, `known_domains.log`, `known_names.log`, `known_devices.log`, `modbus_detailed.log`, `modbus_read_device_identification.log`, `cotp.log`, `s7comm_read_szl.log`, `dnp3_objects.log`, `dnp3_control.log`, `enip.log`, `etc_viz.log`, `analyzer.log`, `unknown_protocols.log` and `generic_dns_tunnels.log`. Every log type a Corelight sensor exports is now parsed.
- `conn_long.log`: the periodic report the sensor writes for a connection that is still open. It shares the schema of `conn.log` and is parsed by the same stage, so a long-lived session is described the same way whether it is reported while open or once closed.
- `known_domains.log`, `known_names.log` and `known_devices.log`: map the entity inventory entries for a domain, a host name and a device, under the `corelight.known.*` namespace the whole `known_*` family shares. The name goes to `host.hostname` and the device hardware address to `host.mac`.
- `modbus_detailed.log`: map the function, the register or coil the request addresses, the quantity of values it covers and the values themselves, which is what makes a write to a specific register visible rather than just "a Modbus write happened".
- `modbus_read_device_identification.log`: map the MEI type, the conformity level and the vendor, product and revision strings the device returns.
- `cotp.log`: map the ISO 8073 PDU carried under TPKT, which is the transport S7comm rides on.
- `s7comm_read_szl.log`: map the system status list being read from the PLC, the method and the return code, plus `event.outcome`.
- `dnp3_objects.log`: map the object group, variation and range of a DNP3 request or reply, one level below the function code `dnp3.log` reports.
- `dnp3_control.log`: map the control relay output block: the operation type, the trip control code, the point index and the status the outstation returned, plus `event.outcome`. This is the log that shows an operator (or an attacker) actuating a point.
- `enip.log`: map the EtherNet/IP command, its status, the session handle and the sender context, plus `event.outcome`.
- `etc_viz.log`: map the encrypted traffic collection statistics Corelight derives for a session. The log carries only the server side of the pair, so only `destination.*` is populated.
- `analyzer.log`: report the protocol, file and packet analyzers that gave up on a session, with the reason and `event.outcome` set to `failure`. An analyzer failing is how parsing gaps and evasion attempts surface.
- `unknown_protocols.log`: map the analyzer that met traffic it could not identify, the protocol identifier and the first bytes it saw. This log carries no connection tuple at all.
- `generic_dns_tunnels.log`: report the domains Corelight suspects of carrying a DNS tunnel under the `intrusion_detection` event category, with the queried domain, the volume observed and the observation window.
- Smart descriptions for every dataset that had none: the fifteen log types above, and the twenty authentication, mail, file and protocol logs added earlier in this release (`ssh`, `kerberos`, `ntlm`, `ldap`, `ldap_search`, `dce_rpc`, `smtp`, `smtp_links`, `smb_files`, `smb_mapping`, `ftp`, `pe`, `ocsp`, `quic`, `ntp`, `snmp`, `mysql`, `tunnel`, `ipsec` and `software`).

- `observer.hostname`: the name the sensor reports for itself is now mapped there as well as to `observer.name`, on every log type.
- `dns.log`: map the transport the query travelled over to `network.transport`, and derive `event.outcome` from the response code the resolver returned.
- `ssl.log`: map the SNI to `destination.domain` as well as `tls.client.server_name`, the client certificate subject and issuer to `tls.client.subject` / `tls.client.issuer`, and derive `event.outcome` from the chain validation.
- `http.log`: map the `Host:` header to `destination.domain` as well as `url.domain`, and the MIME type of each direction to `http.request.mime_type` / `http.response.mime_type`.
- `files.log`: map the analyzer that carried the file (`HTTP`, `SMTP`, `FTP_DATA`, …) to `network.protocol`.
- `known_domains.log`: map the observed domain to `destination.domain`.
- `known_domains.log`, `known_names.log` and `known_devices.log`: map the first application protocol the entity was seen using to `network.protocol`; the whole set stays under `corelight.known.protocols`.
- `software.log`: map the address the software was observed on to `host.ip`.
- `ssh.log`, `smb_files.log`, `smb_mapping.log`, `ntlm.log`: set `network.transport`, which these logs do not carry but their protocol mandates.

### Changed

- `known_users.log`: the counters and annotations move from `corelight.known_users.*` to `corelight.known.*`, the namespace now shared by the whole `known_*` family.

- `notice.log`: keep the raw event in the top-level `message` field; the notice text is now exposed as `corelight.notice.message`.
- `suricata_corelight`: also map `alert.action` to `event.action` (in addition to `action.name`).
- `conn.log`: `source.user.roles` is now emitted as an array; `event.duration` is now emitted as an integer (nanoseconds).
- Detection rules now reference the relevant Zeek/Suricata documentation instead of a generic integration link.
- `conn.log` and `ssh.log`: the latitude and longitude of the Corelight geolocation enrichment are no longer mapped to `source.geo.location` / `destination.geo.location`. The sensor serialises those two doubles with their bytes in reverse order, so the exported values are meaningless (a latitude of 37.751 arrives as -1.04e+172). The city, region, country and ASN of the same enrichment are unaffected and still mapped.
- Events wrapped in a one-element JSON array are now parsed like the others. Part of the exports send `[{...}]` rather than `{...}`; the whole pipeline failed on those, since every stage reads the event as an object.
- `known_services.log`: the application protocol is now really emitted as `network.protocol`. Its guard ended on the `service` list itself, which the engine does not read as a condition, so the assignment never ran.
- `files.log`: the `tx_hosts` / `rx_hosts` fallback used when the log carries no connection tuple now really runs, for the same reason.
- `_meta/fields.yml`: fifty-two fields declared as `keyword` are now declared with the type the sensor actually sends — `boolean` for the flags (`conn.local_orig`, `dns.rejected`, `files.timedout`, `ssl.sni_matches_cert`, …), `long` for the counters and identifiers, `float` for the fractions. They were reported as strings before, which prevented range queries and aggregations on them.
- `_meta/fields.yml`: every field now carries a description.
- `conn.log`: a connection that carries no payload now reports its volume. `orig_bytes` / `resp_bytes` count payload only and Zeek omits them entirely on a SYN with no reply, a reject or an ICMP exchange, so `source.bytes` / `destination.bytes` now fall back to `orig_ip_bytes` / `resp_ip_bytes`, which count every byte seen on the wire and are always present. Those two counters also stay available as `corelight.conn.orig_ip_bytes` / `corelight.conn.resp_ip_bytes`.
- `ssl.log`: the certificate subject and issuer move from `x509.subject.distinguished_name` / `x509.issuer.distinguished_name` to `tls.server.subject` / `tls.server.issuer`. The certificate presented in a session belongs to the server, and that is where ECS holds it; `x509.log` keeps reporting its own certificates under `x509.*`.

## 2026-06-17 - 1.0.0

### Added

- Initial Corelight Open NDR intake format.
- Parsing of Zeek/Corelight logs: `conn`, `dns`, `http`, `ssl`, `files`, `notice` and the Zeek Intelligence Framework (`intel`).
- Parsing of Suricata IDS alerts (`suricata_corelight`).
- Mapping of Corelight entity enrichment (`enrichment_orig.user`, `enrichment_orig.role`, `enrichment_orig.city_location`) to ECS.
