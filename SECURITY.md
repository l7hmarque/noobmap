# Política de Segurança

## Uso responsável

O **noobmap** é uma ferramenta **defensiva**, de uso **autorizado**. Ele:
- só aceita **redes privadas** (`10.x`, `172.16–31.x`, `192.168.x`) e no máximo `/24`;
- **exige** confirmação de autorização escrita (termo RoE) e **falha-fechado** sem ela;
- é **advisory-only**: **nunca** explora falhas nem altera a rede.

**É ilegal** usar esta ferramenta para escanear redes sem autorização. A responsabilidade
pelo uso é inteiramente de quem opera a ferramenta.

## Reportando uma vulnerabilidade

Se você encontrou uma falha **no noobmap** (por exemplo, uma forma de burlar o gate de
autorização, um caminho não-intencional de escrita, ou execução de código), **não** abra
uma issue pública.

Use o canal privado do GitHub:
1. Abra a aba **Security** deste repositório.
2. Clique em **Report a vulnerability** (Relatar uma vulnerabilidade).
3. Descreva o problema e o impacto, com passos para reproduzir e a versão do noobmap.

Isso abre uma conversa **privada** com o mantenedor. Se a opção não estiver disponível,
abra uma issue **sem detalhes sensíveis** pedindo um contato privado.

Vulnerabilidades corrigidas serão documentadas no `CHANGELOG.md`.

## Escopo

Dentro do escopo:
- o código em `src/noobmap/` e os scripts de build/checagem.

Fora do escopo:
- o **Nmap** em si (reporte ao projeto Nmap);
- o **Kali Linux**;
- uso indevido por parte de terceiros.
