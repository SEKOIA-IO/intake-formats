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
- `known_services.log`: map the service to `network.protocol` and the pair it answers on to `destination.ip` / `destination.port`, with the application and the software banner observed.
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

### Changed

- `known_users.log`: the counters and annotations move from `corelight.known_users.*` to `corelight.known.*`, the namespace now shared by the whole `known_*` family.

- `notice.log`: keep the raw event in the top-level `message` field; the notice text is now exposed as `corelight.notice.message`.
- `suricata_corelight`: also map `alert.action` to `event.action` (in addition to `action.name`).
- `conn.log`: `source.user.roles` is now emitted as an array; `event.duration` is now emitted as an integer (nanoseconds).
- Detection rules now reference the relevant Zeek/Suricata documentation instead of a generic integration link.

## 2026-06-17 - 1.0.0

### Added

- Initial Corelight Open NDR intake format.
- Parsing of Zeek/Corelight logs: `conn`, `dns`, `http`, `ssl`, `files`, `notice` and the Zeek Intelligence Framework (`intel`).
- Parsing of Suricata IDS alerts (`suricata_corelight`).
- Mapping of Corelight entity enrichment (`enrichment_orig.user`, `enrichment_orig.role`, `enrichment_orig.city_location`) to ECS.
