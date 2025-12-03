# GitHub Copilot Integration for intake-formats

This directory contains configurations for GitHub Copilot to assist with pull request reviews and code contributions.

## Files

### `copilot-instructions.md`

Custom instructions that guide GitHub Copilot's behavior when:
- Reviewing pull requests
- Analyzing code changes
- Suggesting improvements
- Identifying potential issues

These instructions are automatically loaded by GitHub Copilot when interacting with this repository.

### `PULL_REQUEST_TEMPLATE.md`

A standardized template for pull requests that ensures contributors provide all necessary information. This template includes:
- Description of changes
- Type of change indicators
- Comprehensive checklist for code quality
- Testing requirements
- Documentation requirements

### Workflows

#### `copilot-pr-review.yml`

An automated workflow that triggers when a pull request is opened or updated. It:
1. **Analyzes changed files** - Identifies which intake formats are affected
2. **SCANS FOR SENSITIVE INFORMATION** - Detects real emails, passwords, API keys, IP addresses, and PII in test files
3. **Checks for required files** - Validates presence of README, tests, logos, etc.
4. **Posts a detailed comment** - Provides security scan results, analysis, and checklist to PR author
5. **Flags security issues** - Highlights any sensitive data that must be anonymized before merge
6. **Requests Copilot review** - Automatically assigns Copilot as a reviewer (if available)

## How to Use

### In local Development
1. **Set up GitHub Copilot**: Ensure you have GitHub Copilot enabled for your account and repository.
2. **Launch copilot**: Start using Copilot in your IDE (e.g., VSCode) to get suggestions as you code.
3. **Enter the following prompt** to get assistance based on the custom instructions:
   ```
   @workspace Please run the anonymization checks described in .github/copilot-instructions.md and run the scan on all modified modules
   ```
4. **Help the agent**: Provide context or specify which formats you want to focus on:
   ```
   @workspace Please focus on Vendor/product/parser.py and tests/test_parser.py
   ```
5. **Review suggestions**: Evaluate Copilot's recommendations and make necessary changes.

### For Contributors

1. **Create a Pull Request**: When you open a PR, the automation will:
   - **Scan for sensitive information** in all test files (CRITICAL)
   - Analyze your changes
   - Post a detailed comment with security findings, checklist, and suggestions
   - Request a Copilot review

2. **Review Security Scan Results**: 
   - Check the automated comment for any 🚨 CRITICAL or ⚠️ WARNING flags
   - **If sensitive data is detected**: You MUST anonymize it before the PR can be merged
   - The bot will suggest appropriate replacements (example.com, TEST-NET IPs, etc.)

3. **Interact with Copilot**: You can ask Copilot for help by commenting on your PR:
   ```
   @copilot scan this PR for any sensitive information I might have missed
   ```
   
   ```
   @copilot help me anonymize the test data in tests/test_parser.py
   ```
   
   ```
   @copilot please review the parser logic in Vendor/product/parser.py
   ```
   
   ```
   @copilot can you suggest additional test cases for this intake format?
   ```
   
   ```
   @copilot help me improve the smart-description for this format
   ```

4. **Use the PR Template**: Fill out the security checklist FIRST, then complete other quality standards

### For Reviewers

When reviewing a PR, you can:

1. **Ask Copilot for security review**:
   ```
   @copilot thoroughly scan all test files for sensitive information including emails, IPs, credentials, and PII
   ```
   
   ```
   @copilot verify that all test data is properly anonymized
   ```

2. **Ask Copilot for insights**:
   ```
   @copilot what are the security implications of these parser changes?
   ```
   
   ```
   @copilot check if the test coverage is adequate for this change
   ```

3. **Request specific analyses**:
   ```
   @copilot analyze the regex patterns for potential ReDoS vulnerabilities
   ```
   
   ```
   @copilot verify the taxonomy mappings are correct
   ```

### For Maintainers

The custom instructions help ensure consistent code reviews by:
- **Scanning for sensitive information in test files** (TOP PRIORITY)
- Checking for compliance with contribution guidelines
- Identifying missing documentation
- Validating test coverage
- Flagging security concerns (PII, credentials, ReDoS patterns)
- Suggesting performance improvements

## Customization

### Modifying Copilot Instructions

Edit `.github/copilot-instructions.md` to:
- Add new review criteria
- Update checklist items
- Modify automated actions
- Add repository-specific guidelines

### Updating the Workflow

Edit `.github/workflows/copilot-pr-review.yml` to:
- Change when the workflow triggers
- Add additional file checks
- Modify the comment format
- Adjust analysis logic

### Customizing the PR Template

Edit `.github/PULL_REQUEST_TEMPLATE.md` to:
- Add fields specific to your contribution process
- Update the checklist
- Add links to relevant documentation

## Best Practices

### When Using Copilot for Reviews

1. **Be specific**: Ask targeted questions about particular files or functions
2. **Provide context**: Include relevant information about what you're trying to achieve
3. **Iterate**: Use Copilot's feedback to refine your code, then ask for another review
4. **Verify suggestions**: Always validate Copilot's recommendations against project standards

### When Writing Intake Formats

1. **Follow the structure**: Adhere to the `Vendor/vendor-product/` directory layout
2. **Test thoroughly**: Aim for >75% test coverage
3. **Document clearly**: Provide comprehensive README and smart-descriptions
4. **Include logos**: Add appropriate logo files for visibility
5. **🔒 CRITICAL - Sanitize data**: Never include real credentials, PII, or sensitive information in test samples
6. **Use standard test data**:
   - Email domains: example.com, example.org, test.com
   - IP addresses: 192.0.2.x, 198.51.100.x, 203.0.113.x (TEST-NET ranges)
   - Usernames: user1, testuser, admin
   - Passwords: P@ssw0rd!, SecurePass123 (obvious fakes)
   - Phone numbers: +1-555-0100 (555 test range)
   - Names: John Doe, Jane Smith, User123

## Troubleshooting

### Workflow Not Running

- Check that the workflow file is in `.github/workflows/`
- Verify that pull request triggers are enabled in repository settings
- Ensure proper permissions are granted in the workflow file

### Copilot Not Responding

- Make sure you're using the `@copilot` mention in comments
- Check that GitHub Copilot is enabled for your repository/organization
- Verify that you have proper access permissions

### Custom Instructions Not Applied

- Ensure `copilot-instructions.md` is in the `.github/` directory
- Check that the file is properly formatted in Markdown
- Instructions apply to Copilot interactions within the repository

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Contribution Guidelines](../../CONTRIBUTING.md)
- [Testing Documentation](../../doc/testing.md)
- [Sekoia.io Intake Formats Documentation](../../doc/README.md)

## Feedback

If you have suggestions for improving the Copilot integration or find issues with the automation:
- Open an issue describing the problem or enhancement
- Submit a PR with proposed changes to the workflow or instructions
- Contact the maintainers for guidance

## Examples

### Example Copilot Interactions

**Security scan request:**
```
@copilot please scan all test files in this PR for sensitive information including real email addresses, API keys, passwords, IP addresses, phone numbers, and any PII
```

**Anonymization help:**
```
@copilot help me anonymize the test data in Office 365/office-365-management/tests/test_events.json - replace all real emails, IPs, and usernames with standard test values
```

**Request a comprehensive review:**
```
@copilot please review this PR and check for:
- Parser correctness and efficiency
- Test coverage completeness
- Documentation quality
- Security considerations
```

**Ask for specific improvements:**
```
@copilot the test coverage is at 65%. Can you suggest additional test cases to reach 75%?
```

**Get help with taxonomy:**
```
@copilot help me map these fields to the Sekoia.io taxonomy correctly
```

**Performance optimization:**
```
@copilot analyze the regex patterns in this parser for performance issues
```

---

**Note**: These instructions are designed to work with GitHub Copilot's PR review capabilities. The effectiveness may vary based on your GitHub plan and Copilot features available to your organization.
