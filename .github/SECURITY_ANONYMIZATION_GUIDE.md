# Security Anonymization Guide for Test Data

## 🚨 CRITICAL: This is a Public Repository

All test data, sample logs, and example files **MUST be completely anonymized** before being committed. Real personal information, credentials, or organizational data can **NEVER** be included.

## Why This Matters

- **Legal compliance**: GDPR, CCPA, and other privacy regulations
- **Security**: Prevents credential leaks and unauthorized access
- **Professional responsibility**: Protects individuals and organizations
- **Public exposure**: Anyone can view this repository's history forever

## What to Anonymize

### 1. Email Addresses ✅

#### ❌ DO NOT USE:
- john.smith@company.com
- real.person@organization.net
- any@actual-domain.com

#### ✅ USE INSTEAD:
- user@example.com
- test.user@example.org
- john.doe@test.com
- admin@localhost

**Standard test domains (RFC 2606)**: `example.com`, `example.org`, `example.net`, `*.test`, `*.invalid`,  `*.example`
**Additional project test domains** (for anonymization examples): `mycorp.com`, `mycorp.org`, `mycorp.net`, `localhost`, `hostname`, `test.com`, `test.org`, `test.net`

### 2. IP Addresses ✅

#### ❌ DO NOT USE:
- Real public IP addresses assigned to real systems
- Real internal IP addresses from production or corporate networks
- Any IPv6 address copied from real infrastructure

#### ✅ USE INSTEAD (Documentation/Test Ranges):
- **192.0.2.0/24** → 192.0.2.1, 192.0.2.100, 192.0.2.254
- **198.51.100.0/24** → 198.51.100.1, 198.51.100.50
- **203.0.113.0/24** → 203.0.113.1, 203.0.113.200
- **2001:db8::/32** (IPv6 documentation range) → 2001:db8::1, 2001:db8:100::25

**Limited exceptions**:
- 127.0.0.1 and ::1 for localhost-only examples
- Explicitly fake placeholders like 1.2.3.4 when no routable semantics are needed

**Important**: Avoid 10.x, 172.16-31.x, and 192.168.x in public test data because they can match real internal addressing plans.

### 3. Passwords & API Keys ✅

#### ❌ DO NOT USE:
- Any real password (even if you think it's weak)
- Any real API key, token, or secret
- Any real OAuth tokens
- Any real certificate or SSH key

#### ✅ USE INSTEAD:
- `P@ssw0rd!`
- `SecurePass123`
- `password123`
- `xxxxxxxxxxxx`
- `FAKE_API_KEY_1234567890`
- `sk_test_123abc456def` (clearly fake)
- `REDACTED`
- `<ANONYMIZED>`

### 4. Phone Numbers ✅

#### ❌ DO NOT USE:
- Real phone numbers from any country

#### ✅ USE INSTEAD:
- `+1-555-0100` to `+1-555-0199` (US test range)
- `+33-1-23-45-67-89` (obviously fake format)
- `555-1234` (North American test prefix)

### 5. Personal Names ✅

#### ❌ DO NOT USE:
- Real first and last name combinations
- Real employee names
- Real customer names

#### ✅ USE INSTEAD:
- John Doe, Jane Doe
- John Smith, Jane Smith
- User1, User2, User123
- TestUser, AdminUser
- Alice, Bob, Charlie (classic test names)

### 6. Usernames ✅

#### ❌ DO NOT USE:
- Real employee usernames
- Real customer usernames
- Actual system account names

#### ✅ USE INSTEAD:
- user1, user2, testuser
- admin, administrator
- jdoe, jsmith
- test_account_001

### 7. Company/Organization Names ✅

#### ❌ DO NOT USE:
- Real customer company names
- Real internal team names
- Real department names

#### ✅ USE INSTEAD:
- Example Corp
- Test Company Inc.
- Acme Corporation
- Generic names like "Engineering Team", "Sales Dept"

**Exception**: Public vendor names (Microsoft, Google, AWS) are OK when referring to their products.

### 8. Domain Names & Hostnames ✅

#### ❌ DO NOT USE:
- Real internal domain names
- Real customer domains
- Actual server hostnames

#### ✅ USE INSTEAD:
- example.com, example.org
- test.corp, internal.test
- server1.example.com
- host-001.test.local

### 9. Database & File Paths ✅

#### ❌ DO NOT USE:
- Real database names with sensitive info
- Real file paths with usernames
- Real server paths

#### ✅ USE INSTEAD:
- /var/log/application/events.log
- C:\Logs\test_data.txt
- /home/testuser/documents/
- Database: test_db, sample_database

### 10. JWT Tokens & Hashes ✅

#### ❌ DO NOT USE:
- Real JWT tokens
- Real password hashes
- Real session IDs

#### ✅ USE INSTEAD:
- `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.FAKE_PAYLOAD.FAKE_SIGNATURE`
- `$2b$12$FAKE_HASH_1234567890abcdefghijklmnopqrstuvwxy`
- `<FAKE_SESSION_ID_123456>`

### 11. Device and Persistent Identifiers ✅

#### ❌ DO NOT USE:
- Real MAC addresses
- Real UUIDs or host IDs
- Real serial numbers or hardware fingerprints
- Real cloud account IDs, tenant IDs, subscription IDs, project IDs

#### ✅ USE INSTEAD:
- MAC: `02:00:00:aa:bb:cc` (locally administered/test style)
- UUID: `00000000-0000-4000-8000-000000000000`
- Tenant/account/project IDs: clearly fake placeholders like `tenant-000000-test`

## How to Anonymize Existing Data

### Method 1: Find and Replace

1. Export your test data
2. Use find/replace in your editor:
   - Find: `@yourdomain\.com` → Replace with: `@example.com`
    - Find real IPv4/IPv6 values → Replace with documentation ranges
   - Find real names → Replace with John Doe, Jane Smith
3. Keep referential consistency:
    - If one source user appears in multiple events, replace it with the same anonymized value everywhere.
    - If one host appears in multiple events, keep a stable replacement for that host.

### Method 2: Use Anonymization Scripts

```python
import hashlib
import ipaddress
import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
IPV6_RE = re.compile(r"\b(?:[0-9A-Fa-f]{1,4}:){2,}[0-9A-Fa-f]{1,4}\b")


class Anonymizer:
    def __init__(self):
        self.email_map = {}
        self.ip_map = {}

    @staticmethod
    def _stable_token(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()[:8]

    def anonymize_email(self, text):
        def repl(match):
            email = match.group(0)
            if email not in self.email_map:
                self.email_map[email] = f"user-{self._stable_token(email)}@example.com"
            return self.email_map[email]

        return EMAIL_RE.sub(repl, text)

    def anonymize_ip(self, text):
        def map_ipv4(ip_str):
            if ip_str not in self.ip_map:
                octet = int(self._stable_token(ip_str)[:2], 16)
                self.ip_map[ip_str] = f"192.0.2.{1 + (octet % 254)}"
            return self.ip_map[ip_str]

        def map_ipv6(ip_str):
            if ip_str not in self.ip_map:
                token = self._stable_token(ip_str)
                self.ip_map[ip_str] = f"2001:db8::{token[:4]}:{token[4:8]}"
            return self.ip_map[ip_str]

        def replace_ipv4(match):
            value = match.group(0)
            try:
                ipaddress.IPv4Address(value)
                return map_ipv4(value)
            except ipaddress.AddressValueError:
                return value

        def replace_ipv6(match):
            value = match.group(0)
            try:
                ipaddress.IPv6Address(value)
                return map_ipv6(value)
            except ipaddress.AddressValueError:
                return value

        text = IPV4_RE.sub(replace_ipv4, text)
        return IPV6_RE.sub(replace_ipv6, text)
```

This keeps the replacement mapping local to a specific anonymization pass, which is easier to reason about and makes it easier to reset or isolate state between files.

### Method 3: Ask Copilot

```
@copilot please anonymize all sensitive data in this test file:
- Replace emails with a stable one-to-one mapping (same source email => same anonymized email)
- Replace IPv4 and IPv6 addresses with documentation ranges
- Replace real names with John Doe, Jane Smith
- Replace any credentials with fake values
```

## Automated Checks

Our CI/CD workflow automatically scans for:
- Email patterns not using test domains
- IPv4 and IPv6 addresses outside approved documentation ranges
- Potential API keys and tokens
- JWT token patterns
- Phone number patterns
- MAC address patterns
- UUID and host identifier patterns
- Cloud tenant/account/project identifier patterns
- Common credential field names (`password`, `secret`, `token`, `api_key`) with suspicious values

**If the scan detects issues, your PR will be flagged and must be corrected before merge.**

**Note**: Automated scanning reduces risk but cannot guarantee perfect detection. Always perform manual review on nested, encoded, or binary-like payloads.

## Examples

### ❌ Bad Test Data

```json
{
  "user": "robert.johnson@acmecorp.com",
  "ip": "203.145.67.89",
  "password": "MySecureP@ss2024",
  "phone": "+1-415-555-1234",
  "api_key": "sk_live_REAL_KEY_REDACTED_XXXXXXXXXXXX"
}
```

### ✅ Good Test Data

```json
{
  "user": "user@example.com",
  "ip": "192.0.2.45",
  "password": "P@ssw0rd!",
  "phone": "+1-555-0123",
  "api_key": "sk_test_FAKE_KEY_XXXXXXXXXXXX"
}
```

### ❌ Bad Log Sample

```
2024-10-15 10:30:45 - Login from alice.williams@techstartup.io at 198.51.100.45
2024-10-15 10:31:12 - API call with token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFsaWNlIFdpbGxpYW1zIiwiaWF0IjoxNTE2MjM5MDIyfQ.REAL_SIGNATURE_HERE
```

### ✅ Good Log Sample

```
2024-10-15 10:30:45 - Login from user@example.com at 192.0.2.45
2024-10-15 10:31:12 - API call with token: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.FAKE_PAYLOAD.FAKE_SIGNATURE
```

## Checklist Before Committing

- [ ] All email addresses use test domains (example.com, example.org, test.com)
- [ ] All IPv4 addresses use TEST-NET/documentation ranges
- [ ] All IPv6 addresses use the documentation range (2001:db8::/32)
- [ ] All passwords and API keys are obvious fakes
- [ ] All personal names are generic test names
- [ ] All phone numbers use test ranges (555-xxxx)
- [ ] All usernames are generic (user1, testuser, admin)
- [ ] All company names are generic or anonymized
- [ ] All domain names use example.com or similar
- [ ] No JWT tokens, hashes, or session IDs from real systems
- [ ] No real MACs, UUIDs, tenant IDs, or account IDs
- [ ] Nested/encoded payloads were reviewed (JSON strings, URL params, base64 blocks)
- [ ] Reviewed entire file for any missed sensitive data

## If Non-Anonymized Data Was Already Committed

If non-anonymized data is discovered after commit:

1. Replace sensitive values with anonymized equivalents in the source test files.
2. If any credentials or secrets were exposed, revoke or rotate them immediately.
3. Rewrite Git history to remove previously committed sensitive values.
4. If the data was already pushed to a shared or default branch, follow the GitHub guidance for removing sensitive data from a repository.
5. Re-run anonymization checks to confirm the data is fully sanitized.
6. Add or improve detection rules so the same pattern is caught next time.

## Need Help?

Ask GitHub Copilot:
```
@copilot scan this file for sensitive information and help me anonymize it
```

Or consult with the security team if you're unsure whether something should be anonymized.

## References

- [RFC 5737 - TEST-NET IP Ranges](https://tools.ietf.org/html/rfc5737)
- [RFC 2606 - Reserved Domain Names](https://tools.ietf.org/html/rfc2606)
- [GDPR Guidelines](https://gdpr.eu/)
- [OWASP Data Anonymization](https://owasp.org/www-community/Anonymization)

---

**Remember**: When in doubt, anonymize. It's better to be overly cautious than to expose sensitive information in a public repository.
