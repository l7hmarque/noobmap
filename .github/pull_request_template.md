## O que muda

<!-- Descreva a mudança e o "porquê". -->

## Como testar

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Checklist

- [ ] Os testes passam (`PYTHONPATH=src python -m unittest discover -s tests`)
- [ ] Mantém o comportamento **não-destrutivo** (o noobmap nunca altera a rede)
- [ ] Mantém o **gate de autorização** falha-fechado
- [ ] Só aceita **redes privadas** (≤ `/24`)
- [ ] Nenhum **segredo** ou dado real de cliente incluído
