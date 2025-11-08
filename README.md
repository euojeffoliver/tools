┌──(root㉿kali)-[~/projects]
└─$ cat README.md

    ╔╗╔╔═╗  ╔═╗╦ ╦╔═╗╔╦╗╔═╗╔╦╗  ╦╔═╗  ╔═╗╔═╗╔═╗╔═╗
    ║║║║ ║  ╚═╗╚╦╝╚═╗ ║ ║╣ ║║║  ║╚═╗  ╚═╗╠═╣╠╣ ║╣ 
    ╝╚╝╚═╝  ╚═╝ ╩ ╚═╝ ╩ ╚═╝╩ ╩  ╩╚═╝  ╚═╝╩ ╩╚  ╚═╝

    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                                            ┃
    ┃  "No system is truly safe"                 ┃
    ┃                                            ┃
    ┃  >> Every defense has a weakness           ┃
    ┃  >> Every wall has a crack                 ┃
    ┃  >> Every lock has a key                   ┃
    ┃                                            ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──(root㉿kali)-[~/projects]
└─$ nmap -sV -A --script=all target.system

# H4CK TOOLS:

Repositório com scripts de Recon, POCs, Reverse Shell e Pivot para testes reais.

Files:

* `dnsbrute.py` — Brute POST (configurar campos uname/pass, wordlist).
* `crawler.py` — Coleta de URLs.
* `portscan.py` — Triagem Limpa e Rápida de Portas.
* `email_find.py` — Extração de E-mails.
* `sshcli.py` — Tunelamento SSH.
* `host-discover.sh` — Descoberta Limpa de IPs Locais.
* `wldomains.txt` — Lista de Palavras.
* `adv_trojan.py`, `cowroot*.c`, `peshell.c` — POCs/Alto Risco (Usar Só Em Lab).

---

# METODOLOGIA:

1. AUTORIZAÇÃO: Documento escrito com escopo (IPs/domínios), Datas e Responsáveis.
2. ISOLAMENTO: Executar apenas em ambientes controlados.
3. BACKUP: Preparação de plano de recuperação.
4. BANDA: Aplicar throttling/limites; não sobrecarregar alvo.
5. CÓDIGO RISCO: Não compilar/rodar payloads fora de ambiente controlado.
6. LOGS: Armazenar resultados com acesso restrito/criptografado.
7. REPORT: Reproduzir, Impacto, Logs e Mitigação.

---

Não me responsabilizo pelo uso de qualquer ferramenta de modo indevido.
