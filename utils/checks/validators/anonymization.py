import argparse
import ipaddress
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import INTAKES_PATH
from .constants import ValidationError


# Constants for accepted generic anonymized values
ACCEPTED_GENERIC_VALUES = {"anonymized", "redacted", "removed", "unknown", "N/A", "-", "integration", "test"}


# Constants for accepted anonymized values
ACCEPTED_IPV4_RANGES = [
    ipaddress.IPv4Network("192.0.2.0/24"),  # TEST-NET-1
    ipaddress.IPv4Network("198.51.100.0/24"),  # TEST-NET-2
    ipaddress.IPv4Network("203.0.113.0/24"),  # TEST-NET-3
    ipaddress.IPv4Network("10.0.0.0/8"),  # Private
    ipaddress.IPv4Network("172.16.0.0/12"),  # Private
    ipaddress.IPv4Network("192.168.0.0/16"),  # Private
    ipaddress.IPv4Network("127.0.0.0/8"),  # Loopback
]

ACCEPTED_IPV4_ADDRESSES = ["1.2.3.4", "5.6.7.8", "4.3.2.1", "8.7.6.5", "3.4.5.6", "6.5.4.3", "1.1.1.1"]

ACCEPTED_IPV6_RANGES = [
    ipaddress.IPv6Network("2001:db8::/32"),  # Documentation
    ipaddress.IPv6Network("fe80::/10"),  # Link-local
    ipaddress.IPv6Network("fc00::/7"),  # Unique local
]

ACCEPTED_IPV6_ADDRESSES = ["::1"]

ACCEPTED_DOMAINS = [
    r"^([\w-]+\.)*example\.(com|org|net)$",
    r"^([\w-]+\.)*test\.(corp|local)$",
    r"^([\w-]+\.)*(my)?corp\.(com|org|net)$",
    r"^([\w-]+\.)*internal\.test$",
    r"^(localhost|hostname|company|example)(\.local(domain)?)?$",
]

ACCEPTED_USERNAMES = [
    r"^J(ohn|ane)?(\s+|\.|\-)?(D|Doe|S|Smith)(\$)?$",
    r"^(D|Doe|S|Smith)(\s+|\.|\-)?J(ohn|ane)?(\$)?$",
    r"^User\d+$",
    r"^UserName(\d+)?(\$)?$",
    r"^(Test|Admin)User$",
    r"^Admin(istrator)?$",
    r"^(Alice|Bob|Charlie)$",
    r"^(root|system|SYSTEM)$",
    r"^ANONYMOUS([\s_\-/]+LOGON)?$",
    r"^Service([\s_\-/]+Account([\s_\-/]+Id)?)?$",
]

ACCEPTED_EMAIL_DOMAINS = [
    "example.com",
    "example.org",
    "example.net",
    "test.com",
    "localhost",
    "hostname",
    "mycorp.com",
    "mycorp.org",
    "mycorp.net",
]

ACCEPTED_URL_DOMAINS = [
    "example.com",
    "example.org",
    "example.net",
    "test.local",
    "localhost",
    "hostname",
    "mycorp.com",
    "mycorp.org",
    "mycorp.net",
]

ACCEPTED_PHONE_FORMATS = [
    r"^\+1-555-\d{4}$",
    r"^555-\d{4}$",
    r"^\(555\)\s?\d{3}-\d{4}$",
]

ACCEPTED_UUID = "00000000-0000-0000-0000-000000000000"

ACCEPTED_HASHES = {
    "md5": "68b329da9893e34099c7d8ad5cb9c940",
    "sha1": "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
    "sha256": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
    "sha512": "be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09",
}

ACCEPTED_SESSION_IDS = [
    "S-1-2-3",  # Test SID
    "S-1-2-3-4",  # Test SID (2)
    "S-1-0-0",  # Null Authority
    "S-1-1",  # World Authority
    "S-1-1-0",  # Everyone
    "S-1-2-0",  # Local
    "S-1-3",  # Creator Authority
    "S-1-5",  # NT Authority
    "S-1-5-1",  # Dialup
    "S-1-5-2",  # Network
    "S-1-5-3",  # Batch
    "S-1-5-4",  # Interactive
    "S-1-5-6",  # Service
    "S-1-5-7",  # Anonymous Logon
    "S-1-5-9",  # Enterprise DC
    "S-1-5-18",  # Local System
    "S-1-5-19",  # Local Service
    "S-1-5-20",  # Network Service
    "S-1-5-99",  # Builtin Domain Controllers
]


# Field paths to check for each data type
IP_FIELDS = [
    "source.ip",
    "destination.ip",
    "client.ip",
    "server.ip",
    "host.ip",
    "observer.ip",
    "source.nat.ip",
    "destination.nat.ip",
    "client.nat.ip",
    "server.nat.ip",
]

DOMAIN_FIELDS = [
    "host.name",
    "host.hostname",
    "domain",
    "user.domain",
    "source.domain",
    "destination.domain",
    "url.domain",
    "dns.question.name",
]

USERNAME_FIELDS = [
    "user.name",
    "user.id",
    "source.user.name",
    "destination.user.name",
    "process.user.name",
    "process.user.id",
    "user.target.name",
    "user.target.id",
    "action.properties.SubjectUserName",
    "action.properties.TargetUserName",
    "aws.cloudtrail.user_identity.accessKeyId",
    "aws.cloudtrail.user_identity.principalId",
]

EMAIL_FIELDS = [
    "email.from.address",
    "email.to.address",
    "email.cc.address",
    "user.email",
    "email.subject",
    "email.message_id",
    "action.properties.SenderDisplayName",
    "action.properties.RecipientObjectId",
    "google.report.actor.email",
]

URL_FIELDS = [
    "url.full",
    "url.original",
    "url.path",
    "url.query",
    "http.request.referrer",
    "event.url",
    "threat.enrichments.indicator.url.original",
]

MAC_FIELDS = [
    "source.mac",
    "destination.mac",
    "client.mac",
    "server.mac",
    "host.mac",
    "observer.mac",
]

PHONE_FIELDS = [
    "user.phone",
    "user.mobile",
    "contact.phone",
    "contact.mobile",
]

GEO_FIELDS = [
    "geo.city_name",
    "geo.region_name",
    "geo.country_name",
    "source.geo.city_name",
    "destination.geo.city_name",
    "client.geo.city_name",
    "server.geo.city_name",
    "geo.country_iso_code",
    "geo.location",
]

ORG_FIELDS = [
    "organization.name",
    "organization.id",
    "source.as.organization.name",
    "source.as.organization.id",
    "destination.as.organization.name",
    "destination.as.organization.id",
]

FILE_FIELDS = [
    "file.path",
    "file.directory",
    "process.executable",
    "process.working_directory",
]

HASH_FIELDS = [
    "file.hash.md5",
    "file.hash.sha1",
    "file.hash.sha256",
    "file.hash.sha512",
    "process.hash.md5",
    "process.hash.sha1",
    "process.hash.sha256",
    "dll.hash.md5",
    "dll.hash.sha1",
    "dll.hash.sha256",
    "email.attachments.file.hash.md5",
    "email.attachments.file.hash.sha1",
    "email.attachments.file.hash.sha256",
    "email.attachments.file.hash.sha512",
]

SESSION_ID_FIELDS = [
    "1password.session_uuid",
    "action.properties.SessionId",
    "action.properties.SessionID",
    "action.properties.InitiatingProcessSessionId",
    "paloalto.session.id",
]

ACCOUNT_ID_FIELDS = [
    "cloud.account.id",
    "cloud.account.name",
    "cloud.instance.id",
    "cloud.project.id",
    "aws.cloudtrail.user_identity.accountId",
    "aws.cloudtrail.user_identity.accessKeyId",
    "aws.cloudtrail.user_identity.principalId",
    "aws.cloudtrail.user_identity.arn",
    "aws.guardduty.finding.accesskey.accessKeyId",
    "action.properties.recipientAccountId",
    "azuread.subscriptionId",
    "azuread.tenantId",
    "azuread.resourceId",
    "azure_front_door.resource_id",
    "azure.key_vault.resource_id",
    "google_kubernetes_engine.logName",
    "google_cloud_load_balancing.logName",
    "google_cloud_audit.logName",
    "action.properties.RemoteMachineID",
    "action.properties.RemoteUserID",
    "action.properties.ServiceSid",
    "action.properties.SubjectUserSid",
    "action.properties.TargetSid",
    "action.properties.TargetUserSid",
    "crowdstrike.object_id",
    "process.parent.user.id",
    "process.user.id",
    "user.id",
    "user.target.id",
]

TOKEN_FIELDS = [
    "action.properties.ElevatedToken",
    "api_key",
    "apikey",
    "sessionToken",
]

CERTIFICATE_FIELDS = [
    "tls.client.certificate",
    "tls.server.certificate",
    "tls.cipher",
]

PROCESS_FIELDS = [
    "process.command_line",
    "process.args",
    "process.env_vars",
    "process.name",
]


class AnonymizationError(ValidationError):
    """Represents an anonymization error found in a file."""

    message: str
    code: str
    file_path: str
    field_path: str
    value: Any
    data_type: str
    reason: str

    def __str__(self):
        return (
            f"Anonymization error in {self.file_path}: "
            f"Field '{self.field_path}' (type: {self.data_type}) has value '{self.value}'. "
            f"Reason: {self.reason}"
        )


class AnonymizationValidator:
    """Validates anonymization of sensitive data in test files."""

    _anonymization_config: Optional[Dict] = None
    _anonymization_exceptions: Optional[Dict] = None

    def __init__(
        self,
        config: Optional[Dict] = None,
        exceptions: Optional[Dict] = None,
        strict: bool = False,
        lenient: bool = False,
    ):
        self.config = config or {}
        self.exceptions = exceptions or {}
        self.strict = strict
        self.lenient = lenient

        # Merge additional fields from config
        self.ip_fields = IP_FIELDS + self.config.get("additional_fields", {}).get("ip_addresses", [])
        self.domain_fields = DOMAIN_FIELDS + self.config.get("additional_fields", {}).get("domains", [])
        self.username_fields = USERNAME_FIELDS + self.config.get("additional_fields", {}).get("usernames", [])
        self.email_fields = EMAIL_FIELDS + self.config.get("additional_fields", {}).get("emails", [])
        self.url_fields = URL_FIELDS + self.config.get("additional_fields", {}).get("urls", [])
        self.mac_fields = MAC_FIELDS + self.config.get("additional_fields", {}).get("mac_addresses", [])
        self.phone_fields = PHONE_FIELDS + self.config.get("additional_fields", {}).get("phone_numbers", [])
        self.geo_fields = GEO_FIELDS + self.config.get("additional_fields", {}).get("geographic_data", [])
        self.org_fields = ORG_FIELDS + self.config.get("additional_fields", {}).get("organization_names", [])
        self.file_fields = FILE_FIELDS + self.config.get("additional_fields", {}).get("file_paths", [])
        self.hash_fields = HASH_FIELDS + self.config.get("additional_fields", {}).get("file_hashes", [])
        self.session_id_fields = SESSION_ID_FIELDS + self.config.get("additional_fields", {}).get("session_ids", [])
        self.account_id_fields = ACCOUNT_ID_FIELDS + self.config.get("additional_fields", {}).get("account_ids", [])
        self.token_fields = TOKEN_FIELDS + self.config.get("additional_fields", {}).get("tokens", [])
        self.certificate_fields = CERTIFICATE_FIELDS + self.config.get("additional_fields", {}).get("certificates", [])
        self.process_fields = PROCESS_FIELDS + self.config.get("additional_fields", {}).get("processes", [])

        # Fields to exclude
        self.exclude_fields = set(self.config.get("exclude_fields", []))

    @classmethod
    def _load_json_file(cls, file_path: Path) -> Dict:
        if file_path.exists():
            try:
                with open(file_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass  # Silently fail
        return {}

    @classmethod
    def get_anonymization_config(cls, args: argparse.Namespace) -> Dict:
        if cls._anonymization_config is None:
            if config_path := getattr(args, "anonymization_config", None):
                cls._anonymization_config = cls._load_json_file(Path(config_path))
            else:
                cls._anonymization_config = cls._load_json_file(INTAKES_PATH / ".anonymization-config.json")
        return cls._anonymization_config

    @classmethod
    def get_anonymization_exceptions(cls, args: argparse.Namespace) -> Dict:
        if cls._anonymization_exceptions is None:
            cls._anonymization_exceptions = cls._load_json_file(INTAKES_PATH / ".anonymization-exceptions.json")
        return cls._anonymization_exceptions

    def is_field_excluded(self, field_path: str) -> bool:
        """
        Check if a field path is excluded from validation.

        Args:
            field_path (str): The field path to check.
        Returns:
            bool: True if the field is excluded, False otherwise.
        """
        return field_path in self.exclude_fields

    def is_value_excepted(self, field_path: str, value: Any) -> bool:
        """
        Check if a specific value for a field path is excepted from validation.

        Args:
            field_path (str): The field path to check.
            value (Any): The value to check.
        Returns:
            bool: True if the value is excepted, False otherwise.
        """
        # Check against accepted generic values
        if str(value).lower() in ACCEPTED_GENERIC_VALUES:
            return True

        # Check against exceptions from config
        allowed = self.exceptions.get("allowed_values", {}).get(field_path, [])
        return value in allowed

    def validate_ipv4(self, ip_str: str) -> bool:
        """
        Validate if an IPv4 address is in accepted anonymized ranges.

        Args:
            ip_str (str): The IPv4 address to validate.
        Returns:
            bool: True if the IPv4 address is properly anonymized, False otherwise.
        """
        try:
            # Check against specific accepted addresses first
            if ip_str in ACCEPTED_IPV4_ADDRESSES:
                return True

            # Validate IP and check ranges
            ip = ipaddress.IPv4Address(ip_str)
            return any(ip in network for network in ACCEPTED_IPV4_RANGES)

        except (ipaddress.AddressValueError, ValueError):
            return False

    def validate_ipv6(self, ip_str: str) -> bool:
        """
        Validate if an IPv6 address is in accepted anonymized ranges.

        Args:
            ip_str (str): The IPv6 address to validate.
        Returns:
            bool: True if the IPv6 address is properly anonymized, False otherwise.
        """
        try:
            # Check against specific accepted addresses first
            if ip_str in ACCEPTED_IPV6_ADDRESSES:
                return True

            # Validate IP and check ranges
            ip = ipaddress.IPv6Address(ip_str)
            return any(ip in network for network in ACCEPTED_IPV6_RANGES)

        except (ipaddress.AddressValueError, ValueError):
            return False

    def validate_ip(self, ip_str: str) -> bool:
        """
        Validate if an IP address is in accepted anonymized ranges.

        Args:
            ip_str (str): The IP address to validate.
        Returns:
            bool: True if the IP address is properly anonymized, False otherwise.
        """
        # Check for special case of
        if ip_str == "0.0.0.0":
            return True

        # Check both IPv4 and IPv6
        return self.validate_ipv4(ip_str) or self.validate_ipv6(ip_str)

    def validate_domain(self, domain: str) -> bool:
        """
        Validate if a domain matches accepted anonymized patterns.

        Args:
            domain (str): The domain to validate.
        Returns:
            bool: True if the domain is properly anonymized, False otherwise.
        """
        # Check against accepted patterns
        for pattern in ACCEPTED_DOMAINS:
            if re.match(pattern, domain, re.IGNORECASE):
                return True

        # Check against custom patterns from config
        custom_patterns = self.config.get("custom_patterns", {}).get("domains", [])
        return any(re.match(pattern, domain, re.IGNORECASE) for pattern in custom_patterns)

    def validate_username(self, username: str) -> bool:
        """
        Validate if a username matches accepted anonymized patterns.

        Args:
            username (str): The username to validate.
        Returns:
            bool: True if the username is properly anonymized, False otherwise.
        """
        # Check against accepted usernames
        for pattern in ACCEPTED_USERNAMES:
            if re.match(pattern, username, re.IGNORECASE):
                return True

        # Check against custom patterns from config
        custom_patterns = self.config.get("custom_patterns", {}).get("usernames", [])
        for pattern in custom_patterns:
            if re.match(pattern, username, re.IGNORECASE):
                return True

        # Check against accepted session IDs
        if username.strip() in ACCEPTED_SESSION_IDS:
            return True

        # Check if the account id is a numeric id and that is a repeated digit string
        if re.fullmatch(r"\d+", username) and all(c == username[0] for c in username):
            return True

        return False

    def validate_email(self, email: str) -> bool:
        """
        Validate if an email uses an accepted anonymized domain or username.

        Args:
            email (str): The email address to validate.
        Returns:
            bool: True if the email is properly anonymized, False otherwise.
        """
        # Check for presence of '@' symbol
        if "@" not in email:
            return False

        # Split into account and domain
        account, domain = email.rsplit("@", 1)

        # Check against accepted email domains
        if domain.lower() in ACCEPTED_EMAIL_DOMAINS:
            return True

        # Check against custom email domains from config
        custom_domains = self.config.get("custom_patterns", {}).get("email_domains", [])
        if domain.lower() in [d.lower() for d in custom_domains]:
            return True

        # Check account part against accepted generic values
        if account.lower() in ACCEPTED_GENERIC_VALUES:
            return True

        # Check account part against accepted username patterns
        return any(re.match(pattern, account, re.IGNORECASE) for pattern in ACCEPTED_USERNAMES)

    def validate_url(self, url: str) -> bool:
        """
        Validate if a URL uses an accepted anonymized domain.

        Args:
            url (str): The URL to validate.
        Returns:
            bool: True if the URL is properly anonymized, False otherwise.
        """
        # Extract domain from URL
        domain_match = re.search(r"://([^/:]+)", url)

        # If no domain found, check if it's a relative URL
        if not domain_match:
            return url.startswith("/") or url.startswith("?")

        # Extracted domain
        domain = domain_match.group(1)

        # Check against accepted URL domains
        for accepted_domain in ACCEPTED_URL_DOMAINS:
            if domain.endswith(accepted_domain):
                return True
        return False

    def validate_mac(self, mac: str) -> bool:
        """
        Validate if a MAC address is a locally administered address.

        Args:
            mac (str): The MAC address to validate.
        Returns:
            bool: True if the MAC address is properly anonymized, False otherwise.
        """
        # Normalize MAC address by removing non-alphanumeric characters
        normalized_mac = "".join(filter(str.isalnum, mac)).lower()

        # If length is not 12, it's invalid
        if len(normalized_mac) != 12:
            return False

        # Check if the locally administered bit is set
        try:
            first_octet = int(normalized_mac[:2], 16)
            return (first_octet & 2) == 2
        except ValueError:
            return False

    def validate_phone(self, phone: str) -> bool:
        """
        Validate if a phone number matches accepted anonymized formats.

        Args:
            phone (str): The phone number to validate.
        Returns:
            bool: True if the phone number is properly anonymized, False otherwise.
        """
        # Check against accepted phone formats
        return any(re.match(pattern, phone) for pattern in ACCEPTED_PHONE_FORMATS)

    def validate_geo(self, location: str) -> bool:
        """
        Validate if geographic data is anonymized.

        Args:
            location (str): The geographic location to validate.
        Returns:
            bool: True if the geographic data is properly anonymized, False otherwise.
        """
        # In strict mode, only allow specific test values or accepted generic values
        if self.strict:
            test_values = ["Test City", "Test Region", "Test Country"]
            return location in test_values or location.lower() in ACCEPTED_GENERIC_VALUES
        return True

    def validate_org(self, org_name: str, field_path: str) -> bool:
        """
        Validate if organization name is anonymized.

        Args:
            org_name (str): The organization name to validate.
            field_path (str): The field path indicating the organization field.
        Returns:
            bool: True if the organization name is properly anonymized, False otherwise.
        """
        # Specific check for org ID
        if field_path.endswith(".id"):
            return org_name == "org-12345678"

        # Check against accepted test organization patterns
        test_orgs = [
            r"^Test(\s+(Corp\.?|Corporation|Company|Inc\.?|LLC))?$",
            r"^Example(\s+(Corp\.?|Corporation|Company|Inc\.?|LLC))?$",
            r"^ACME(\s+(Corp\.?|Corporation))?$",
            "Example Organization",
            "Test Organization",
        ]
        return any(re.fullmatch(pattern, org_name, re.IGNORECASE) for pattern in test_orgs) or not self.strict

    def validate_file_path(self, path: str) -> bool:
        """
        Validate if a file path contains sensitive user directory information.

        Args:
            path (str): The file path to validate.
        Returns:
            bool: True if the file path is properly anonymized, False otherwise.
        """
        # Check for sensitive user directory patterns
        sensitive_patterns = [
            re.compile(r"/home/([^/]+)"),
            re.compile(r"/Users/([^/]+)"),
            re.compile(r"C:\\Users\\([^\\]+)"),
        ]

        # Iterate over patterns to extract username and validate
        for pattern in sensitive_patterns:
            match = pattern.search(path)
            if match:
                user = match[1]
                if not self.validate_username(user):
                    return False

        return True

    def validate_uuid(self, value: str) -> bool:
        """
        Validate if a UUID matches the accepted anonymized UUID.

        Args:
            value (str): The UUID value to validate.
        Returns:
            bool: True if the UUID is properly anonymized, False otherwise.
        """
        return value == ACCEPTED_UUID

    def validate_hash(self, value: str, field_path: str) -> bool:
        """
        Validate if a hash value matches the accepted anonymized hash.

        Args:
            value (str): The hash value to validate.
            field_path (str): The field path indicating the hash type.
        Returns:
            bool: True if the hash is properly anonymized, False otherwise.
        """
        # Determine hash type from field path
        hash_type = field_path.split(".")[-1]

        # Check against accepted hashes
        if hash_type in ACCEPTED_HASHES:
            return value == ACCEPTED_HASHES[hash_type]

        return False

    def validate_session_id(self, value: str) -> bool:
        """
        Validate if a session ID matches accepted anonymized patterns.

        Args:
            value (str): The session ID value to validate.
        Returns:
            bool: True if the session ID is properly anonymized, False otherwise.
        """
        # Check against accepted session IDs
        if str(value).strip() in ACCEPTED_SESSION_IDS:
            return True

        # Check for UUID format
        if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(value), re.IGNORECASE):
            return self.validate_uuid(str(value))

        # If the SID starts with "S-1-5-21-", check for repeated digit pattern
        if str(value).startswith("S-1-5-21-"):
            parts = str(value).split("-")
            for part in parts[4:7]:
                if not (part.isdigit() and all(c == part[0] for c in part)):
                    return False

            return True

        return False

    def validate_arn(self, arn_str: str) -> bool:
        """
        Validate if an AWS ARN matches accepted anonymized patterns.

        Args:
            arn_str (str): The ARN string to validate.
        Returns:
            bool: True if the ARN is properly anonymized, False otherwise.
        """
        # Parse the ARN
        arn = ARN.parse(arn_str)

        # If parsing failed, return False
        if not arn:
            return False

        # Check against accepted account ID patterns
        if not self.validate_account_id(arn.account_id, "arn.account_id"):
            return False

        # For IAM or User ARNs, validate username
        if arn.service == "iam" and arn.resource_type == "user" and not self.validate_username(arn.resource_id):
            return False

        # For S3 ARNs, validate bucket name
        if arn.service == "s3" and arn.resource_id == "example-bucket":
            return True

        # For EC2 Instance ARNs, validate instance ID
        if arn.service == "ec2" and arn.resource_type == "instance" and arn.resource_id == "i-11111111111111":
            return True

        return False

    def validate_azure_subscription(self, resource_id: str) -> bool:
        """
        Validate if an Azure resource ID matches accepted anonymized patterns.

        Args:
            resource_id (str): The Azure resource ID to validate.
        Returns:
            bool: True if the resource ID is properly anonymized, False otherwise.
        """
        # Parse the Azure subscription resource ID
        subscription = AzureSubscription.parse(resource_id)

        # If parsing failed, return False
        if not subscription:
            return False

        # Check the subscription ID
        if not self.validate_uuid(subscription.subscription_id):
            return False

        # Check the resource group
        if subscription.resource_group not in ACCEPTED_GENERIC_VALUES:
            return False

        # Check the resource provider
        if subscription.resource_name not in ACCEPTED_GENERIC_VALUES:
            return False

        return True

    def validate_urn(self, urn_str: str) -> bool:
        """
        Validate if a URN matches accepted anonymized patterns.

        Args:
            urn_str (str): The URN string to validate.
        Returns:
            bool: True if the URN is properly anonymized, False otherwise.
        """
        # Parse the URN
        urn = URN.parse(urn_str)

        # If parsing failed, return False
        if not urn:
            return False

        # Check for the UUID nid type
        if urn.nid == "uuid":
            return self.validate_uuid(urn.nss)

        # Check for the ucode nid type
        if urn.nid == "ucode":
            return self.validate_account_id(urn.nss, "urn.nss")

        # Check for the spo nid type (Microsoft SharePoint)
        if urn.nid == "spo":
            # Extract type and id from nss
            match = re.match(r"^(?P<type>[^:#]+)[:#](?P<id>.+)$", urn.nss)

            # If no match, return False
            if not match:
                return False

            resource_type = match["type"]
            resource_id = match["id"]

            # For anonymous access, return True
            if resource_type == "anon":
                return True

            # For guest resource, validate the hash
            if resource_type == "guest":
                # Validate the resource ID as a hash
                resource_id_match = re.match(r"hash:(?P<hash>[0-9a-zA-Z]+)", resource_id)

                # If no match, return False
                if not resource_id_match:
                    return False

                # Validate the hash
                resource_hash = resource_id_match.group("hash")
                return self.validate_hash(resource_hash, "urn.spo.resource_id")

        return False

    def validate_account_id(self, value: str, field_path: str) -> bool:
        """
        Validate if an account identifier matches accepted anonymized patterns.

        Args:
            value (str): The account identifier value to validate.
            field_path (str): The field path indicating the type of account identifier.
        Returns:
            bool: True if the account identifier is properly anonymized, False otherwise.
        """
        # Check against accepted generic values
        if value.strip().lower() in ACCEPTED_GENERIC_VALUES:
            return True

        # Check against accepted session IDs
        if value.strip() in ACCEPTED_SESSION_IDS:
            return True

        # Check specific field paths for known accepted values
        if "accountId" in field_path:
            return value == "123456789012"
        if "principalId" in field_path:
            return value == "ABCDEFGHIJKLMN1234567"
        if "accessKeyId" in field_path:
            return value == "AKIAIOSFODNN7EXAMPLE"
        if "project.id" in field_path:
            return value == "my-project"
        if "instance.id" in field_path:
            return value == "my-instance"

        # Check for AWS ARN
        if "arn" in value:
            return self.validate_arn(value)

        # Check for Azure resource ID
        if "resourceId" in field_path or "/subscriptions/" in value.lower():
            return self.validate_azure_subscription(value)

        if "urn" in value.lower():
            return self.validate_urn(value)

        # Check for UUIDs in specific fields
        if "subscriptionId" in field_path or "tenantId" in field_path:
            return self.validate_uuid(value)

        # Check for session IDs
        if "Sid" in field_path or "sid" in field_path:
            return self.validate_session_id(value)

        # Check if the account id is an email
        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value):
            return self.validate_email(value)

        # Check if the account id is an UUID
        if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", value, re.IGNORECASE):
            return self.validate_uuid(value)

        # Check if the account id is a numeric id and that is a repeated digit string
        if re.fullmatch(r"\d+", value) and all(c == value[0] for c in value):
            return True

        return self.validate_username(value)

    def validate_token(self, value: str, field_path: str) -> bool:
        """
        Validate if a token matches accepted anonymized patterns.

        Args:
            value (str): The token value to validate.
            field_path (str): The field path indicating the type of token.
        Returns:
            bool: True if the token is properly anonymized, False otherwise.
        """
        # Check for API keys
        if "api_key" in field_path.lower():
            return value == "ABCD-1234-EFGH-5678-IJKL"

        # Check for session tokens
        if "sessionToken" in field_path:
            return value == "FQoGZXIvYXdzEJr//////////wEaDGV4YW1wbGVUb2tlbg=="

        # Check for OAuth tokens
        if value.startswith("ya29."):
            return value == "ya29.A0ARrdaM-EXAMPLETOKEN"

        # Check for JWT tokens
        if value.startswith("eyJ"):
            return value.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
        return False

    def validate_certificate(self, value: str, field_path: str) -> bool:
        """
        Validate if a certificate or related field matches accepted anonymized patterns.

        Args:
            value (str): The certificate or related field value to validate.
            field_path (str): The field path indicating the type of certificate data.
        Returns:
            bool: True if the certificate data is properly anonymized, False otherwise.
        """
        # Check for PEM certificate
        if field_path.endswith(".certificate"):
            return value.startswith("-----BEGIN CERTIFICATE-----")

        # Check for fingerprint
        if "fingerprint" in field_path:
            return value == "3A:5B:7C:9D:EF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD"

        # Check for cipher suites
        if "cipher" in field_path:
            return True

        # Check for x509 subject
        if "x509" in field_path:
            return "CN=example.com" in value

        return False

    def validate_process_info(self, value: str) -> bool:
        """
        Validate if process information contains sensitive data.

        Args:
            value (str): The process information to validate.
        Returns:
            bool: True if the process information is properly anonymized, False otherwise.
        """
        # Check for sensitive user directory patterns
        if "C:\\Users\\" in value or "/home/" in value or "/Users/" in value:
            return self.validate_file_path(value)

        return True

    def get_nested_value(self, data: Any, path: str) -> list[tuple[str, Any]]:
        """
        Retrieve all values from nested dictionaries/lists based on a dot-separated path.

        Args:
            data (Any): The nested data structure (dicts/lists).
            path (str): The dot-separated path to the desired value.
        Returns:
            list[tuple[str, Any]]: A list of tuples containing the full path and the corresponding value.
        """
        results = set()
        parts = path.split(".")

        def traverse(obj: Any, remaining_parts: List[str], current_path: str = ""):
            """
            Recursively traverse the data structure to find values at the specified path.

            Args:
                obj (Any): The current object being traversed.
                remaining_parts (List[str]): The remaining parts of the path to traverse.
                current_path (str): The current full path being constructed.
            """
            # Base case: no more parts to traverse
            if not remaining_parts:
                if obj is not None and obj != "":
                    # Handle lists
                    if isinstance(obj, list):
                        for item in obj:
                            if item is not None and item != "" and not isinstance(item, (list, dict)):
                                results.add((current_path.lstrip("."), item))
                    # Single value
                    elif not isinstance(obj, (list, dict)):
                        results.add((current_path.lstrip("."), obj))
                return

            # Continue traversal
            part = remaining_parts[0]
            rest = remaining_parts[1:]

            # Traverse dictionaries
            if isinstance(obj, dict):
                if part in obj:
                    new_path = f"{current_path}.{part}" if current_path else part
                    traverse(obj[part], rest, new_path)
                for key, value in obj.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    if key == part:
                        traverse(value, rest, new_path)
                    elif isinstance(value, (dict, list)):
                        traverse(value, remaining_parts, new_path)
            # Traverse lists
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    array_path = f"{current_path}[{i}]"
                    traverse(item, remaining_parts, array_path)

        traverse(data, parts)
        return list(results)

    def validate_content(self, test_content: dict, file_path: Path) -> List[AnonymizationError]:
        """
        Validate the anonymization of sensitive data in the provided test content.

        Args:
            test_content (dict): The test content to validate.
            file_path (Path): The path to the test file (for error reporting).
        Returns:
            List[ValidationError]: A list of validation errors found.
        """
        errors = []

        # Extract the expected section from the test content
        data = test_content.get("expected", {})

        # Get relative file path for error reporting
        str_file_path = str(file_path.relative_to(INTAKES_PATH))

        # Define checks for each data type
        checks = [
            (self.ip_fields, self.validate_ip, "IP Address", "Not in accepted anonymized IP ranges"),
            (self.domain_fields, self.validate_domain, "Domain", "Not in accepted anonymized domain patterns"),
            (self.username_fields, self.validate_username, "Username", "Not in accepted anonymized username patterns"),
            (self.email_fields, self.validate_email, "Email", "Not using accepted anonymized email domain"),
            (self.url_fields, self.validate_url, "URL", "Not using accepted anonymized domain in URL"),
            (self.mac_fields, self.validate_mac, "MAC Address", "Not a locally administered address"),
            (self.phone_fields, self.validate_phone, "Phone", "Not using accepted anonymized phone format"),
            (self.geo_fields, self.validate_geo, "Geographic Data", "Potential real location data (strict mode)"),
            (self.org_fields, self.validate_org, "Organization", "Potential real organization name (strict mode)"),
            (self.file_fields, self.validate_file_path, "File Path", "Contains potential sensitive user directory"),
            (self.hash_fields, self.validate_hash, "Hash", "Not an accepted anonymized hash value"),
            (self.session_id_fields, self.validate_session_id, "Session ID", "Not an accepted anonymized session ID"),
            (
                self.account_id_fields,
                self.validate_account_id,
                "Account ID",
                "Not an accepted anonymized account identifier",
            ),
            (self.token_fields, self.validate_token, "Token", "Not an accepted anonymized token"),
            (
                self.certificate_fields,
                self.validate_certificate,
                "Certificate",
                "Not an accepted anonymized certificate",
            ),
            (self.process_fields, self.validate_process_info, "Process Info", "Sensitive information not redacted"),
        ]

        # Perform checks for each data type
        for fields, validator_func, data_type, reason in checks:
            for field in fields:
                # Skip excluded fields
                if self.is_field_excluded(field):
                    continue

                # Retrieve all values for the current field
                for full_path, value in self.get_nested_value(data, field):
                    # Skip excepted values
                    if self.is_value_excepted(full_path, value):
                        continue

                    # Validate the value
                    if validator_func in [
                        self.validate_org,
                        self.validate_hash,
                        self.validate_account_id,
                        self.validate_token,
                        self.validate_certificate,
                    ]:
                        is_valid = validator_func(value, full_path)
                    else:
                        is_valid = validator_func(value)

                    if value is not None and value != "" and not is_valid:
                        errors.append(
                            AnonymizationError(
                                message="Anonymization Error",
                                code="anonymization_missing",
                                file_path=str_file_path,
                                field_path=full_path,
                                value=value,
                                data_type=data_type,
                                reason=reason,
                            )
                        )
        return errors


@dataclass
class ARN:
    """
    Represents an AWS ARN (Amazon Resource Name).
    """

    partition: str
    service: str
    region: str
    account_id: str
    resource_id: str
    resource_type: str | None

    @classmethod
    def extract_resource(cls, resource: str) -> tuple[str | None, str | None]:
        """
        Extract resource type and resource ID from the resource part of the ARN.

        Args:
            resource (str): The resource part of the ARN.
        Returns:
            tuple[str | None, str | None]: A tuple containing the resource type and resource ID
        """
        # If resource uses slash separator
        if "/" in resource:
            resource_type, resource_id = resource.split("/", 1)
            return resource_type, resource_id
        # If resource uses colon separator
        elif ":" in resource:
            resource_type, resource_id = resource.split(":", 1)
            return resource_type, resource_id
        # Otherwise, return resource as is
        else:
            return None, resource

    @classmethod
    def parse(cls, arn_str: str) -> Optional["ARN"]:
        """
        Parse an AWS ARN string into its components.

        Args:
            arn_str (str): The ARN string to parse.
        Returns:
            Optional[ARN]: An ARN object if parsing is successful, None otherwise.
        """
        # Define ARN regex pattern
        pattern = (
            r"^arn:(?P<partition>[^:]+):(?P<service>[^:]*):(?P<region>[^:]*):(?P<account_id>[^:]*):(?P<resource>.+)$"
        )

        # Match the ARN string against the pattern
        match = re.match(pattern, arn_str)

        # If match is found, extract components
        if match:
            resource_type, resource_id = cls.extract_resource(match["resource"])
            return cls(
                partition=match["partition"],
                service=match["service"],
                region=match["region"],
                account_id=match["account_id"],
                resource_type=resource_type,
                resource_id=resource_id,
            )

        # If no match, return None
        return None


@dataclass
class AzureSubscription:
    """
    Represents an Azure Subscription Resource ID.
    """

    subscription_id: str
    resource_group: str
    resource_provider: str
    resource_type: str
    resource_name: str

    @classmethod
    def parse(cls, resource_id: str) -> Optional["AzureSubscription"]:
        """
        Parse an Azure resource ID string into its components.

        Args:
            resource_id (str): The Azure resource ID string to parse.
        Returns:
            Optional[AzureSubscription]: An AzureSubscription object if parsing is successful, None otherwise.
        """
        # Define Azure resource ID regex pattern
        pattern = (
            r"^/subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/"
            r"(?P<resource_provider>[^/]+)/(?P<resource_type>[^/]+)/(?P<resource_name>[^/]+)$"
        )

        # Match the resource ID against the pattern
        match = re.match(pattern, resource_id, re.IGNORECASE)

        # If match is found, extract components
        if match:
            return cls(
                subscription_id=match["subscription_id"],
                resource_group=match["resource_group"],
                resource_provider=match["resource_provider"],
                resource_type=match["resource_type"],
                resource_name=match["resource_name"],
            )

        # If no match, return None
        return None


@dataclass
class URN:
    """
    Represents a URN (Uniform Resource Name).
    """

    nid: str
    nss: str

    @classmethod
    def parse(cls, urn_str: str) -> Optional["URN"]:
        """
        Parse a URN string into its components.

        Args:
            urn_str (str): The URN string to parse.
        Returns:
            Optional[URN]: A URN object if parsing is successful, None otherwise.
        """
        # Define URN regex pattern
        pattern = r"^urn:(?P<nid>[^:]+):(?P<nss>.+)$"

        # Match the URN string against the pattern
        match = re.match(pattern, urn_str)

        # If match is found, extract components
        if match:
            return cls(
                nid=match["nid"],
                nss=match["nss"],
            )

        # If no match, return None
        return None
