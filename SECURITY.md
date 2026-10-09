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

Envie um e-mail para o mantenedor (veja a aba Security).
- descrição do problema e impacto;
- passos para reproduzir;
- versão do noobmap.

Você receberá um retorno assim que possível. Vulnerabilidades corrigidas serão
documentadas no `CHANGELOG.md`.

## Escopo

Dentro do escopo:
- o código em `src/noobmap/` e os scripts de build/checagem.

Fora do escopo:
- o **Nmap** em si (reporte ao projeto Nmap);
- o **Kali Linux**;
- uso indevido por parte de terceiros.
