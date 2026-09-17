---
name: fix-anonymization
description: "Detect and fix anonymization issues (real PII/IP/credentials leaked in test data) for a specific module or format. Use when: user asks to 'fix anonymization', 'check anonymization issues', 'anonymize tests for <vendor/product>', or a CI anonymization check fails."
argument-hint: "Module and/or format to check (e.g., 'Fortinet' or 'Fortinet/fortigate')"
---

# fix-anonymization

Run the repository-wide anonymization checker, then diagnose and fix the issues that belong to the
module/format requested by the user.

## Context

- The anonymization checker lives at `utils/checks` and is invoked with `uv run python utils/checks`.
- It **always scans every module and format** — it has no `--module`/`--format` filter option.
  The agent MUST run it in full, then filter the JSON results itself to the module/format the
  user asked about.
- Anonymization rules and accepted "safe" values are documented in
  `.github/SECURITY_ANONYMIZATION_GUIDE.md`. Always consult this file to judge whether a flagged
  value is genuinely sensitive.
- The actual validation logic (accepted IP ranges, domains, usernames, regexes, etc.) lives in
  `utils/checks/validators/anonymization.py`.
- Known, legitimate exceptions (values that are safe but don't match the generic patterns) can be
  declared in `.anonymization-exceptions.json` at the repo root, under `allowed_values.<field_path>`.

## Actions to perform

1. **Identify the target** from the user's prompt: a module name (e.g. `Fortinet`), a format path
   (e.g. `Fortinet/fortigate`), or both. If ambiguous, ask the user to clarify before proceeding.

2. **Run the full anonymization check** (there is no way to scope it upfront):

   ```bash
   cd utils && uv run python checks --json
   ```

3. **Filter the JSON output** to keep only entries whose `path` matches the requested module/format
   (e.g. entries under `Fortinet/` or exactly `Fortinet/fortigate`). Ignore unrelated errors from
   other modules/formats — do not attempt to fix those.

4. **For each remaining anonymization error** (`code: "anonymization_missing"`, with `field_path`,
   `value`, `data_type`, `reason`, `file_path`):

   a. Open the referenced `file_path` (typically a file under `tests/`) and inspect the flagged
      `value` in context.

   b. Decide, using `.github/SECURITY_ANONYMIZATION_GUIDE.md` as the reference:

      - **Case A — Real sensitive data**: the value is genuinely a real IP, email, name, hostname,
        credential, etc. that isn't anonymized.
        → **Fix the test data**: replace the value in the test file with an anonymized equivalent
        from the guide (e.g. `192.0.2.x`/`198.51.100.x`/`203.0.113.x` for IPs, `user@example.com`
        for emails, `John Doe`/`user1` for names, obvious fake tokens/hashes, etc.). Keep the
        replacement consistent across the file if the same value appears multiple times, and keep
        it plausible for the field's data type.
        → After editing, re-run the parser tests for that format (see `validate-parser` skill) to
        confirm the parser output still matches, using `--fix-expectations` only if the change only
        affects the raw/anonymized value and not real parsing logic.

      - **Case B — False positive / overly strict validator**: the value is already a clearly
        anonymized/redacted/safe value (per the guide) but doesn't match any pattern in
        `utils/checks/validators/anonymization.py` (e.g. a new safe domain, a new safe username
        pattern, a new safe generic placeholder).
        → Prefer the smallest safe fix:
          1. First consider adding the value to `.anonymization-exceptions.json` under
             `allowed_values.<field_path>` if it's a one-off, legitimate value tied to a specific field.
          2. If the value represents a whole class of legitimately-anonymized values (e.g. a new
             accepted domain suffix, username pattern, IP range, or generic placeholder), update the
             relevant constant/regex list in `utils/checks/validators/anonymization.py`
             (e.g. `ACCEPTED_DOMAINS`, `ACCEPTED_USERNAMES`, `ACCEPTED_EMAIL_DOMAINS`,
             `ACCEPTED_GENERIC_VALUES`, `ACCEPTED_IPV4_RANGES`, etc.) so the validator accepts it
             going forward.
        → Never loosen the validator just to silence a real leak — only extend it when the value is
          genuinely already anonymized/non-sensitive.

   c. If unsure which case applies, treat it as Case A (fix the test data) — anonymizing a
      technically-safe value is a bounded no-op, while under-fixing risks leaking real data.

5. **Re-run the full check** after fixes to confirm the targeted module/format is now clean:

   ```bash
   cd utils && uv run python checks --json
   ```

   Filter again for the same module/format and confirm zero remaining anonymization errors there.

6. **Run the parser tests/linting** for any format whose test files were modified (see
   `validate-parser` skill) to ensure the fix didn't break parsing.

## Output

Report to the user, grouped by file:
- ✅ Issues found and fixed in test data (value → anonymized replacement)
- 🛠️ Validator updates made (constant/regex changed, or exception added) and why they were safe
- ⚠️ Any remaining issues that need a manual decision (e.g. ambiguous real vs. fake data)
- ✅ Confirmation that tests/linting still pass after the fix
