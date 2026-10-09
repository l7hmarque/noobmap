# Architecture Decision Records

Índice das decisões de arquitetura do **Scanner de Segurança para Redes de Clientes (Kali Live)**.
Formato: Michael Nygard (skill `architecture-decision-records`).

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [0001](0001-cli-on-kali-live-not-web-stack.md) | Plataforma é um CLI no Kali Live, não uma stack web | Accepted | 2026-10-08 |
| [0002](0002-nmap-as-scanning-engine.md) | Nmap como motor de varredura (não scanner próprio) | Accepted | 2026-10-08 |
| [0003](0003-non-destructive-advisory-only.md) | Ferramenta não destrutiva / apenas orientativa | Accepted | 2026-10-08 |
| [0004](0004-self-contained-offline-html-report.md) | Relatório em HTML offline self-contained (+ resumo no terminal) | Accepted | 2026-10-08 |
| [0005](0005-roe-authorization-gate.md) | Gate obrigatório de autorização (RoE) via `--autorizado` | Accepted | 2026-10-08 |

## Referências
- PRD: `.claude/prds/security-scan-and-fix.prd.md`
- Template em branco para uso manual: [template.md](template.md)
