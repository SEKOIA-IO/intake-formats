import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse

from checks.validators.anonymization import (
    ACCEPTED_GENERIC_VALUES,
    MAC_FIELDS,
    URL_FIELDS,
    USERNAME_FIELDS,
    AnonymizationValidator,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger(__name__)


# --- Utility Functions for Nested JSON Manipulation ---
def parse_path(path) -> list[str]:
    """
    Parses a dot-separated path string, potentially containing array indices
    (e.g., 'a.b[0].c'), into a list of individual keys/indices.
    Example: 'a.b[0].c' -> ['a', 'b', '0', 'c']
    """
    return re.findall(r"[^.[\\]+", path)


def deep_get(data: Any, path: str) -> Any:
    """
    Retrieves a value from a deeply nested dictionary or list structure using a
    dot-separated path string. It handles both dictionary keys and list indices.
    Returns None if the path does not exist or is invalid.
    """
    keys = parse_path(path)
    current_level = data
    for key in keys:
        if not hasattr(current_level, "__getitem__"):
            return None  # Cannot traverse further
        if key.isdigit() and isinstance(current_level, list):
            try:
                current_level = current_level[int(key)]
            except IndexError:
                return None  # Index out of bounds
        elif isinstance(current_level, dict):
            current_level = current_level.get(key)
        else:
            return None  # Not a dict or list at this level
    return current_level


def gather_files(paths: list) -> list[Path]:
    result = []
    for target in paths:
        target_path = Path(target)
        if target_path.is_file():
            result.append(target_path)

        else:
            for path in target_path.rglob("*.json"):
                if path.parent.name != "tests":
                    continue

                result.append(path)

    return result


class Anonymizer:
    def __init__(self) -> None:
        self.anonymization_check = AnonymizationValidator()

    @staticmethod
    def generate_fake_uuids():
        # Generate all-numeric UUIDs

        # Starting from the same number (e.g. 11111111-1111-1111-1111-111111111111)
        for digit in range(1, 10):
            d = str(digit)
            yield f"{d * 8}-{d * 4}-{d * 4}-{d * 4}-{d * 12}"

        # After 99999999-9999-9999-9999-999999999999, change numbers by one group
        groups = [1, 1, 1, 1, 2]

        while True:
            uuid_str = (
                f"{str(groups[0]) * 8}-"
                f"{str(groups[1]) * 4}-"
                f"{str(groups[2]) * 4}-"
                f"{str(groups[3]) * 4}-"
                f"{str(groups[4]) * 12}"
            )
            yield uuid_str

            groups[4] += 1

            for i in range(4, -1, -1):
                if groups[i] > 9:
                    groups[i] = 1
                    if i > 0:
                        groups[i - 1] += 1

    @staticmethod
    def generate_fake_sids():
        for digit in range(1, 10):
            d = str(digit)
            yield f"S-1-5-21-{d * 9}-{d * 9}-{d * 9}-{d * 9}"

        groups = [1, 1, 1, 2]

        while True:
            uuid_str = (
                f"S-1-5-21-"
                f"{str(groups[0]) * 9}-"
                f"{str(groups[1]) * 9}-"
                f"{str(groups[2]) * 9}-"
                f"{str(groups[3]) * 9}"
            )
            yield uuid_str

            groups[3] += 1

            for i in range(3, -1, -1):
                if groups[i] > 9:
                    groups[i] = 1
                    if i > 0:
                        groups[i - 1] += 1

    @staticmethod
    def generate_fake_mac_addresses():
        groups = [0, 0, 0, 0, 1]

        while True:
            yield "02" + "".join(f"{num:02x}" for num in groups)

            groups[4] += 1

            for i in range(4, -1, -1):
                if groups[i] > 16:
                    groups[i] = 1
                    if i > 0:
                        groups[i - 1] += 1

    def replace_uuids(self, t: str):
        re_uuid = "[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
        all_uuids = set(re.findall(re_uuid, t))

        uuids_correct = set()
        uuids_to_fix = set()
        for u in all_uuids:
            if self.anonymization_check.validate_uuid(u):
                uuids_correct.add(u)

            else:
                uuids_to_fix.add(u)

        uuid_to_replace = {}

        # We don't want to overwrite correct UUIDs
        fake_uuids = self.generate_fake_uuids()
        for uuid_old in uuids_to_fix:
            uuid_new = next(fake_uuids)
            while uuid_new in uuids_correct:
                uuid_new = next(fake_uuids)

            uuid_to_replace[uuid_old] = uuid_new

        for uuid_old, uuid_new in uuid_to_replace.items():
            logger.warning(f"Will replace {uuid_old} with {uuid_new}")
            t = t.replace(uuid_old, uuid_new)

        return t

    def replace_hash(self, t: str, ln: int, c: str):
        re_hash = '"([0-9A-Fa-f]{%d})"' % ln
        all_hashes = set(re.findall(re_hash, t))

        hash_to_new = {}
        for hash in all_hashes:
            if hash != c:
                hash_to_new[hash] = c

        for hash_old, hash_new in hash_to_new.items():
            logger.warning(f"Will replace {hash_old} with {hash_new}")
            t = t.replace(hash_old, hash_new)

        return t

    def replace_hashes(self, t: str):
        # these are hashes from anonymization checker
        t = self.replace_hash(
            t,
            128,
            "be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09",
        )  # sha-512
        t = self.replace_hash(t, 64, "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b")  # sha-256
        t = self.replace_hash(t, 40, "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc")  # sha-1
        t = self.replace_hash(t, 32, "68b329da9893e34099c7d8ad5cb9c940")  # md5
        return t

    def replace_ips(self, t: str):
        re_ips = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        all_ips = set(re.findall(re_ips, t))

        # hacks
        chrome_versions = set(re.findall(r"Chrome/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", t))
        mozilla_versions = set(re.findall(r"rv:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", t))

        all_ips = all_ips - chrome_versions - mozilla_versions

        ips_correct = set()
        ips_to_fix = set()
        for ip in all_ips:
            if self.anonymization_check.validate_ip(ip):
                ips_correct.add(ip)
            else:
                ips_to_fix.add(ip)

        ip_to_new = {}

        n = 1
        for ip in ips_to_fix:
            tmp = [str(n)] * 4
            new_ip = ".".join(tmp)

            while new_ip in ips_correct:
                n += 1
                tmp = [str(n)] * 4
                new_ip = ".".join(tmp)

            ip_to_new[ip] = new_ip

            n += 1

        for ip_old, ip_new in ip_to_new.items():
            logger.warning(f"Will replace {ip_old} with {ip_new}")
            t = t.replace(ip_old, ip_new)

        return t

    def validate_username(self, v: str) -> bool:
        if str(v).lower() in ACCEPTED_GENERIC_VALUES:
            return True

        return self.anonymization_check.validate_username(v)

    def validate_url(self, v: str) -> bool:
        if str(v).lower() in ACCEPTED_GENERIC_VALUES:
            return True

        return self.anonymization_check.validate_url(v)

    def validate_domain(self, v: str) -> bool:
        if str(v).lower() in ACCEPTED_GENERIC_VALUES:
            return True

        return self.anonymization_check.validate_domain(v)

    def validate_mac(self, v: str) -> bool:
        if str(v).lower() in ACCEPTED_GENERIC_VALUES:
            return True

        # we won't fix MAC address that doesn't event look like a MAC address
        normalized_mac = "".join(filter(str.isalnum, v)).lower()
        if len(normalized_mac) != 12:
            return False

        return self.anonymization_check.validate_mac(v)

    def replace_emails_and_usernames(self, raw: dict[str, Any], text: str) -> str:
        usernames_to_replace = set()

        email_mapping = {}
        username_mapping = {}

        # Try to use extracted fields first
        for field_name in USERNAME_FIELDS:
            field_value = deep_get(raw["expected"], field_name)
            if field_value:
                if not self.validate_username(field_value):
                    usernames_to_replace.add(field_value)

        # Search trough raw message
        # (?<!\\) in order to avoid grabbing escaped characters (e.g. \\t) along with an email
        re_email = r"\b(?<!\\)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        all_emails = set(re.findall(re_email, text))

        for email in all_emails:
            username, domain = email.split("@")

            # First, we have to check email's address domain
            if not self.validate_domain(domain):
                email_mapping[email] = f"{username}@example.com"

            # Then check username as well
            if not self.validate_username(username):
                # as we identified username, we can now replace it through the whole event
                usernames_to_replace.add(username)

        for i, username in enumerate(usernames_to_replace, start=1):
            logger.warning(f"Will replace {username} with user{i}")
            username_mapping[f"user{i}"] = re.compile(re.escape(username), re.IGNORECASE)

        for email_from, email_to in email_mapping.items():
            logger.warning(f"Will replace {email_from} with {email_to}")
            text = text.replace(email_from, email_to)

        for username_to, username_re in username_mapping.items():
            text = username_re.sub(username_to, text)

        return text

    def replace_urls(self, raw: dict[str, Any], text: str) -> str:
        re_url = r"\b(?:http|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])\b"
        all_urls = set(re.findall(re_url, text))
        url_mapping = {}

        # Try to use extracted fields as well
        for field_name in URL_FIELDS:
            field_value = deep_get(raw["expected"], field_name)
            if field_value:
                if not self.validate_url(field_value):
                    all_urls.add(field_value)

        if all_urls:
            for url in all_urls:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                if not self.validate_domain(domain):
                    new_domain = "example.com"
                    updated_url = parsed_url._replace(netloc=new_domain)
                    url_mapping[url] = urlunparse(updated_url)

        for url_from, url_to in url_mapping.items():
            logger.warning(f"Replacing {url_from} with {url_to}")
            text = text.replace(url_from, url_to)

        return text

    def replace_session_ids(self, t: str) -> str:
        re_sid = r"S-1-\d{1,3}-\d{1,3}(?:-\d{1,9}){1,10}"

        all_sids = re.findall(re_sid, t)

        sids_correct = set()
        sids_to_fix = set()

        for sid in all_sids:
            if self.anonymization_check.validate_session_id(sid):
                sids_correct.add(sid)

            else:
                sids_to_fix.add(sid)

        fake_sids = self.generate_fake_sids()
        sid_to_replace = {}

        for sid_old in sids_to_fix:
            sid_new = next(fake_sids)
            # We don't want to overwrite correct SIDs
            while sid_new in sids_correct:
                sid_new = next(fake_sids)

            sid_to_replace[sid_old] = sid_new

        for sid_old, sid_new in sid_to_replace.items():
            logger.warning(f"Will replace {sid_old} with {sid_new}")
            t = t.replace(sid_old, sid_new)

        return t

    @staticmethod
    def normalize_mac(mac: str) -> str:
        """
        Strip all separators and lowercase -> canonical 12 hex-char form.
        e.g. 'AA-bb:CC.DD.EE.FF' -> 'aabbccddeeff'
        """
        return re.sub(r"[^0-9A-Fa-f]", "", mac).lower()

    @staticmethod
    def detect_mac_format(mac: str) -> tuple[str, int, bool]:
        """Return (separator, group_size, is_upper) describing MAC address style."""
        if ":" in mac:
            sep, group = ":", 2
        elif "-" in mac:
            sep, group = "-", 2
        elif "." in mac:
            sep, group = ".", 4
        else:
            sep, group = "", 2

        letters = [c for c in mac if c.isalpha()]
        is_upper = bool(letters) and all(c.isupper() for c in letters)
        return sep, group, is_upper

    def format_mac(self, mac: str, sep: str, group: int, is_upper: bool) -> str:
        mac = self.normalize_mac(mac)
        mac = sep.join(mac[i : i + group] for i in range(0, 12, group))
        if is_upper:
            mac = mac.upper()

        return mac

    def replace_mac_addresses(self, raw: dict[str, Any], t: str) -> str:
        macs_to_replace = set()
        macs_correct_normalized = set()

        # We use it for the extracted fields, so AABBCCDDEEFF is definitely valid
        MAC_PATTERN = re.compile(
            r"""
            (?<![0-9A-Fa-f:\-])                   # not preceded by more hex/sep chars
            (?:
                (?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}     |  # AA:BB:CC:DD:EE:FF / AA-BB-...
                (?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}       |  # AABB.CCDD.EEFF
                [0-9A-Fa-f]{12}                                # AABBCCDDEEFF
            )
            (?![0-9A-Fa-f:\-])                    # not followed by more hex/sep chars
            (?!\.[0-9A-Fa-f]{4})                  # ...and not immediately followed by another .hex4 group
            """,
            re.VERBOSE,
        )

        # We use it to find non-extracted MAC addresses, so AABBCCDDEEFF could be false positive
        STRICT_MAC_PATTERN = re.compile(
            r"""
            (?<![0-9A-Fa-f:\-])                   # not preceded by more hex/sep chars
            (?:
                (?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}     |  # AA:BB:CC:DD:EE:FF / AA-BB-...
                (?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}          # AABB.CCDD.EEFF
            )
            (?![0-9A-Fa-f:\-])                    # not followed by more hex/sep chars
            (?!\.[0-9A-Fa-f]{4})                  # ...and not immediately followed by another .hex4 group
            """,
            re.VERBOSE,
        )

        for field_name in MAC_FIELDS:
            field_value = deep_get(raw["expected"], field_name)
            if field_value:
                vals = []

                if isinstance(field_value, str):
                    vals = [field_value]

                # Fields like host.mac could contain multiple values
                elif isinstance(field_value, list):
                    vals = field_value

                for v in vals:
                    # We could only fix something that looks like MAC address.
                    if re.match(MAC_PATTERN, v):
                        if self.validate_mac(v):
                            macs_correct_normalized.add(self.normalize_mac(v))

                        else:
                            macs_to_replace.add(v)

                    else:
                        logger.warning(f"`{v}` does not look like a MAC address")

        for match in re.findall(STRICT_MAC_PATTERN, t):
            macs_to_replace.add(match)

        if not macs_to_replace:
            return t

        iter_fake_macs = self.generate_fake_mac_addresses()

        mac_old_to_new = {}
        for mac_old in macs_to_replace:
            # We don't want to overwrite correct MAC address
            mac_fake_new = next(iter_fake_macs)
            while mac_fake_new in macs_correct_normalized:
                mac_fake_new = next(iter_fake_macs)

            mac_new = self.format_mac(mac_fake_new, *self.detect_mac_format(mac_old))
            mac_old_to_new[mac_old] = mac_new

        for mac_old, mac_new in mac_old_to_new.items():
            t = t.replace(mac_old, mac_new)

        return t

    def process_file(self, path: Path):
        with path.open("rt") as file:
            raw = json.load(file)

        msg = raw["input"]["message"]
        old_msg = msg

        msg = self.replace_emails_and_usernames(raw, msg)
        msg = self.replace_urls(raw, msg)
        msg = self.replace_uuids(msg)
        msg = self.replace_hashes(msg)
        msg = self.replace_ips(msg)
        msg = self.replace_session_ids(msg)
        msg = self.replace_mac_addresses(raw, msg)

        raw["input"]["message"] = msg
        raw["expected"]["message"] = msg

        with path.open("wt") as file:
            json.dump(raw, file, indent=2)

        if old_msg != msg:
            logger.info(f"Processed {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool for test anonymization")
    parser.add_argument("path", nargs="+", help="File paths or directories")

    args = parser.parse_args()
    tests_to_process = gather_files(args.path)
    if not tests_to_process:
        logger.info("No files found")
        exit()

    anon = Anonymizer()
    for test_path in tests_to_process:
        anon.process_file(test_path)
