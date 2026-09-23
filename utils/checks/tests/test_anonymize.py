from anonymize import Anonymizer, deep_get, parse_path


def test_parse_path_with_list_index():
    assert parse_path("a.b[0].c") == ["a", "b", "0", "c"]


def test_deep_get_with_nested_list_index():
    payload = {"a": {"b": [{"c": "value"}]}}
    assert deep_get(payload, "a.b[0].c") == "value"


def test_deep_get_returns_none_for_missing_path():
    payload = {"a": {"b": [{"c": "value"}]}}
    assert deep_get(payload, "a.b[1].c") is None


def test_replace_emails_and_usernames_supports_list_fields():
    anonymizer = Anonymizer()
    raw = {
        "expected": {
            "source": {
                "user": {
                    "name": ["Edouard", "Marie"],
                }
            }
        }
    }
    text = "Login from Edouard then MARIE"

    out = anonymizer.replace_emails_and_usernames(raw, text)

    assert out == "Login from user1 then user2"


def test_replace_urls_supports_list_fields():
    anonymizer = Anonymizer()
    raw = {
        "expected": {
            "url": {
                "original": ["https://secret-company.tld/app"],
            }
        }
    }
    text = "Visit https://secret-company.tld/app now"

    out = anonymizer.replace_urls(raw, text)

    assert out == "Visit https://example.com/app now"


def test_replace_urls_keeps_accepted_domain_with_port():
    anonymizer = Anonymizer()
    raw = {"expected": {}}
    text = "Open https://example.com:443/path"

    out = anonymizer.replace_urls(raw, text)

    assert out == text


def test_replace_urls_replaces_domain_and_preserves_port():
    anonymizer = Anonymizer()
    raw = {"expected": {}}
    text = "Open https://real-company.tld:8443/path"

    out = anonymizer.replace_urls(raw, text)

    assert out == "Open https://example.com:8443/path"


def test_replace_urls_from_expected_with_credentials_in_message():
    anonymizer = Anonymizer()
    raw = {
        "expected": {
            "url": {
                "original": ["https://alice:secret@example.com:443/path"],
            }
        }
    }
    text = "Fetch https://alice:secret@example.com:443/path now"

    out = anonymizer.replace_urls(raw, text)

    assert out == "Fetch https://example.com:443/path now"


def test_replace_ips_is_deterministic():
    anonymizer = Anonymizer()
    text = "IPs 91.198.174.192 and 142.250.74.14"

    out1 = anonymizer.replace_ips(text)
    out2 = anonymizer.replace_ips(text)

    assert out1 == out2
    assert "1.1.1.1" in out1
    assert "2.2.2.2" in out1


def test_replace_macs_is_deterministic():
    anonymizer = Anonymizer()
    raw = {"expected": {}}
    text = "MACs aa-bb-cc-dd-ee-ff and 11:22:33:44:55:66"

    out1 = anonymizer.replace_mac_addresses(raw, text)
    out2 = anonymizer.replace_mac_addresses(raw, text)

    assert out1 == out2