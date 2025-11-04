import pytest
from pathlib import Path
from checks.validators.anonymization import AnonymizationValidator


@pytest.fixture
def validator():
    return AnonymizationValidator()


@pytest.fixture
def strict_validator():
    return AnonymizationValidator(strict=True)


class TestAnonymizationValidator:
    @pytest.mark.parametrize(
        "ip, expected",
        [
            ("192.0.2.1", True),
            ("198.51.100.10", True),
            ("203.0.113.200", True),
            ("10.1.2.3", True),
            ("172.16.1.1", True),
            ("192.168.1.1", True),
            ("127.0.0.1", True),
            ("1.2.3.4", True),
            ("8.8.8.8", False),
            ("1.1.1.2", False),
            ("not-an-ip", False),
        ],
    )
    def test_validate_ipv4(self, validator, ip, expected):
        assert validator.validate_ipv4(ip) == expected

    @pytest.mark.parametrize(
        "ip, expected",
        [
            ("2001:db8::1", True),
            ("fe80::1", True),
            ("fc00::1", True),
            ("::1", True),
            ("2001:db9::1", False),
            ("not-an-ip", False),
        ],
    )
    def test_validate_ipv6(self, validator, ip, expected):
        assert validator.validate_ipv6(ip) == expected

    @pytest.mark.parametrize(
        "ip, expected",
        [
            ("192.0.2.1", True),
            ("2001:db8::1", True),
            ("8.8.8.8", False),
            ("2001:db9::1", False),
            ("0.0.0.0", True),
        ],
    )
    def test_validate_ip(self, validator, ip, expected):
        assert validator.validate_ip(ip) == expected

    @pytest.mark.parametrize(
        "domain, expected",
        [
            ("example.com", True),  # Domain is accepted
            ("sub.example.org", True),  # Domain is accepted
            ("test.corp", True),  # Domain is accepted
            ("mycorp.com", True),  # Domain is accepted
            ("localhost", True),  # Domain is accepted
            ("hostname.local", True),  # Domain is accepted
            ("google.com", False),
            ("sekoia.io", False),
        ],
    )
    def test_validate_domain(self, validator, domain, expected):
        assert validator.validate_domain(domain) == expected

    @pytest.mark.parametrize(
        "username, expected",
        [
            ("John.Doe", True),
            ("User123", True),
            ("AdminUser", True),
            ("root", True),
            ("SYSTEM", True),
            ("ANONYMOUS_LOGON", True),
            ("111111", True),
            ("2222", True),
            ("00000000-0000-0000-0000-000000000000", True),
            ("edouard", False),
            ("my-user", False),
        ],
    )
    def test_validate_username(self, validator, username, expected):
        assert validator.validate_username(username) == expected

    @pytest.mark.parametrize(
        "email, expected",
        [
            ("test@example.com", True),  # Domain is accepted
            ("john.doe@test.com", True),  # Domain is accepted
            ("redacted@domain.com", True),  # Account is redacted
            ("user1@mycorp.com", True),  # Domain is accepted
            ("test@gmail.com", True),  # Account is redacted
            ("marie.poppins@gmail.com", False),
            ("not-an-email", False),
        ],
    )
    def test_validate_email(self, validator, email, expected):
        assert validator.validate_email(email) == expected

    @pytest.mark.parametrize(
        "url, expected",
        [
            ("http://example.com/path", True),
            ("https://sub.test.local/page?query=1", True),
            ("/relative/path", True),
            ("?query=true", True),
            ("http://google.com", False),
            ("ftp://example.com/file", True),
        ],
    )
    def test_validate_url(self, validator, url, expected):
        assert validator.validate_url(url) == expected

    @pytest.mark.parametrize(
        "mac, expected",
        [
            ("02:00:00:00:00:00", True),
            ("0A-1B-2C-3D-4E-5F", True),
            ("0e:00:00:00:00:00", True),
            ("FF-FF-FF-FF-FF-FF", True),
            ("00:00:00:00:00:00", False),
            ("01:00:00:00:00:00", False),
            ("59:1f:99:f1:96:e5", False),
            ("not-a-mac", False),
        ],
    )
    def test_validate_mac(self, validator, mac, expected):
        assert validator.validate_mac(mac) == expected

    @pytest.mark.parametrize(
        "phone, expected",
        [
            ("+1-555-1234", True),
            ("555-5678", True),
            ("(555) 123-4567", True),
            ("(555)123-4567", True),
            ("+1-123-456-7890", False),
            ("1234567", False),
        ],
    )
    def test_validate_phone(self, validator, phone, expected):
        assert validator.validate_phone(phone) == expected

    @pytest.mark.parametrize(
        "location, strict, expected",
        [
            ("Test City", True, True),
            ("Test Region", True, True),
            ("Test Country", True, True),
            ("anonymized", True, True),
            ("Paris", True, False),
            ("London", True, False),
            ("Paris", False, True),
            ("London", False, True),
        ],
    )
    def test_validate_geo(self, location, strict, expected):
        validator = AnonymizationValidator(strict=strict)
        assert validator.validate_geo(location) == expected

    @pytest.mark.parametrize(
        "org_name, field_path, strict, expected",
        [
            ("org-12345678", "organization.id", False, True),
            ("org-12345678", "organization.id", True, True),
            ("my-org", "organization.id", False, False),
            ("my-org", "organization.id", True, False),
            ("Test Corp", "organization.name", True, True),
            ("Example Inc.", "organization.name", True, True),
            ("ACME", "organization.name", True, True),
            ("My Company", "organization.name", True, False),
            ("Sekoia.io", "organization.name", True, False),
            ("Test Corp", "organization.name", False, True),
            ("My Company", "organization.name", False, True),
            ("Sekoia.io", "organization.name", False, True),
        ],
    )
    def test_validate_org(self, org_name, field_path, strict, expected):
        validator = AnonymizationValidator(strict=strict)
        assert validator.validate_org(org_name, field_path) == expected

    @pytest.mark.parametrize(
        "path, expected",
        [
            ("/usr/bin/myapp", True),
            ("C:\\Windows\\System32\\kernel32.dll", True),
            ("/home/john.doe/file", True),
            ("/home/User01/file", True),
            ("C:\\Users\\Administrator\\file", True),
            ("/home/realuser/file", False),
            ("C:\\Users\\RealUser\\file", False),
        ],
    )
    def test_validate_file_path(self, validator, path, expected):
        assert validator.validate_file_path(path) == expected

    @pytest.mark.parametrize(
        "uuid, expected",
        [
            ("00000000-0000-0000-0000-000000000000", True),
            ("11111111-1111-1111-1111-111111111111", True),
            ("123e4567-e89b-12d3-a456-426614174000", False),
        ],
    )
    def test_validate_uuid(self, validator, uuid, expected):
        assert validator.validate_uuid(uuid) == expected

    @pytest.mark.parametrize(
        "value, field_path, expected",
        [
            ("68b329da9893e34099c7d8ad5cb9c940", "file.hash.md5", True),
            ("adc83b19e793491b1c6ea0fd8b46cd9f32e592fc", "file.hash.sha1", True),
            (
                "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
                "process.hash.sha256",
                True,
            ),
            (
                "be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09",
                "email.attachments.file.hash.sha512",
                True,
            ),
            ("11111111111111111111111111111111", "file.hash.md5", True),
            ("d41d8cd98f00b204e9800998ecf8427e", "file.hash.md5", False),
            ("da39a3ee5e6b4b0d3255bfef95601890afd80709", "file.hash.sha1", False),
        ],
    )
    def test_validate_hash(self, validator, value, field_path, expected):
        assert validator.validate_hash(value, field_path) == expected

    @pytest.mark.parametrize(
        "value, field_path, expected",
        [
            ("demo", "account.id", True),
            ("S-1-5-3", "account.id", True),
            ("123456789012", "accountId", True),
            ("john.doe@example.org", "account.id", True),
            ("11111111-1111-1111-1111-111111111111", "account.id", True),
            ("11111111111111", "account.id", True),
            ("ABCDEFGHIJKLMN1234567", "principalId", True),
            ("AKIA1111111111111111", "accessKeyId", True),
            ("my-project", "project.id", True),
            ("my-instance", "instance.id", True),
            ("i-00000000000000000", "cloud.instance.id", True),
            ("ASIA1111111111111", "aws.cloudtrail.user_identity.accessKeyId", True),
            ("AAAAA", "aws.cloudtrail.user_identity.accessKeyId", True),
            ("arn:aws:iam::111111111111:user/john.doe", "aws.cloudtrail.user_identity.arn", True),
            ("arn:aws:iam::111111111111:user/root", "aws.cloudtrail.user_identity.arn", True),
            ("arn:aws:sns:us-east-1:111111111111:example-sns-topic-name", "aws.cloudtrail.user_identity.arn", True),
            (
                "arn:aws:sts::1111111111:assumed-role/role/1111111111111111111111111",
                "aws.cloudtrail.user_identity.arn",
                True,
            ),
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-111111111111/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                "azuread.subscriptionId",
                True,
            ),
            ("urn:uuid:11111111-1111-1111-1111-111111111111", "account.id", True),
            ("urn:ucode:2222222222222222", "account.id", True),
            ("urn:spo:anon", "account.id", True),
            ("urn:spo:guest:hash#68b329da9893e34099c7d8ad5cb9c940", "account.id", True),
            ("MyPrincipalID12345", "principalId", False),
            ("AKIAIOSFODNN7EXAMPLE", "accessKeyId", False),
            ("project-austin", "project.id", False),
            ("instance-valerian", "instance.id", False),
            ("arn:aws:iam::111111111111:user/catherine", "aws.cloudtrail.user_identity.arn", False),
            (
                "/SUBSCRIPTIONS/123e4567-e89b-12d3-a456-426614174000/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                "azuread.subscriptionId",
                False,
            ),
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-111111111111/RESOURCEGROUPS/ResourceGroup/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                "azuread.subscriptionId",
                False,
            ),
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-111111111111/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/VAULT",
                "azuread.subscriptionId",
                False,
            ),
            ("urn:uuid:123e4567-e89b-12d3-a456-426614174000", "account.id", False),
            ("urn:spo:guest:hash#aSPngX3nlOfknaGB", "account.id", False),
            ("random-account-id", "account.id", False),
            ("bitcoin@nasdaq.org", "account.id", False),
            ("123e4567-e89b-12d3-a456-426614174000", "account.id", False),
            ("12342134642", "account.id", False),
        ],
    )
    def test_validate_account_id(self, validator, value, field_path, expected):
        assert validator.validate_account_id(value, field_path) == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("arn:aws:iam::111111111111:user/john.doe", True),
            ("arn:aws:iam::111111111111:user/root", True),
            ("arn:aws:sns:us-east-1:111111111111:example-sns-topic-name", True),
            (
                "arn:aws:sts::1111111111:assumed-role/role/1111111111111111111111111",
                True,
            ),
            ("arn:aws:iam::111111111111:user/catherine", False),
        ],
    )
    def test_validate_arn(self, validator, value, expected):
        assert validator.validate_arn(value) == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-1111111111/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                True,
            ),
            (
                "/SUBSCRIPTIONS/123e4567-e89b-12d3-a456-426614174000/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                False,
            ),
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-1111111111/RESOURCEGROUPS/ResourceGroup/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/TEST",
                False,
            ),
            (
                "/SUBSCRIPTIONS/11111111-1111-1111-1111-1111111111/RESOURCEGROUPS/INTEGRATION/PROVIDERS/MICROSOFT.KEYVAULT/VAULTS/VAULT",
                False,
            ),
        ],
    )
    def test_validate_azure_subscription(self, validator, value, expected):
        assert validator.validate_azure_subscription(value) == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("urn:uuid:11111111-1111-1111-1111-1111111111", True),
            ("urn:ucode:2222222222222222", True),
            ("urn:spo:anon", True),
            ("urn:spo:guest:hash#68b329da9893e34099c7d8ad5cb9c940", True),
            ("urn:uuid:123e4567-e89b-12d3-a456-426614174000", False),
            ("urn:spo:guest:hash#aSPngX3nlOfknaGB", False),
        ],
    )
    def test_validate_urn(self, validator, value, expected):
        assert validator.validate_urn(value) == expected

    def test_get_nested_value(self, validator):
        data = {
            "source": {"ip": "1.2.3.4", "port": 123},
            "destination": {"ip": "5.6.7.8"},
            "network": {"ips": ["1.1.1.1", "2.2.2.2"]},
            "foo": [{"bar": {"ip": "9.9.9.9"}}],
            "flat_ip": "4.3.2.1",
            "list_of_objects": [{"name": "a", "value": "x"}, {"name": "b", "value": "y"}],
        }

        expected_ip = {
            ("source.ip", "1.2.3.4"),
            ("destination.ip", "5.6.7.8"),
            ("foo[0].bar.ip", "9.9.9.9"),
        }
        assert set(validator.get_nested_value(data, "ip")) == expected_ip

        expected_source_ip = {("source.ip", "1.2.3.4")}
        assert set(validator.get_nested_value(data, "source.ip")) == expected_source_ip

        expected_ips = {("network.ips", "1.1.1.1"), ("network.ips", "2.2.2.2")}
        assert set(validator.get_nested_value(data, "network.ips")) == expected_ips

        expected_values = {
            ("list_of_objects[0].value", "x"),
            ("list_of_objects[1].value", "y"),
        }
        assert set(validator.get_nested_value(data, "value")) == expected_values

    def test_validate_content(self, validator, monkeypatch):
        monkeypatch.setattr("checks.validators.anonymization.INTAKES_PATH", Path("."))
        test_content = {
            "expected": {
                "source": {"ip": "8.8.8.8"},
                "destination": {"ip": "1.2.3.4"},
                "user": {"name": "realuser"},
                "domain": "google.com",
            }
        }
        file_path = Path("module/tests/test.json")
        errors = validator.validate_content(test_content, file_path)
        assert len(errors) == 3

        error_fields = {e.field_path for e in errors}
        assert "source.ip" in error_fields
        assert "user.name" in error_fields
        assert "domain" in error_fields
