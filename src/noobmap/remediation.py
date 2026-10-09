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
    "servico-rpcbind": _entry(
        "Revisar o rpcbind/portmapper exposto (porta 111)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Se não houver serviço de arquivos (NFS) na rede, bloqueie a porta 111 de entrada.",
            "Se houver, restrinja o acesso à rede local (nunca pela internet).",
        ],
        "Não bloqueie se a rede usa NFS internamente, sem confirmar antes.",
    ),
    "servico-rexec": _entry(
        "Desligar o rexec (serviço remoto antigo, porta 512)",
        "Painel do roteador > Firewall / Acesso remoto",
        [
            "Desative serviços r (rsh/rexec/rlogin) — são antigos e sem criptografia.",
            "Remova qualquer encaminhamento dessas portas para a internet.",
        ],
        "Não desligue o acesso remoto que a empresa realmente usa (prefira SSH/VPN).",
    ),
    "servico-rlogin": _entry(
        "Desligar o rlogin (serviço remoto antigo, porta 513)",
        "Painel do roteador > Firewall / Acesso remoto",
        [
            "Desative o rlogin — não tem criptografia.",
            "Para acesso remoto, use SSH ou VPN.",
        ],
        "Prefira SSH/VPN; só desative após confirmar que ninguém depende disso.",
    ),
    "servico-rsh": _entry(
        "Desligar o rsh (serviço remoto antigo, porta 514)",
        "Painel do roteador > Firewall / Acesso remoto",
        [
            "Desative o rsh — não tem criptografia.",
            "Remova encaminhamentos da porta 514 para a internet.",
        ],
        "Prefira SSH/VPN; só desative após confirmar que ninguém depende disso.",
    ),
    "servico-oracle": _entry(
        "Fechar o banco Oracle exposto (porta 1521)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 1521 para a internet.",
            "Bancos de dados devem ficar só na rede interna.",
            "Para acesso remoto legítimo, use VPN.",
        ],
        "Não pare o banco; apenas feche o acesso vindo da internet.",
    ),
    "servico-nfs": _entry(
        "Proteger o compartilhamento NFS (porta 2049)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova qualquer encaminhamento da porta 2049 para a internet.",
            "Restrinja o NFS por IP/cliente na própria máquina que compartilha.",
        ],
        "Não desligue o NFS interno se ele for usado pela empresa.",
    ),
    "servico-docker": _entry(
        "Fechar a API do Docker exposta (porta 2375) — URGENTE",
        "Servidor (não o roteador): arquivo de configuração do Docker",
        [
            "Nunca exponha a API do Docker (2375/2376) na internet: dá controle total da máquina.",
            "Remova o '-H tcp://...' da configuração do daemon.",
            "Use apenas o socket local; para remoto, use SSH.",
        ],
        "Fazer isso sem saber pode derrubar contêineres em uso — faça com calma e backup.",
    ),
    "servico-winrm": _entry(
        "Proteger a gerência remota Windows / WinRM (porta 5985)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 5985 para a internet (use 5986 com TLS só via VPN).",
            "Para administrar remotamente, prefira VPN.",
        ],
        "Não desligue o WinRM usado internamente pela equipe de TI.",
    ),
    "servico-redis": _entry(
        "Fechar o Redis exposto (porta 6379)",
        "Servidor (não o roteador): configuração do Redis",
        [
            "Redis não deve ficar acessível de fora da rede.",
            "Tire o encaminhamento da porta 6379 no roteador.",
            "Ative senha (requirepass) e escute só em 127.0.0.1/rede local.",
        ],
        "O Redis pode guardar dados em uso — não apague nada, apenas restrinja o acesso.",
    ),
    "servico-https-alt": _entry(
        "Revisar o painel HTTPS alternativo exposto (porta 8443)",
        "Painel do roteador > Administração / Serviços",
        [
            "Confirme se esse painel precisa mesmo estar acessível.",
            "Use senha forte e mantenha o firmware atualizado.",
            "Prefira acesso local ou via VPN em vez de expor na internet.",
        ],
        "Não desative o painel local por onde você administra o equipamento.",
    ),
    "servico-jupyter": _entry(
        "Fechar o Jupyter exposto (porta 8888) — execução de código",
        "Servidor (não o roteador): configuração do Jupyter",
        [
            "Um Jupyter aberto permite executar código na máquina — feche o acesso externo.",
            "Tire o encaminhamento da porta 8888 no roteador.",
            "Use senha/token e escute só na rede local ou via VPN.",
        ],
        "Não apague notebooks; apenas restrinja quem consegue acessar.",
    ),
    "servico-elasticsearch": _entry(
        "Fechar o Elasticsearch exposto (porta 9200)",
        "Servidor (não o roteador): configuração do Elasticsearch",
        [
            "Elasticsearch não deve ficar acessível de fora da rede.",
            "Tire o encaminhamento da porta 9200 no roteador.",
            "Ative autenticação e escute só na rede local.",
        ],
        "Não pare o serviço de busca; apenas restrinja o acesso.",
    ),
    "servico-memcached": _entry(
        "Fechar o Memcached exposto (porta 11211)",
        "Servidor (não o roteador): configuração do Memcached",
        [
            "Memcached pode ser abusado em ataques de amplificação — não exponha na internet.",
            "Tire o encaminhamento da porta 11211 no roteador.",
            "Escute só em 127.0.0.1/rede local.",
        ],
        "Não pare o cache; apenas restrinja o acesso.",
    ),
    "servico-mongodb": _entry(
        "Fechar o MongoDB exposto (porta 27017)",
        "Painel do roteador > Firewall / Port Forwarding",
        [
            "Remova o encaminhamento da porta 27017 para a internet.",
            "Ative autenticação e restrinja o banco à rede local.",
            "Para acesso remoto, use VPN.",
        ],
        "Não pare o banco; apenas feche o acesso vindo da internet.",
    ),
    "precisa-verificacao": PLACEHOLDER,
}


def has(key):
    return key in REMEDIATION


def get(key):
    return REMEDIATION.get(key, PLACEHOLDER)
