import ipaddress
import shutil
import subprocess

NMAP_BINARY = "nmap"
SAFE_SCAN_ARGS = ["-sV", "-T3", "--top-ports", "100", "-Pn"]
MAX_PREFIX = 24
PRIVATE_RANGES = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
)


class ScanError(Exception):
    pass


def validate_target(rede):
    try:
        net = ipaddress.ip_network(str(rede).strip(), strict=False)
    except ValueError as exc:
        raise ScanError(
            'Rede inválida: "{rede}". Use o formato CIDR, ex.: 192.168.1.0/24'.format(
                rede=rede
            )
        ) from exc
    if net.version != 4:
        raise ScanError("Apenas redes IPv4 são suportadas.")
    if net.prefixlen < MAX_PREFIX:
        raise ScanError(
            "Rede grande demais ({n} hosts). O limite é /24 (até 254 hosts).".format(
                n=net.num_addresses
            )
        )
    if not any(net.subnet_of(r) for r in PRIVATE_RANGES):
        raise ScanError(
            "Apenas redes privadas LAN (10.x / 172.16-31.x / 192.168.x) são permitidas."
        )
    return str(net)


def build_command(rede, xml_path):
    return [NMAP_BINARY, *SAFE_SCAN_ARGS, "-oX", str(xml_path), rede]


def ensure_nmap():
    path = shutil.which(NMAP_BINARY)
    if path is None:
        raise ScanError(
            "nmap não encontrado. Rode a ferramenta no Kali Live, onde o nmap já vem instalado."
        )
    return path


def run_scan(rede, xml_path, timeout=900):
    binary = ensure_nmap()
    cmd = build_command(rede, xml_path)
    cmd[0] = binary
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise ScanError("A varredura demorou demais e foi interrompida.") from exc
    return cmd, proc
