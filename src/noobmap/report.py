import html

from . import remediation as remediation_mod
from .findings import SEVERITIES, SEVERITY_LABEL

GLOSSARY = [
    ("Porta", "uma 'janela' pela qual um programa aceita conexões. Porta aberta = algo escutando."),
    ("Serviço", "o programa que responde naquela porta (ex.: site, banco de dados, acesso remoto)."),
    ("Firmware", "o 'sistema' interno do roteador; mantenha atualizado para corrigir falhas."),
    ("Port forwarding", "regra que 'abre' uma porta de fora para um aparelho de dentro. Evite quando não precisar."),
    ("VPN", "túnel seguro para acesso remoto, mais seguro que expor portas na internet."),
]

STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; margin: 0; color: #1a1a1a; background: #f5f6f8; }
header { background: #ffffff; padding: 24px 32px; border-bottom: 4px solid #0b5; }
h1 { margin: 0 0 4px; font-size: 22px; }
h2 { margin-top: 32px; border-bottom: 1px solid #ddd; padding-bottom: 6px; }
main { max-width: 900px; margin: 0 auto; background: #fff; padding: 24px 32px 48px; }
.meta { color: #555; font-size: 13px; }
.finding { border: 1px solid #e0e0e0; border-left-width: 6px; border-radius: 6px; padding: 12px 16px; margin: 12px 0; }
.sev-Critico { border-left-color: #c0392b; }
.sev-Alto { border-left-color: #e67e22; }
.sev-Medio { border-left-color: #f1c40f; }
.sev-Baixo { border-left-color: #3498db; }
.sev-Informativo { border-left-color: #95a5a6; }
.tag { font-size: 12px; font-weight: bold; padding: 2px 8px; border-radius: 10px; background: #eee; }
.finding h3 { margin: 0 0 6px; font-size: 15px; }
.desc { margin: 0 0 8px; color: #333; }
details { margin-top: 6px; }
summary { cursor: pointer; font-weight: bold; }
ol { margin: 8px 0; padding-left: 22px; }
ol li { margin: 4px 0; }
.notice { background: #fff8e1; border: 1px solid #ffe082; padding: 12px 16px; border-radius: 6px; }
.empty { color: #2e7d32; font-weight: bold; }
footer { max-width: 900px; margin: 0 auto; padding: 16px 32px; color: #666; font-size: 12px; }
@media print { body { background: #fff; } main { padding: 0; } }
"""


def _finding_article(finding):
    rem = remediation_mod.get(finding["chave"])
    passos = "".join("<li>{}</li>".format(html.escape(p)) for p in rem["passos"])
    return (
        '<article class="finding sev-{sev}">\n'
        "  <h3>{host} &mdash; porta {porta}/{proto} ({servico}) "
        '<span class="tag">{sevlabel}</span></h3>\n'
        '  <p class="desc">{desc}</p>\n'
        "  <details>\n"
        "    <summary>Como corrigir: {titulo}</summary>\n"
        "    <p><strong>Onde ir:</strong> {onde_ir}</p>\n"
        "    <ol>{passos}</ol>\n"
        "    <p><strong>Backup antes:</strong> {backup}</p>\n"
        "    <p><strong>Como desfazer:</strong> {desfazer}</p>\n"
        "    <p><strong>O que NÃO mexer:</strong> {nao_mexer}</p>\n"
        "  </details>\n"
        "</article>"
    ).format(
        sev=finding["severidade"],
        host=html.escape(str(finding["host"])),
        porta=finding["porta"],
        proto=html.escape(str(finding["protocolo"])),
        servico=html.escape(str(finding["servico"])),
        sevlabel=SEVERITY_LABEL.get(finding["severidade"], finding["severidade"]),
        desc=html.escape(str(finding["descricao"])),
        titulo=html.escape(rem["titulo"]),
        onde_ir=html.escape(rem["onde_ir"]),
        passos=passos,
        backup=html.escape(rem["backup"]),
        desfazer=html.escape(rem["desfazer"]),
        nao_mexer=html.escape(rem["nao_mexer"]),
    )


def _normalize(findings):
    result = []
    for f in findings:
        if f.get("severidade") not in SEVERITIES:
            f = dict(f, severidade="Informativo")
        result.append(f)
    return result


def render_html(cliente, quando, rede, findings):
    findings = _normalize(findings)
    sections = []
    for severidade in SEVERITIES:
        group = [f for f in findings if f["severidade"] == severidade]
        if not group:
            continue
        label = SEVERITY_LABEL[severidade]
        sections.append("<h2>{label} ({n})</h2>".format(label=label, n=len(group)))
        sections.append("\n".join(_finding_article(f) for f in group))
    if not sections:
        sections.append('<p class="empty">Nenhum risco encontrado. Rede sem portas abertas detectadas.</p>')
    gloss = "".join(
        "<li><strong>{}</strong> — {}</li>".format(html.escape(t), html.escape(d))
        for t, d in GLOSSARY
    )
    return (
        "<!doctype html>\n"
        '<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Relatório de Segurança — {cliente}</title>\n"
        "<style>{style}</style>\n</head>\n<body>\n"
        "<header>\n<h1>Relatório de Segurança da Rede</h1>\n"
        '<p class="meta">Cliente: {cliente} &middot; Rede: {rede} &middot; Data: {quando}</p>\n'
        "</header>\n<main>\n"
        '<p class="notice">{disclaimer}</p>\n'
        "{sections}\n"
        "<h2>Glossário (termos explicados)</h2>\n<ul>{gloss}</ul>\n"
        "<h2>Aviso sobre falsos positivos</h2>\n"
        "<p>Uma porta aberta nem sempre é uma falha: pode ser um serviço necessário. "
        "Este relatório é um roteiro para conversar, não uma acusação. Na dúvida, não altere "
        "nada e confirme o que aquele serviço faz.</p>\n"
        "</main>\n<footer>Gerado por noobmap — ferramenta de varredura orientativa. "
        "Nenhuma alteração é aplicada automaticamente.</footer>\n</body>\n</html>\n"
    ).format(
        cliente=html.escape(str(cliente)),
        rede=html.escape(str(rede)),
        quando=html.escape(str(quando)),
        style=STYLE,
        disclaimer=html.escape(remediation_mod.DISCLAIMER),
        sections="\n".join(sections),
        gloss=gloss,
    )


def terminal_summary(findings, report_path):
    findings = _normalize(findings)
    counts = {s: 0 for s in SEVERITIES}
    for f in findings:
        counts[f["severidade"]] = counts.get(f["severidade"], 0) + 1
    lines = ["Resumo da varredura:"]
    for s in SEVERITIES:
        lines.append("  {label}: {n}".format(label=SEVERITY_LABEL[s], n=counts[s]))
    top = [f for f in findings if f["severidade"] in ("Critico", "Alto")][:3]
    if top:
        lines.append("Prioridade (corrija primeiro):")
        for f in top:
            lines.append(
                "  - {host}:{porta} — {desc}".format(
                    host=f["host"], porta=f["porta"], desc=f["descricao"]
                )
            )
    lines.append("Relatório completo: {p}".format(p=report_path))
    return "\n".join(lines)
