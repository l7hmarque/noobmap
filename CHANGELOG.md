# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e
[Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

## [0.2.0] - 2026-10-09

### Adicionado
- Novas regras de gravidade e orientações de correção para mais serviços:
  rpcbind (111); r-services `rsh`/`rlogin`/`rexec` (512/513/514); Oracle (1521); NFS (2049);
  API do Docker (2375, Crítico); WinRM (5985); Redis (6379); painel HTTPS alternativo (8443);
  Jupyter (8888); Elasticsearch (9200); Memcached (11211); MongoDB (27017).
- `README.en.md`: documentação completa em inglês.

### Alterado
- README reorganizado com seletor de idioma (`README.md` em PT-BR, `README.en.md` em inglês).

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
