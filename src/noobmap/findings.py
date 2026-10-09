import xml.etree.ElementTree as ET

SEVERITIES = ["Critico", "Alto", "Medio", "Baixo", "Informativo"]
SEVERITY_RANK = {"Critico": 0, "Alto": 1, "Medio": 2, "Baixo": 3, "Informativo": 4}
SEVERITY_LABEL = {
    "Critico": "Crítico",
    "Alto": "Alto",
    "Medio": "Médio",
    "Baixo": "Baixo",
    "Informativo": "Informativo",
}

PORT_RULES = {
    21: ("servico-ftp", "Alto", "FTP (transferência de arquivos) exposto"),
    22: ("servico-ssh", "Baixo", "Acesso remoto por SSH exposto"),
    23: ("servico-telnet", "Critico", "Telnet exposto — tudo trafega sem criptografia"),
    25: ("servico-smtp", "Medio", "Servidor de e-mail SMTP exposto"),
    53: ("servico-dns", "Baixo", "Servidor DNS exposto"),
    80: ("servico-http", "Informativo", "Site HTTP exposto (sem HTTPS)"),
    110: ("servico-pop3", "Medio", "E-mail POP3 exposto"),
    135: ("servico-rpc", "Alto", "Serviço RPC do Windows exposto"),
    139: ("servico-netbios", "Alto", "NetBIOS do Windows exposto"),
    143: ("servico-imap", "Medio", "E-mail IMAP exposto"),
    443: ("servico-https", "Informativo", "Site HTTPS exposto"),
    445: ("servico-smb", "Alto", "Compartilhamento de arquivos SMB exposto"),
    1433: ("servico-mssql", "Alto", "Banco de dados SQL Server exposto"),
    3306: ("servico-mysql", "Alto", "Banco de dados MySQL exposto"),
    3389: ("servico-rdp", "Alto", "Área de trabalho remota (RDP) exposta"),
    5432: ("servico-postgres", "Alto", "Banco de dados PostgreSQL exposto"),
    5900: ("servico-vnc", "Alto", "Acesso remoto por VNC exposto"),
    8080: ("servico-http-alt", "Medio", "Site/painel HTTP alternativo exposto"),
}

SERVICE_RULES = {
    "telnet": PORT_RULES[23],
    "ftp": PORT_RULES[21],
    "ssh": PORT_RULES[22],
    "http": PORT_RULES[80],
    "https": PORT_RULES[443],
    "http-alt": PORT_RULES[8080],
    "microsoft-ds": PORT_RULES[445],
    "netbios-ssn": PORT_RULES[139],
    "msrpc": PORT_RULES[135],
    "ms-wbt-server": PORT_RULES[3389],
    "mssql": PORT_RULES[1433],
    "ms-sql-s": PORT_RULES[1433],
    "mysql": PORT_RULES[3306],
    "postgresql": PORT_RULES[5432],
    "vnc": PORT_RULES[5900],
    "domain": PORT_RULES[53],
    "smtp": PORT_RULES[25],
}

DEFAULT_RULE = (
    "precisa-verificacao",
    "Informativo",
    "Serviço desconhecido — precisa de verificação manual",
)


def _rule_for(porta, servico):
    if porta in PORT_RULES:
        return PORT_RULES[porta]
    if servico and servico.lower() in SERVICE_RULES:
        return SERVICE_RULES[servico.lower()]
    return DEFAULT_RULE


def parse_nmap_xml(xml_text):
    if "<!DOCTYPE" in xml_text or "<!ENTITY" in xml_text:
        raise ValueError("XML com DOCTYPE/ENTITY não é permitido.")
    root = ET.fromstring(xml_text)
    findings = []
    for host in root.iter("host"):
        status = host.find("status")
        if status is not None and status.get("state") != "up":
            continue
        address = host.find("address")
        host_addr = address.get("addr") if address is not None else "?"
        ports = host.find("ports")
        if ports is None:
            continue
        for port in ports.findall("port"):
            state = port.find("state")
            if state is None or state.get("state") != "open":
                continue
            porta = int(port.get("portid"))
            service = port.find("service")
            servico = service.get("name") if service is not None else ""
            chave, severidade, descricao = _rule_for(porta, servico)
            findings.append(
                {
                    "host": host_addr,
                    "porta": porta,
                    "protocolo": port.get("protocol", "tcp"),
                    "servico": servico or "desconhecido",
                    "chave": chave,
                    "severidade": severidade,
                    "descricao": descricao,
                }
            )
    findings.sort(key=lambda f: (SEVERITY_RANK[f["severidade"]], f["host"], f["porta"]))
    return findings
