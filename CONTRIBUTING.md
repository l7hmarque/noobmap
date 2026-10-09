# Contribuindo com o noobmap

Obrigado pelo interesse! 🎉 Este projeto quer manter a **segurança de rede acessível a
qualquer pessoa**. Contribuições são muito bem-vindas.

## Formas de ajudar

- **Orientações de correção para modelos de roteador específicos** (Mikrotik, TP-Link,
  Intelbras, Ubiquiti, Asus, etc.). O arquivo `src/noobmap/remediation.py` já tem um
  "espaço de extensão" genérico — adicione entradas específicas.
- **Novas regras de gravidade** para serviços/portas (em `src/noobmap/findings.py`).
- **Traduções** de documentação e mensagens.
- **Correções de bugs** e melhoria de testes.

## Regras do projeto

- **Não-destrutivo.** O noobmap **nunca** altera a rede. Nada de exploração ativa,
  força bruta ou `--script` do Nmap.
- **Falha-fechado.** Nunca publique código que permita uma varredura **sem** o gate de
  autorização.
- **Só redes privadas.** Mantenha a validação que recusa faixas públicas e redes > `/24`.
- **Sem segredos.** Não commite chaves, senhas ou dados reais de clientes.

## Ambiente de desenvolvimento

Requisitos: **Python 3.9+** e (opcional, para varredura real) **Nmap**.

```bash
git clone https://github.com/l7hmarque/noobmap
cd noobmap

# rodar os testes (sem dependências externas: só a stdlib)
PYTHONPATH=src python -m unittest discover -s tests

# rodar a ferramenta localmente
PYTHONPATH=src python -m noobmap --version
```

## Fluxo de contribuição

1. Abra uma **issue** descrevendo o que você quer mudar (ou pegue uma existente).
2. Crie um **branch**: `git checkout -b feat/minha-melhoria`.
3. **Escreva o teste primeiro** (usamos `unittest`; veja `tests/`).
4. Implemente a mudança mínima para o teste passar.
5. Garanta que **tudo passa**: `PYTHONPATH=src python -m unittest discover -s tests`.
6. Abra um **Pull Request** explicando o "porquê" (não só o "o quê").

## Estilo

- Python simples, stdlib only (nenhuma dependência externa).
- Mensagens ao usuário em **português, linguagem simples** (o público é leigo).
- Mantenha o relatório **offline** (sem assets externos) e **escapando** os dados.

## Código de conduta

Seja gentil, paciente e didático. O público deste projeto inclui pessoas **começando agora**.
