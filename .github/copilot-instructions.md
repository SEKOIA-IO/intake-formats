# GitHub Copilot Custom Instructions for intake-formats

## Repository Context

This repository contains intake formats for Sekoia.io security data ingestion. It includes parsers, taxonomies, and configurations for various security vendors and products.

## Pull Request Review Checklist

When reviewing a pull request, please check and comment on the following:

### 1. Code Quality & Structure
- Verify that new intake formats follow the existing directory structure: `Vendor/vendor-product/`
- Check that `_meta` directories contain required metadata files
- Ensure proper YAML formatting and indentation
- Validate that parser files have appropriate naming conventions

### 2. Documentation Requirements
- **Module README**: Verify that new modules have a `README.md` in the vendor directory
- **Format Description**: Check that formats have clear descriptions in their metadata
- **Taxonomy Mapping**: Ensure taxonomy fields are properly documented
- **Logo Files**: Confirm that new modules and formats include logo files (PNG/SVG)

### 3. Testing Requirements
- **Test Files**: Check for presence of test files in the intake directory
- **Sample Data**: Ensure test files include representative sample data
- **Edge Cases**: Look for tests covering edge cases and error handling

### 4. Parser Quality
- **Field Extraction**: Verify that important security fields are extracted (timestamps, IPs, users, actions)
- **Taxonomy Compliance**: Check that fields map correctly to Sekoia.io taxonomy
- **Error Handling**: Ensure parsers handle malformed data gracefully
- **Performance**: Look for potential performance issues in regex patterns or loops

### 5. Smart Descriptions
- **Presence**: Confirm at least one smart-description is provided for new formats
- **Quality**: Verify smart-descriptions are clear and informative
- **Variables**: Check that smart-descriptions use appropriate variables from parsed data

### 6. Contribution Guidelines
- **Linting**: Verify the parser is formatted with Prettier
- **Linting**: Verify smart-descriptions, test files, manifest are formatted with `utils/linter.py`, with the command line `poetry run python linter.py check --changes` and the working directory as `utils/`
- **Dependencies**: Check that new dependencies are properly documented
- **Breaking Changes**: Flag any changes that might break existing integrations

## Automated Actions on PR Creation

When a new pull request is created, please:

1. **Analyze Changed Files**
   - Identify which intake formats are modified or added
   - List the vendor/product combinations affected
   - Check if changes are in existing formats or new additions

2. **Run Initial Validation**
   - Verify YAML syntax in changed files
   - Check for required files (README, logos, metadata)
   - Identify missing documentation

3. **Comment with Checklist**
   - Post a comment with the contribution checklist
   - Highlight any missing required elements
   - Provide helpful suggestions for improvements

4. **SECURITY SCAN - Check for Sensitive Information (CRITICAL)**
   - **Scan all test files** for real PII (names, emails, phones, addresses)
   - **Check for credentials** (passwords, API keys, tokens, certificates)
   - **Verify IP anonymization** (use TEST-NET ranges: 192.0.2.x, 198.51.100.x, 203.0.113.x)
   - **Validate email domains** (should use example.com, example.org, test.com)
   - **Flag real organizational data** (company names, internal hostnames, real usernames)
   - **If ANY sensitive data is found**: Request changes immediately and provide anonymized alternatives

5. **Flag Other Potential Issues**
   - Incomplete test coverage
   - Missing logos or documentation
   - Non-standard directory structure
   - Formatting issues (suggest running Prettier)

6. **Suggest Improvements**
   - Recommend additional test cases
   - Suggest better field mappings
   - Propose documentation enhancements

## Code Review Focus Areas

### For New Intake Formats
- Directory structure follows: `Vendor/README.md`, `Vendor/_meta/`, `Vendor/vendor-product/`
- All required files present: parser, tests, metadata, logos
- Smart-descriptions provide meaningful event summaries

### For Parser Updates
- Changes maintain backward compatibility
- New fields are properly documented
- Tests updated to cover new functionality
- Taxonomy mappings remain consistent

### For Documentation Changes
- Technical accuracy of content
- Clarity and completeness
- Proper formatting and links
- Examples are correct and tested

## Common Issues to Flag

1. **Missing Required Files**
   - No logo files for new vendors/products
   - Missing README.md files
   - Absent or incomplete metadata

2. **SECURITY: Sensitive Information in Tests (CRITICAL)**
   - Real email addresses in test data
   - Real passwords, API keys, or tokens
   - Real names or personal information
   - Real IP addresses (not from TEST-NET ranges)
   - Real company/organization identifiers
   - Any PII that could identify real individuals

3. **Testing Issues**
   - No test files for new parsers
   - Tests don't cover error cases

4. **Formatting Problems**
   - Not linted with Prettier or the linter script
   - Inconsistent YAML indentation
   - Mixed line endings

5. **Documentation Gaps**
   - Unclear or missing descriptions
   - No smart-descriptions for new formats
   - Incomplete taxonomy documentation

## Helpful Responses

When reviewing PRs, be constructive and provide:
- Specific line references for issues
- Examples of correct implementation
- Links to relevant documentation
- Suggestions, not just criticisms
- Recognition of good practices

## Security Considerations - CRITICAL

### Sensitive Information in Tests (TOP PRIORITY)

**This is a public repository. ALL test data MUST be anonymized.**

When reviewing test files (especially in `tests/`, `test_*.py`, `test_*.json`, `test_*.txt`), ALWAYS check for:

1. **Personal Identifiable Information (PII)**:
   - Real names (replace with: "John Doe", "Jane Smith", "User123")
   - Real email addresses (replace with: "user@example.com", "test@example.org")
   - Real phone numbers (replace with: "+1-555-0100", "+33-1-23-45-67-89")
   - Real physical addresses (replace with: "123 Main St, Anytown, USA")
   - Social security numbers, tax IDs, or national ID numbers
   - Date of birth, age, or other personal identifiers
   - Real IP addresses from private networks (use: 192.0.2.x, 198.51.100.x, 203.0.113.x)

2. **Authentication Credentials**:
   - Passwords (use: "P@ssw0rd!", "SecurePass123")
   - API keys or tokens (use: "xxxxxxxxxxxx", "REDACTED", or fake keys like "sk_test_123abc")
   - OAuth tokens or refresh tokens
   - Session IDs or cookies
   - SSH keys or certificates
   - Database connection strings with credentials

3. **Organization-Specific Information**:
   - Real company names (unless they're public vendors)
   - Internal hostnames or domain names (use: "example.com", "internal.corp")
   - Real usernames (use: "user1", "admin", "testuser")
   - Real server names or internal URLs
   - Real database names or table schemas
   - Internal network configurations

4. **Security Tokens & Hashes**:
   - Real JWT tokens (generate fake ones or use obvious placeholders)
   - Real hashes of passwords or data
   - Real encryption keys
   - Real certificate serial numbers

### How to Flag Sensitive Information

When you detect potential sensitive information:

1. **IMMEDIATELY flag it** with a clear comment
2. **Specify the exact line number** and file
3. **Explain why it's sensitive** (e.g., "This looks like a real email address")
4. **Suggest an anonymized replacement**
5. **Mark the PR as requiring changes** before merge

### Example Comments for Sensitive Data

```
⚠️ SECURITY ISSUE: Line 45 in tests/test_parser.py contains what appears to be a real email address: "john.smith@company.com"

Recommendation: Replace with anonymized email like "user@example.com" or "test.user@example.org"
```

```
🚨 CRITICAL: Lines 78-82 contain what looks like a real API key. This must be replaced with a dummy key like "xxxxxxxxxxxx" or "test_api_key_123456789" before merging.
```

### Anonymization Best Practices to Verify

- Email domains should use: `example.com`, `example.org`, `test.com`
- IP addresses should use TEST-NET ranges: 192.0.2.x, 198.51.100.x, 203.0.113.x
- Usernames should be generic: "user1", "testuser", "admin"
- Passwords should be obvious fakes: "password123", "P@ssw0rd!"
- Tokens should be clearly fake: "xxxxxxxxxxxx", "FAKE_TOKEN_123"
- Hostnames should use: "host.example.com", "server.test"

### Other Security Considerations

- Check that parsers properly sanitize inputs
- Ensure no hardcoded secrets in configuration files
- Flag any suspicious regex patterns that might cause ReDoS
- Verify that logging doesn't expose sensitive data

## Performance Guidelines

- Watch for inefficient regex patterns
- Flag nested loops or recursive operations
- Suggest optimization opportunities
- Consider memory usage for large log processing

## Integration with CI/CD

This repository has automated workflows:
- `build-intakes.yml`: Builds and deploys intakes on merge
- `test.yml`: Runs tests on PRs
- `test_linting.yml`: Checks code formatting
- `smart_desc.yml`: Validates smart descriptions

When reviewing, consider:
- Will this pass CI/CD checks?
- Are there workflow-specific requirements?
- Should any workflow configurations be updated?
