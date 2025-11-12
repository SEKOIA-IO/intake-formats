## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Check the relevant option(s) -->

- [ ] New intake format
- [ ] Update to existing intake format
- [ ] Bug fix
- [ ] Documentation update
- [ ] Other (please describe):

## Affected Intake Formats

<!-- List the vendor/product formats affected by this PR -->

- Vendor/product:

## Checklist

<!-- Ensure all requirements are met before submitting -->

### 🔒 CRITICAL - Security Requirements (MUST BE VERIFIED FIRST)

- [ ] **No real email addresses** in test files (use: user@example.com, test@example.org)
- [ ] **No real passwords or API keys** (use: "P@ssw0rd!", "xxxxxxxxxxxx", "FAKE_TOKEN_123")
- [ ] **No real IP addresses** (use TEST-NET ranges: 192.0.2.x, 198.51.100.x, 203.0.113.x)
- [ ] **No real phone numbers** (use: +1-555-0100 or similar test numbers)
- [ ] **No real names or PII** (use: "John Doe", "Jane Smith", "User123")
- [ ] **No real company/organization names** in test data (unless public vendors)
- [ ] **No real usernames, hostnames, or domain names** (use: user1, host.example.com, test.corp)
- [ ] All test data has been anonymized and verified

### Required for All PRs

- [ ] Code has been linted
    - [ ] with the linter for manifest, smart-descriptions, and test files (`poetry run python linter.py check --changes` in utils/)
    - [ ] with Prettier for the parser code files (`npx prettier --write <module>/<format>/ingest/parser.yml`)
- [ ] All CI/CD checks pass
- [ ] Changes follow the contribution guidelines in `CONTRIBUTING.md`

### Required for New/Updated Intake Formats

- [ ] Clear descriptions provided for modules and formats
- [ ] Logo files included for new modules/formats
- [ ] Parser test coverage is at least 75%
- [ ] At least one smart-description is provided
- [ ] README.md updated (if applicable)
- [ ] Taxonomy mappings are correct and documented
- [ ] Test cases cover edge cases and error handling

### Testing

- [ ] Local tests pass (`poetry run pytest` in utils/)
- [ ] Sample data is representative and **completely anonymized**
- [ ] **No sensitive information** (PII, credentials, real IPs, real emails) in test files
- [ ] Test data uses example.com/example.org domains and TEST-NET IP ranges
- [ ] Parser handles malformed data gracefully

### Documentation

- [ ] Code changes are documented
- [ ] Smart-descriptions are clear and informative
- [ ] Field mappings are explained

## Additional Notes

<!-- Add any additional context, screenshots, or information that would help reviewers -->

## Related Issues

<!-- Link any related issues using #issue_number -->

Closes #
