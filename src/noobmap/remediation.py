DISCLAIMER = (
    "Importante: esta ferramenta NUNCA aplica alterações na sua rede. As orientações abaixo "
    "são para você executar manualmente, sempre com backup da configuração antes."
)

PLACEHOLDER = {
    "titulo": "Precisa de verificação manual",
    "onde_ir": "—",
    "passos": [
        "Este item não tem correção automática pronta.",
        "Anote o host e a porta e verifique com calma antes de mudar qualquer coisa.",
        "Na dúvida, pare e não altere a configuração.",
    ],
    "backup": "Antes de qualquer mudança, exporte/salve a configuração atual do roteador.",
    "desfazer": "Guarde o backup para restaurar a configuração anterior se algo piorar.",
    "nao_mexer": "Não desligue serviços sem saber o que são — pode derrubar a internet.",
}


def _entry(titulo, onde_ir, passos, nao_mexer):
    return {
        "titulo": titulo,
        "onde_ir": onde_ir,
        "passos": passos,
        "backup": "Antes de mudar: abra a página do roteador e salve/exporte a configuração atual.",
        "desfazer": "Se algo quebrar, restaure o backup e reinicie o roteador.",
        "nao_mexer": nao_mexer,
    }


REMEDIATION = {
    "servico-telnet": _entry(
        "Desligar o Telnet (acesso remoto antigo e sem criptografia)",
        "Painel do roteador > Administração / Acesso remoto (Remote Management)",
        [
            "Procure a opção de acesso remoto/Telnet e DESATIVE.",
            "Se você precisa de acesso remoto, use apenas via VPN.",
            "Confirme que a opção 'WAN/Internet remote access' ficou desligada.",
        ],
        "Não desligue o acesso local (LAN) por onde você administra o roteador.",
    ),
    "servico-ftp": _entry(
        "Desligar o FTP exposto",
        "Painel do roteador > Serviços / USB / Servidor de arquivos",
        [
            "Se o FTP do roteador estiver ativo para a internet, DESATIVE.",
            "Para compartilhar arquivos, prefira a rede local ou um serviço com senha forte.",
            "Se houver regra de encaminhamento (port forward) para a porta 21, remova.",
        ],
        "Não remova o compartilhamento de arquivos que a empresa realmente usa, sem avisar.",
    ),
    "servico-rpc": _entry(
        "Bloquear RPC do Windows na borda (porta 135)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Procure regras que apontam a porta 135 para um computador interno e REMOVA.",
            "Garanta que o bloqueio de entrada (WAN) esteja ligado no firewall do roteador.",
            "Se o Windows não usa RPC pela internet, nada precisa ser aberto.",
        ],
        "Não mexa no RPC usado internamente entre computadores da mesma rede.",
    ),
    "servico-netbios": _entry(
        "Bloquear NetBIOS na borda (porta 139)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova qualquer encaminhamento da porta 139 para dentro da rede.",
            "Confirme que o roteador bloqueia acessos de entrada (WAN) por padrão.",
            "Mantenha o compartilhamento só na rede local.",
        ],
        "Não desative o compartilhamento interno se a empresa depende dele.",
    ),
    "servico-smb": _entry(
        "Proteger o SMB / compartilhamento de arquivos (porta 445)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova qualquer encaminhamento (port forward) da porta 445 para a internet.",
            "Mantenha o compartilhamento acessível apenas na rede local.",
            "Se houver servidor de arquivos, restrinja por usuário e senha forte.",
        ],
        "Não desligue o servidor de arquivos da empresa; apenas feche o acesso externo.",
    ),
    "servico-mssql": _entry(
        "Fechar o banco SQL Server exposto (porta 1433)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 1433 para a internet.",
            "Bancos de dados nunca devem ficar acessíveis de fora da rede.",
            "Se houver acesso remoto legítimo, use VPN.",
        ],
        "Não pare o banco de dados; apenas feche o acesso vindo da internet.",
    ),
    "servico-mysql": _entry(
        "Fechar o banco MySQL exposto (porta 3306)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 3306 para a internet.",
            "Restrinja o banco à rede local.",
            "Para acesso remoto, use VPN em vez de expor a porta.",
        ],
        "Não pare o banco de dados; apenas feche o acesso vindo da internet.",
    ),
    "servico-postgres": _entry(
        "Fechar o banco PostgreSQL exposto (porta 5432)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 5432 para a internet.",
            "Restrinja o banco à rede local.",
            "Para acesso remoto, use VPN em vez de expor a porta.",
        ],
        "Não pare o banco de dados; apenas feche o acesso vindo da internet.",
    ),
    "servico-rdp": _entry(
        "Proteger a Área de Trabalho Remota / RDP (porta 3389)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 3389 para a internet.",
            "Para acesso remoto legítimo, use VPN em vez de expor o RDP.",
            "Exija senha forte e bloqueio após várias tentativas erradas.",
        ],
        "Não desligue o RDP interno usado pelos funcionários na rede local.",
    ),
    "servico-vnc": _entry(
        "Proteger o acesso VNC (porta 5900)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 5900 para a internet.",
            "Use VPN para acesso remoto em vez de expor o VNC.",
            "Defina senha forte e limite quem pode conectar.",
        ],
        "Não desligue o VNC usado internamente, sem avisar quem depende dele.",
    ),
    "servico-http": _entry(
        "Ativar HTTPS no site/painel (porta 80)",
        "Painel do roteador > Administração > HTTPS",
        [
            "Ative o acesso de administração via HTTPS, se disponível.",
            "Troque a senha padrão por uma senha forte e única.",
            "Evite administrar o roteador por HTTP; prefira HTTPS.",
        ],
        "Não desative o acesso web local por onde você administra o roteador.",
    ),
    "servico-ssh": _entry(
        "Proteger o SSH (porta 22)",
        "Painel do roteador > Administração / SSH",
        [
            "Use chave em vez de senha, se possível.",
            "Desative o login de root por senha e use senha forte para os demais.",
            "Restrinja o acesso SSH à rede local ou via VPN.",
        ],
        "Não desligue o SSH se ele for o único jeito de administrar o equipamento.",
    ),
    "servico-dns": _entry(
        "Revisar o servidor DNS exposto (porta 53)",
        "Painel do roteador > Serviços de rede / DNS",
        [
            "Se o DNS não precisa ser público, bloqueie respostas para a internet.",
            "Evite DNS aberto (open resolver), que pode ser abusado por atacantes.",
            "Mantenha o firmware do roteador atualizado.",
        ],
        "Não desative o DNS local, ou a rede perde a resolução de nomes.",
    ),
    "servico-smtp": _entry(
        "Revisar o servidor de e-mail SMTP exposto (porta 25)",
        "Painel do roteador > Firewall / Servidor de e-mail",
        [
            "Se não houver servidor de e-mail próprio, bloqueie a porta 25 de entrada.",
            "Se houver, exija autenticação e use TLS.",
            "Encaminhe o envio de e-mails por um provedor confiável, se possível.",
        ],
        "Não bloqueie o e-mail que a empresa realmente usa, sem confirmar antes.",
    ),
    "servico-http-alt": _entry(
        "Revisar o painel alternativo exposto (porta 8080)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Se o painel não precisa ser acessado de fora, remova o encaminhamento da 8080.",
            "Ative HTTPS no painel, se disponível.",
            "Troque a senha padrão por uma senha forte e única.",
        ],
        "Não desligue o painel se ele for o jeito de administrar o aparelho na rede local.",
    ),
    "servico-https": _entry(
        "Revisar o serviço HTTPS exposto (porta 443)",
        "Painel do roteador > Administração / Serviços",
        [
            "Confirme se o painel realmente precisa ficar acessível.",
            "Use senha forte e mantenha o firmware atualizado.",
            "Prefira acesso pela rede local ou via VPN em vez de expor na internet.",
        ],
        "Não desative o HTTPS do painel local, ou você perde o acesso seguro ao roteador.",
    ),
    "servico-pop3": _entry(
        "Revisar o e-mail POP3 exposto (porta 110)",
        "Painel do roteador > Firewall / Servidor de e-mail",
        [
            "Se não houver servidor de e-mail próprio, bloqueie a 110 vinda da internet.",
            "Se houver, exija autenticação e use SSL/TLS (POP3S, porta 995).",
            "Evite acessar e-mail sem criptografia; prefira um provedor confiável.",
        ],
        "Não bloqueie o e-mail que a empresa realmente usa, sem confirmar antes.",
    ),
    "servico-imap": _entry(
        "Revisar o e-mail IMAP exposto (porta 143)",
        "Painel do roteador > Firewall / Servidor de e-mail",
        [
            "Se não houver servidor de e-mail próprio, bloqueie a 143 vinda da internet.",
            "Se houver, exija autenticação e use SSL/TLS (IMAPS, porta 993).",
            "Evite e-mail sem criptografia; prefira um provedor confiável.",
        ],
        "Não bloqueie o e-mail que a empresa realmente usa, sem confirmar antes.",
    ),
    "precisa-verificacao": PLACEHOLDER,
}


def has(key):
    return key in REMEDIATION


def get(key):
    return REMEDIATION.get(key, PLACEHOLDER)
