# ADR-0002: Nmap como motor de varredura (não um scanner próprio)

**Date**: 2026-10-08
**Status**: Accepted
**Deciders**: Architect (revisão do PRD `security-scan-and-fix`)

## Context

O produto precisa descobrir hosts, portas e serviços em uma **rede pequena (≤254 hosts)** e traduzir
isso em achados interpretáveis por um leigo. Reimplementar descoberta de rede é arriscado, e o
ambiente-alvo (**Kali Live**) já traz ferramentas de varredura consolidadas instaladas. O PRD
(Technical Decisions, linha 41) define **Nmap** como motor.

## Decision

Usar o **Nmap**, já presente no Kali Live, como motor de varredura, invocado pelo script. O script
apenas orquestra o Nmap e interpreta sua saída — não faz descoberta de rede própria.

## Alternatives Considered

### Alternative 1: Scanner próprio (sockets / pacotes raw)
- **Pros**: controle total do formato de saída; zero dependência externa.
- **Cons**: reinventar a roda; risco de bugs, falsos negativos/positivos e invalidação dos achados;
  alto custo de manutenção e validação.
- **Why not**: Nmap é padrão de facto, testado por décadas, e já está no Kali — reimplementar não
  agrega valor e aumenta o risco de um relatório incorreto para o cliente.

### Alternative 2: Outra ferramenta (masscan, zmap, nbtscan)
- **Pros**: masscan/zmap são muito rápidos em grandes escalas.
- **Cons**: otimizados para escala/velocidade e potencialmente agressivos — risco de degradar a rede
  do cliente; menos adequados a uma rede pequena; cobertura de detecção de serviço/versão inferior.
- **Why not**: o alvo é rede pequena e um operador leigo; Nmap equilibra descoberta, portas e
  serviços com cadência controlável, e já vem instalado (**AC2**).

## Consequences

### Positive
- Detecção confiável e reconhecida (hosts, portas, serviços/versões) para ≤254 hosts.
- Zero instalação adicional — alinha com **AC2** (roda no Kali Live sem setup).
- Comunidade e documentação amplas reduzem esforço de manutenção.

### Negative
- Dependência do Nmap e de sua versão presentes no Kali Live.
- Exige parsing estável da saída (ex.: XML) para alimentar o relatório.

### Risks
- **Risco**: varredura agressiva pode impactar a rede/dispositivos.
  **Mitigação**: usar perfis/timing conservadores por padrão e nunca habilitar exploração (fora de
  escopo), reforçando **ADR-0003 (não destrutivo)**.
