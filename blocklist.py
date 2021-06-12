#!/usr/bin/env python3
import os
import ipcalc
import logging
import requests
import time

from typing import List, Optional

OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.getcwd())

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("blocklist")

lists = {
    "net": {
        "cidr_report_bogons": "https://www.cidr-report.org/bogons/freespace-prefix.txt",
        "spamhaus_drop": "https://www.spamhaus.org/drop/drop.txt",
        "spamhaus_edrop": "https://www.spamhaus.org/drop/edrop.txt",
    },
    "ipv4": {
        "alienvault_reputation": "https://reputation.alienvault.com/reputation.generic",
        "bds_atif": "https://www.binarydefense.com/banlist.txt",
        "blocklist_de": "https://lists.blocklist.de/lists/all.txt",
        "bruteforceblocker": "http://danger.rulez.sk/projects/bruteforceblocker/blist.php",
        "ciarmy": "https://cinsscore.com/list/ci-badguys.txt",
        "cruzit_web_attacks": "https://iplists.firehol.org/files/cruzit_web_attacks.ipset",
        "et_compromised": "https://rules.emergingthreats.net/blockrules/compromised-ips.txt",
        "feodo": "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        "malc0de": "https://malc0de.com/bl/IP_Blacklist.txt",
        "nixspam": "https://iplists.firehol.org/files/nixspam.ipset",
        "sslbl": "https://sslbl.abuse.ch/blacklist/sslipblacklist.txt",
        "yoyo_adservers": "https://pgl.yoyo.org/adservers/iplist.php?ipformat=plain&showintro=0&mimetype=plaintext",
    },
    "other": {
        "dm_tor": "https://www.dan.me.uk/torlist/",
        "dshield": "https://feeds.dshield.org/block.txt",
    }
}


def parse_list(type: str, name: str, url: str) -> Optional[List[str]]:
    if type == "net":
        return parse_net_list(url)
    elif type == "ipv4":
        return parse_ipv4_list(url)
    elif type == "other":
        if name == "dm_tor":
            return parse_tor_list(url)
        elif name == "dshield":
            return parse_dshield_list(url)
        else:
            return None
    else:
        return None


def parse_net_list(url: str) -> List[str]:
    r = requests.get(url)
    r.raise_for_status()

    blocklist = []

    for line in r.text.splitlines():
        if not line or line.startswith(";") or line.startswith("#") or line.startswith("//"):
            continue

        ip_net = ipcalc.Network(line.split(maxsplit=1)[0])
        blocklist.append(f"{ip_net[0]}-{ip_net[-1]}")

    return blocklist


def parse_ipv4_list(url: str) -> List[str]:
    r = requests.get(url)
    r.raise_for_status()

    blocklist = []

    for line in r.text.splitlines():
        if not line or line.startswith(";") or line.startswith("#") or line.startswith("//"):
            continue

        ip_address = line.split(maxsplit=1)[0]
        blocklist.append(f"{ip_address}-{ip_address}")

    return blocklist


def parse_tor_list(url: str) -> List[str]:
    r = requests.get(url)
    r.raise_for_status()

    blocklist = []

    for line in r.text.splitlines():
        if not line or line.startswith("#") or ":" in line:
            continue

        ip_address = line.split(maxsplit=1)[0]
        blocklist.append(f"{ip_address}-{ip_address}")

    return blocklist


def parse_dshield_list(url: str) -> List[str]:
    r = requests.get(url)
    r.raise_for_status()

    blocklist = []

    for line in r.text.splitlines():
        if not line or line.startswith("#") or line.startswith("Start"):
            continue

        try:
            columns = line.split(maxsplit=3)
            ip_address = columns[0]
            mask = int(columns[2])
        except ValueError:
            continue

        ip_net = ipcalc.Network(ip_address, mask)
        blocklist.append(f"{ip_net[0]}-{ip_net[-1]}")

    return blocklist


def create_sources_file(output_dir: str = ""):
    sources = {}

    for group in lists.values():
        for name, url in group.items():
            sources[name] = url

    with open(os.path.join(output_dir, "sources.txt"), "w+") as f:
        f.write("The blocklist.p2p.gz file is built using the following free lists:\n\n")

        for name in sorted(sources.keys()):
            f.write(f" - {name}: {sources[name]}\n")

        f.write("\nThis list contains only data provided for FREE for non-commercial purposes, IBlocklist.com go away.\n")
        f.write("DShield.org Recommended Block List is licensed under CC BY-NC-SA 2.5\n")


def get_list_count() -> int:
    i = 0
    for group in lists.values():
        i += len(group.keys())

    return i


def main():
    logger.info(f"Building P2P blocklist file using {get_list_count()} lists")

    total = 0
    start_time = time.time()

    with open(os.path.join(OUTPUT_DIR, "blocklist.p2p"), "w+") as f:
        for type, group in lists.items():
            for name, url in group.items():
                logger.info(f"Downloading list {name}: {url}")

                try:
                    parsed_list = parse_list(type, name, url)
                except Exception as e:
                    logger.error("Failed to download list: " + str(e))
                    continue

                logger.info(f"Adding {len(parsed_list)} entries to blocklist file...")

                for entry in parsed_list:
                    f.write(f"{name}:{entry}\n")

                total += len(parsed_list)

    logger.info("Creating sources.txt with list refrences and authors")

    try:
        create_sources_file(OUTPUT_DIR)
    except IOError as e:
        logger.error("Failed to create file: " + str(e))

    logger.info(f"Done! Added {total} entries in {round(time.time() - start_time, 2)} seconds.")


if __name__ == "__main__":
    main()
