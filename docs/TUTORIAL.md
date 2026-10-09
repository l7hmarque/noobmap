# Tutorial do noobmap — do zero à rede protegida

> Este guia assume que você **nunca usou Linux** e **nunca fez uma varredura de rede**.
> Siga na ordem, sem pular etapas. Em cada passo dizemos **o que vai acontecer**.

---

## 0. O que você vai precisar

- Um **pendrive** de **8 GB ou mais** (os arquivos dele serão apagados).
- Um **computador** onde você possa dar boot pelo pendrive (o seu notebook serve).
- O **noobmap** (o pacote `noobmap-<versão>.zip`) — veja o passo 6.
- **Autorização** de quem é responsável pela rede (cliente, empresa, sua casa).

> ⚠️ **Regra de ouro:** só escaneie redes **que são suas** ou para as quais você tem
> **autorização escrita**. O noobmap **não roda** sem você confirmar isso.

---

## 1. Baixar o Kali Live

O Kali Live é um "Linux de pendrive": roda sem instalar nada no computador.

1. Acesse **https://www.kali.org/get-kali/**.
2. Escolha **"Live Boot"** (a opção de rodar a partir de um pendrive).
3. Baixe o arquivo **`.iso`** (alguns GB — pode demorar).

---

## 2. Gravar o Kali no pendrive

1. Baixe um gravador de ISO:
   - **Windows:** [Rufus](https://rufus.ie/)
   - **Qualquer sistema:** [balenaEtcher](https://etcher.balena.io/)
2. No gravador, selecione:
   - a **imagem** = o arquivo `.iso` do Kali que você baixou;
   - o **destino** = o **pendrive** (confira que é o pendrive certo!).
3. Clique em **gravar**. Isso **apaga tudo** do pendrive.
4. Espere terminar e ejete com segurança.

---

## 3. Dar boot pelo pendrive

1. Com o pendrive ligado, **ligue/reinicie** o computador.
2. Aperte a **tecla de boot** logo no começo (aparece na tela de abertura). Comuns:
   `F12`, `F2`, `F10`, `DEL` ou `ESC`.
3. Escolha o **pendrive** na lista de boot.
4. Se o computador não aceitar o pendrive, entre na **BIOS/UEFI** e:
   - **desative o "Secure Boot"**; e/ou
   - coloque o **USB** como primeiro na ordem de boot.
5. Na tela do Kali, escolha **"Live system (amd64)"**.
   - **Não** escolha "Install" nem "Graphical install".
6. Em alguns segundos você chega na **área de trabalho do Kali**. Isso está rodando do
   pendrive — **nada** foi instalado no computador.

---

## 4. Conectar à rede do cliente

1. Conecte o computador à rede que será avaliada: **cabo de rede** ou **wi-fi** do local.
2. Abra o **Terminal** (ícone perto do menu, ou `Ctrl+Alt+T`).

---

## 5. Descobrir "qual é a rede"

Você precisa do **endereço da rede** no formato `192.168.1.0/24`.

- No **próprio noobmap**, se você não souber, pode olhar no roteador: entre no painel
  dele pelo navegador (endereço comum: `192.168.0.1` ou `192.168.1.1`) e veja a **LAN**.
- Ou no terminal do Kali:

  ```bash
  ip route
  ```

  Procure algo como `192.168.1.0/24`. O número antes de `/24` é o endereço da sua rede.

> O noobmap só aceita **redes privadas** (`10.x`, `172.16–31.x`, `192.168.x`) e no máximo
> **/24** (até 254 aparelhos). Redes públicas são recusadas.

---

## 6. Ter o noobmap no pendrive

Baixe o pacote de release **`noobmap-<versão>.zip`** (na página *Releases* do repositório,
ou do arquivo que você recebeu).

Copie o `.zip` para o **pendrive** (ou para a Área de Trabalho do Kali). Depois, no
terminal do Kali:

```bash
cd ~/Desktop          # ou onde estiver o arquivo
unzip noobmap-*.zip
cd noobmap-*
chmod +x noobmap
./noobmap --version    # deve mostrar "noobmap <versão>"
```

---

## 7. Autorizar (obrigatório)

1. Abra e **imprima** o termo: `docs/roe/termo-de-autorizacao.md`.
2. O responsável pela rede **assina** (ou aceita por escrito/e-mail).
3. Guarde uma via junto ao relatório.

Sem isso, o next passo **aborta** — é a sua proteção legal.

---

## 8. Rodar a varredura

Troque pelo **nome do cliente** e pela **rede** correta:

```bash
./noobmap scan --autorizado --cliente "Mercado do Zé" --rede 192.168.1.0/24
```

O que vai acontecer:

1. Ele registra a autorização (nome + data/hora).
2. Roda o Nmap de forma **não invasiva** (a tela mostra o progresso).
3. Ao final, mostra um **resumo** e gera o **relatório**.

Cuidados:
- **Não desligue** o pendrive nem o terminal durante o processo.
- Se der `Ctrl+C`, nada é gerado (sem relatório pela metade).

---

## 9. Ler o relatório

Os arquivos ficam em `noobmap-out/<cliente>/<data>/`:

- **`relatorio.html`** — abra no navegador. É o documento do cliente.
- `nmap_bruto.xml` — dado técnico (guarde).
- `autorizacao.json` — prova de autorização.

No relatório, os riscos vêm por **gravidade**: **Crítico → Alto → Médio → Baixo → Informativo**.
Cada item tem **"Como corrigir"** com: **onde ir**, **o que mudar** e **o que NÃO mexer**.

---

## 10. Aplicar as correções (com cuidado)

1. **Antes de qualquer mudança:** abra o painel do roteador e **salve/exporte a
   configuração atual** (backup). Todo passo de correção lembra disso.
2. Faça **uma mudança por vez**, exatamente como o relatório orienta.
3. Depois de cada mudança, **teste** se a internet e os aparelhos continuam funcionando.
4. Se algo quebrar: **restaure o backup** e reinicie o roteador.
5. Na dúvida, **pare** — o relatório também avisa sobre **falsos positivos**.

> O noobmap **nunca** aplica mudanças. Você é quem mexe. Ele só diz o caminho.

---

## 11. Re-scan para confirmar

Rode de novo para ver se a rede ficou mais limpa:

```bash
./noobmap scan --autorizado --cliente "Mercado do Zé" --rede 192.168.1.0/24
```

Compare o **antes** e o **depois**. O ideal é **zero achados Crítico/Alto** em aberto.

---

## 12. Entregar e guardar

- **Copie a pasta do cliente para o pendrive** (o Kali Live não guarda os arquivos ao
  desligar).
- Entregue o `relatorio.html` ao cliente (imprima ou envie).
- **Desligue o Kali** pelo menu (ou `sudo poweroff`) e remova o pendrive.

---

## Problemas comuns

| Situação | O que fazer |
|---|---|
| "nmap não encontrado" | Você não está no Kali Live. Rode dentro do Kali. |
| "Varredura bloqueada: é obrigatória autorização" | Falta `--autorizado` (e o termo assinado). |
| "Apenas redes privadas…" | Use a rede interna do cliente (`192.168.x.0/24`), não um IP público. |
| "Rede grande demais" | Use no máximo `/24`. |
| Não achei minha rede | Veja o passo 5 (`ip route` ou painel do roteador). |

Pronto! Você fez uma avaliação de segurança de rede do começo ao fim. 🎉
