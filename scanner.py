import ipaddress
import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def ping_host(ip_address):
    system_name = platform.system().lower()

    if system_name == "windows":
        command = ["ping", "-n", "1", "-w", "800", str(ip_address)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip_address)]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def get_hostname(ip_address):
    try:
        return socket.gethostbyaddr(str(ip_address))[0]
    except Exception:
        return "Unknown"


def get_mac_address(ip_address):
    try:
        system_name = platform.system().lower()

        if system_name == "windows":
            output = subprocess.check_output(["arp", "-a", str(ip_address)], text=True)
        else:
            output = subprocess.check_output(["arp", "-n", str(ip_address)], text=True)

        for line in output.splitlines():
            if str(ip_address) in line:
                parts = line.split()
                for part in parts:
                    if "-" in part or ":" in part:
                        if len(part) >= 17:
                            return part

        return "Unknown"
    except Exception:
        return "Unknown"


def scan_single_host(ip_address):
    is_online = ping_host(ip_address)

    if is_online:
        return {
            "ip": str(ip_address),
            "status": "Online",
            "hostname": get_hostname(ip_address),
            "mac": get_mac_address(ip_address)
        }

    return None


def scan_network(network_range, max_workers=50):
    results = []

    try:
        network = ipaddress.ip_network(network_range, strict=False)
    except ValueError:
        raise ValueError("Invalid network range. Example: 192.168.1.0/24")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = {
            executor.submit(scan_single_host, ip): ip
            for ip in network.hosts()
        }

        for future in as_completed(future_tasks):
            result = future.result()
            if result:
                results.append(result)

    results.sort(key=lambda item: tuple(map(int, item["ip"].split("."))))
    return results