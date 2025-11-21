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
**Project-specific example domains** (not RFC standards, for anonymization only): `mycorp.com`, `mycorp.org`, `mycorp.net`, `localhost`, `hostname`, `test.com`, `test.org`, `test.net`

### 2. IP Addresses ✅

#### ❌ DO NOT USE:
- Real public IP addresses (e.g., 203.0.113.5 if it's real)
- Real internal IP addresses from actual networks

#### ✅ USE INSTEAD (TEST-NET Ranges):
- **192.0.2.0/24** → 192.0.2.1, 192.0.2.100, 192.0.2.254
- **198.51.100.0/24** → 198.51.100.1, 198.51.100.50
- **203.0.113.0/24** → 203.0.113.1, 203.0.113.200

**Also acceptable**:
- 10.0.0.x (private range)
- 172.16.0.x to 172.31.0.x (private range)
- 192.168.0.x (private range)
- 127.0.0.1 (localhost)
- 1.2.3.4, 5.6.7.8, 3.4.5.6, 4.3.2.1, 8.7.6.5 (obviously fake)

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

## How to Anonymize Existing Data

### Method 1: Find and Replace

1. Export your test data
2. Use find/replace in your editor:
   - Find: `@yourdomain\.com` → Replace with: `@example.com`
   - Find real IPs → Replace with TEST-NET ranges
   - Find real names → Replace with John Doe, Jane Smith

### Method 2: Use Anonymization Scripts

```python
import re

def anonymize_email(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                  'user@example.com', text)

def anonymize_ip(text):
    return re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', 
                  '192.0.2.1', text)
```

### Method 3: Ask Copilot

```
@copilot please anonymize all sensitive data in this test file:
- Replace emails with user@example.com pattern
- Replace IPs with TEST-NET ranges
- Replace real names with John Doe, Jane Smith
- Replace any credentials with fake values
```

## Automated Checks

Our CI/CD workflow automatically scans for:
- Email patterns not using test domains
- IP addresses outside TEST-NET ranges
- Potential API keys and tokens
- JWT token patterns
- Phone number patterns

**If the scan detects issues, your PR will be flagged and must be corrected before merge.**

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
- [ ] All IP addresses use TEST-NET ranges or private ranges
- [ ] All passwords and API keys are obvious fakes
- [ ] All personal names are generic test names
- [ ] All phone numbers use test ranges (555-xxxx)
- [ ] All usernames are generic (user1, testuser, admin)
- [ ] All company names are generic or anonymized
- [ ] All domain names use example.com or similar
- [ ] No JWT tokens, hashes, or session IDs from real systems
- [ ] Reviewed entire file for any missed sensitive data

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
