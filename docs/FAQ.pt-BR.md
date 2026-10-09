# FAQ — Perguntas frequentes

### Isso é legal?
Sim, **desde que você tenha autorização**. Só escaneie redes **suas** ou para as quais o
responsável deu **autorização escrita**. A ferramenta **exige** essa confirmação (termo
RoE) e **não roda sem ela**. Escanear rede de terceiros sem permissão é ilegal.

### Preciso saber Linux ou ser "hacker"?
Não. O [tutorial](TUTORIAL.md) foi escrito para quem **nunca usou Linux**. Você só precisa
dar boot no Kali Live e digitar **um comando**.

### Funciona no Windows ou no Mac?
O jeito recomendado é o **Kali Live** (pendrive), que já traz o `nmap`. O noobmap é só
Python 3 + Nmap: em teoria roda em qualquer sistema com esses dois itens, mas o suporte
alvo é o **Kali Live** (sem instalar nada).

### Isso vai derrubar a internet ou os aparelhos?
**Não.** A varredura é **não invasiva** e em ritmo moderado (`-T3`). O noobmap **não altera
nada** na rede — ele só observa e relata. Quem aplica as mudanças é você, manualmente.

### Vai instalar algo no meu computador?
Não. O **Kali Live** roda do pendrive; nada é instalado. Ao desligar, o computador volta
ao normal.

### Quanto tempo demora?
Alguns minutos para uma rede `/24`. Depende de quantos aparelhos respondem.

### O que é "autorização (RoE)"?
"Rules of Engagement": um termo de 1 página (`docs/roe/termo-de-autorizacao.md`) que o
responsável pela rede assina, autorizando a varredura. É a sua proteção legal.

### O relatório é difícil de entender?
Foi feito para leigos: linguagem simples, riscos por gravidade e um **passo a passo** de
correção dizendo **onde ir**, **o que mudar** e **o que NÃO mexer**.

### O que faço depois de receber o relatório?
1. Salve/exporte a configuração do roteador (**backup**).
2. Aplique as correções **uma a uma**, seguindo o relatório.
3. Teste a internet e os aparelhos depois de cada mudança.
4. Rode o noobmap de novo (**re-scan**) para confirmar a melhoria.

### Apareceu um "falso positivo"?
Toda porta aberta **não é necessariamente** uma falha — pode ser um serviço necessário. O
relatório avisa sobre isso. Na dúvida, **não altere** e confirme o que aquele serviço faz.

### Ele avalia wi-fi, celular ou senha fraca?
**Não.** O noobmap olha **portas/serviços expostos** na rede (foco em ataques remotos
comuns). Wi-fi, celulares, phishing e senhas ficam fora do escopo.

### Isso deixa minha rede 100% segura?
Não. É uma **linha de base** ("segurança mínima"). Ele **reduz bastante** o risco de ataques
remotos automatizados comuns **se** as correções forem aplicadas — mas não substitui
atualização de firmware, senhas fortes, antivírus e cuidados do usuário.

### Posso usar comercialmente / cobrar por isso?
A licença é **MIT** (use à vontade). Mas **lembre-se**: o valor que você entrega é a
avaliação + a orientação de correção — e isso **exige autorização** de quem contrata.

### Como contribuir?
Veja **[CONTRIBUTING.md](../CONTRIBUTING.md)**. Ajuda muito: orientações de correção para
**modelos de roteador específicos**, novas regras de gravidade e traduções.
