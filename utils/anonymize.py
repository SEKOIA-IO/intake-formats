import argparse
import json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from checks.validators.anonymization import ACCEPTED_DOMAINS, ACCEPTED_USERNAMES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger(__name__)


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


def replace_uuids(t: str):
    re_uuid = (
        "[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}"
    )
    all_uuids = set(re.findall(re_uuid, t))

    uuid_to_replace = {}

    for uuid_old, uuid_new in zip(all_uuids, generate_fake_uuids()):
        uuid_to_replace[uuid_old] = uuid_new

    for uuid_old, uuid_new in uuid_to_replace.items():
        logger.warning(f"Will replace {uuid_old} with {uuid_new}")
        t = t.replace(uuid_old, uuid_new)

    return t


def replace_hash(t: str, ln: int, c: str):
    re_hash = '"([0-9A-Fa-f]{%d})"' % ln
    all_hashes = set(re.findall(re_hash, t))

    hash_to_new = {}
    for hash in all_hashes:
        hash_to_new[hash] = c

    for hash_old, hash_new in hash_to_new.items():
        logger.warning(f"Will replace {hash_old} with {hash_new}")
        t = t.replace(hash_old, hash_new)

    return t


def replace_hashes(t: str):
    # these are hashes from anonymization checker
    t = replace_hash(
        t,
        128,
        "be688838ca8686e5c90689bf2ab585cef1137c999b48c70b92f67a5c34dc15697b5d11c982ed6d71be1e1e7f7b4e0733884aa97c3f7a339a8ed03577cf74be09",
    )  # sha-512
    t = replace_hash(
        t, 64, "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b"
    )  # sha-256
    t = replace_hash(t, 40, "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc")  # sha-1
    t = replace_hash(t, 32, "68b329da9893e34099c7d8ad5cb9c940")  # md5
    return t


def replace_ips(t: str):
    re_ips = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    all_ips = set(re.findall(re_ips, t))

    # hacks
    chrome_versions = set(re.findall(r"Chrome/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", t))
    mozilla_versions = set(re.findall(r"rv:([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", t))

    all_ips = all_ips - chrome_versions - mozilla_versions

    ip_to_new = {}
    unique_ips = set()
    for ip in all_ips:
        if ip in ("127.0.0.1",):
            continue

        unique_ips.add(ip)

    n = 1
    for ip in unique_ips:
        tmp = [str(n)] * 4
        new_ip = ".".join(tmp)
        ip_to_new[ip] = new_ip

        n += 1

    for ip_old, ip_new in ip_to_new.items():
        logger.warning(f"Will replace {ip_old} with {ip_new}")
        t = t.replace(ip_old, ip_new)

    return t


def replace_emails_and_usernames(text: str) -> str:
    re_email = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    all_emails = set(re.findall(re_email, text))

    email_mapping = {}
    usernames_to_replace = set()
    username_mapping = {}

    for email in all_emails:
        username, domain = email.split("@")

        # First, we have to check email's address domain
        for pattern in ACCEPTED_DOMAINS:
            if re.match(pattern, domain, re.IGNORECASE):
                break

        else:
            # no break
            email_mapping[email] = f"{username}@example.com"

        # Then check username as well
        for pattern in ACCEPTED_USERNAMES:
            if re.match(pattern, username, re.IGNORECASE):
                break

        else:
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


def replace_urls(text: str) -> str:
    re_url = r"(?:http|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"

    all_urls = set(re.findall(re_url, text))
    url_mapping = {}

    if all_urls:
        for url in all_urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            for pattern in ACCEPTED_DOMAINS:
                if re.match(pattern, domain, re.IGNORECASE):
                    break

            else:
                new_domain = "example.com"
                updated_url = parsed_url._replace(netloc=new_domain)
                url_mapping[url] = urlunparse(updated_url)

    for url_from, url_to in url_mapping.items():
        logger.warning(f"Replacing {url_from} with {url_to}")
        text = text.replace(url_from, url_to)

    return text


def process_file(path: Path):
    with path.open("rt") as file:
        raw = json.load(file)

    msg = raw["input"]["message"]
    old_msg = msg

    msg = replace_emails_and_usernames(msg)
    msg = replace_urls(msg)
    msg = replace_uuids(msg)
    msg = replace_hashes(msg)
    msg = replace_ips(msg)

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

    for test_path in tests_to_process:
        process_file(test_path)
