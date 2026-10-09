# Como usar (guia rápido, passo a passo)

Ferramenta de varredura de segurança das redes dos seus clientes. Roda no **Kali Live
(pendrive)**, sem instalar nada, e **nunca altera** o roteador ou a rede do cliente.

## Antes de tudo: autorização (obrigatória)

1. Abra `docs/roe/termo-de-autorizacao.md`, imprima e faça o **cliente assinar**.
   (Sem isso, a ferramenta **não roda** — é sua proteção legal.)
2. Guie a varredura apenas na rede do cliente que assinou.

## Ligar o Kali e abrir o terminal

1. Dê boot pelo pendrive do Kali (não precisa instalar).
2. Abra o **Terminal**.

## Descobrir a rede do cliente

1. No painel do roteador do cliente (ou no seu celular conectado ao wi-fi dele), veja o
   endereço da rede. Costuma ser algo como `192.168.1.0/24` ou `192.168.0.0/24`.
2. A ferramenta só aceita **redes privadas** e **no máximo /24 (254 aparelhos)**.

## Rodar a varredura

Digite (trocando pelo nome do cliente e pela rede dele):

```
noobmap scan --autorizado --cliente "Nome do Cliente" --rede 192.168.1.0/24
```

O que acontece:

1. Ela registra a autorização (nome do cliente + data/hora).
2. Roda o Nmap de forma **não invasiva** (sem explorar nada).
3. Cria um **relatório** e mostra um resumo no terminal.

## Onde ficam os arquivos

Na pasta `noobmap-out/Nome-do-Cliente/AAAA-MM-DD/`:

- `relatorio.html` — **abra no navegador**. É o documento para o cliente.
- `nmap_bruto.xml` — dado técnico (guarde, não precisa entender).
- `autorizacao.json` — prova de que havia autorização.

> Dica: salve a pasta num **pendrive** para não perder o relatório quando desligar o Kali.

## Entender o relatório

- Os riscos vêm por gravidade: **Crítico → Alto → Médio → Baixo → Informativo**.
- Cada item tem "Como corrigir", com **onde ir**, **o que mudar** e o que **não mexer**.
- Faça **backup** da configuração do roteador antes de mudar qualquer coisa.
- Na dúvida, **pare** e não altere — o relatório também avisa sobre falsos positivos.

## Preciso de ajuda?

```
noobmap --help
noobmap scan --help
noobmap --version
```
