# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e
[Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

## [0.1.0] - 2026-10-08

### Adicionado
- Primeira versão pública.
- Varredura guiada com **Nmap** (não invasiva, sem scripts de exploração).
- **Gate de autorização (RoE)** falha-fechado: sem `--autorizado`, a varredura aborta.
- Classificação de achados por **gravidade** (Crítico → Informativo) para ~16 serviços comuns.
- **Relatório HTML offline** em linguagem simples, com passo a passo de correção.
- Resumo no terminal com contagens e prioridades.
- Saída organizada por **cliente/data**, com permissões restritas (0700/0600).
- Validação de alvo (apenas redes privadas, no máximo `/24`).
- Empacotamento (`scripts/build_release.py`) e checagens de saúde (`scripts/canary.py`, `scripts/audit.py`).
- Documentação: tutorial (PT-BR/EN), FAQ, termo de autorização e diagramas.
