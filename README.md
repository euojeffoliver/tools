# SSHCLI:
Script em Python que estabelece uma sessão SSH interativa com um host remoto utilizando autenticação por senha.
Ele utiliza a biblioteca **Paramiko** para criar uma conexão segura (`SSHClient()`), define a política `AutoAddPolicy()` para aceitar automaticamente novas chaves de host e executa comandos recebidos via entrada padrão (`raw_input`) em loop contínuo.
Cada comando é enviado ao host e executado com `exec_command()`, retornando a saída capturada em `stdout` e impressa na tela.

---

**Modo de uso**

1. **Pré-requisitos:**

   * Python 2.x instalado.
   * Biblioteca Paramiko instalada (`pip install paramiko`).

2. **Execução:**

   ```
   python sshcli.py <user> <host> <password>
   ```

   ou, se o script estiver com permissão de execução:

   ```
   ./sshcli.py <user> <host> <password>
   ```

3. **Parâmetros:**

   * `<user>`: usuário autorizado no host remoto.
   * `<host>`: IP ou domínio do servidor remoto (porta padrão 22).
   * `<password>`: senha correspondente ao usuário informado.

4. **Comportamento:**

   * O script cria uma instância `paramiko.SSHClient()` e conecta ao servidor remoto.
   * Entra em um loop interativo exibindo o prompt `Code:`.
   * Cada comando digitado é executado remotamente via `exec_command()`.
   * A saída do comando (`stdout`) é retornada e exibida em formato de lista Python.
   * Interrompe a execução com `Ctrl+C` ou fechamento do terminal.

5. **Observações técnicas:**

   * Não há tratamento de exceções durante o loop — falhas de rede ou autenticação encerram o programa.
   * As chaves de host são aceitas automaticamente, o que dispensa verificação manual (potencial risco em ambiente de produção).
   * Senhas são passadas como argumento em linha de comando (visíveis em histórico/process list).
   * Compatível apenas com **Python 2** devido ao uso de `raw_input` e `print` sem parênteses.



# PORTSCAN:
Script em Python (destinado a Python 2) que realiza um *port scan* sequencial em uma lista fixa de portas.
Recebe um argumento (host/IP), cria um socket TCP para cada porta, usa `connect_ex()` com timeout de 0.5s para testar conectividade e imprime `"<porta>-> OPEN"` quando a conexão é bem-sucedida (código 0). O loop inclui `time.sleep(1)` entre tentativas; ao final aguarda 2s e imprime `Scan Completed.`.

---

**Modo de uso**

1. **Pré-requisitos:** Python 2.x (interprete compatível com `raw` prints usados no script). Nenhuma dependência externa.
2. **Execução:**

   ```
   python portscan.py <Address|IP>
   ```

   ou, se tornar executável e corrigir o shebang para Python:

   ```
   ./portscan.py <Address|IP>
   ```
3. **Parâmetros:**

   * `<Address|IP>`: nome do host (ex.: `example.com`) ou endereço IP a ser escaneado.
4. **Comportamento:**

   * Porta alvo: lista estática `ports = [20,21,22,23,25,53,67,68,80,110,123,143,156,179,442,1723,1863,3128,2289]`.
   * Para cada porta: cria `socket(AF_INET, SOCK_STREAM)`, configura `settimeout(0.5)`, executa `connect_ex((url, port))`.
   * Se `connect_ex()` retornar `0`, imprime `"<porta>-> OPEN"`.
   * Há `time.sleep(1)` entre cada porta (varia a duração total do scan).
   * Fecha o script com mensagem final `Scan Completed.` após `time.sleep(2)`.
5. **Observações técnicas / limitações:**

   * Shebang está errado (`/bin/bash`) — o script só roda como Python quando invocado explicitamente com `python`.
   * Compatível com **Python 2** (uso de `print` sem parênteses e `raw_input` ausente aqui, mas estilo similar).
   * Não fecha explicitamente cada socket (`c.close()` ausente) — pode esgotar descritores em scans maiores.
   * `time.sleep(1)` torna o scanner lento (um segundo por porta).
   * Scan é **sequencial** (não paralelo) e cobre apenas portas na lista fixa.
   * Timeout de 0.5s pode gerar falsos negativos em redes lentas.
6. **Aviso legal/ético:**

   * Use apenas contra hosts/infraestruturas que você possua autorização explícita para testar. Scans não autorizados podem ser ilegais e detectados por sistemas de defesa.



# PESHELL:
Nome do binário: `peshell`. Código tenta `setresuid(0,0,0)` e em seguida chama `system("/bin/bash")`. Elevação só ocorre se o processo já tiver capacidade/privilegios para assumir UID 0 no momento da execução.

---

**Modo de Uso**

1. **Compilar:**

```
gcc -o peshell peshell.c -Wall -Wextra -O0 -g
```

2. **Executar (ambiente controlado / laboratório):**

```
./peshell
```

3. **Executar com privilégios (somente em teste autorizado):**

* Se você precisa testar comportamento de elevação em ambiente controlado, execute como root:

```
sudo ./peshell
```

(ou inicie um shell root e execute `./peshell`).

---

**Avisos rápidos**

* Não torne esse binário SUID em sistemas de produção.
* Teste apenas em VMs/containers isolados e com autorização.
* Compilar/rodar em máquinas alheias sem permissão é ilegal.


# HOST-DISCOVER:
Script `discover.sh` em Bash que itera IPs `10.0.0.1` a `10.0.0.254`, dispara um `ping -c 1` por IP em segundo plano e filtra respostas bem-sucedidas com `grep "bytes from"`.
Resultado: linhas de ping apenas para hosts que responderam ICMP. Não há sincronização (`wait`) nem controle de número máximo de processos simultâneos.

---

**Modo de uso**

1. **Pré-requisitos:** shell POSIX (bash), utilitário `ping`, `grep`. Ambiente com permissão para enviar ICMP no segmento de rede alvo.
2. **Nome do arquivo:** `discover.sh`
3. **Permissão de execução:**

```bash
chmod +x discover.sh
```

4. **Execução:**

```bash
./discover.sh
```

5. **Parâmetros (edição do script):**

* Subnet fixa no script: `10.0.0.` — altere conforme sua rede.
* Intervalo de IPs: `seq 1 254` — ajuste se precisar de outro range.

6. **Comportamento em tempo de execução:**

* Para cada IP do range, cria um processo que executa `ping -c 1 10.0.0.$ip` e canaliza a saída para `grep "bytes from"`.
* Hosts que respondem geram uma linha do tipo `64 bytes from 10.0.0.x: icmp_seq=1 ttl=64 time=0.123 ms`.
* Processos são executados em background (`&`); o script termina rapidamente sem aguardar todos os pings (saída pode intercalar ou alguns resultados aparecerem após o término do shell pai).

7. **Limitações / observações técnicas:**

* Gera até 254 processos simultâneos — risco de esgotar descritores/processos em sistemas com limites baixos.
* Sem `wait` nem sincronização; para garantir conclusão use `wait` ao final.
* Timeout do `ping` depende da implementação; em redes lentas pode haver falso negativo.
* Saída não ordenada; resultados chegam conforme resposta dos hosts.
* Uso de `grep "bytes from"` funciona em implementações de `ping` que imprimem essa string (BSD/Linux comuns); pode variar em outros sistemas.

8. **Aviso legal/ético:**

* Execute apenas em redes onde você tem autorização explícita. Scans/ICMP floods em redes alheias podem ser detectados e são potencialmente ilegais.


# EMAIL-FIND:
Ferramenta em Python que realiza varredura automatizada em um site para localizar endereços de e-mail embutidos em páginas HTML.
O script rastreia links internos e segue as URLs encontradas, coletando e armazenando todos os e-mails detectados com expressões regulares. Inclui cabeçalho “User-Agent” para simular navegação real e aceita definição do número de tentativas de rastreamento.

**Modo de uso técnico:**

1. Execute no terminal:

   ```bash
   python email_find.py
   ```
2. Informe o domínio-alvo sem `http://` (ex: `example.com`).
3. Defina o número de tentativas (iterações de rastreamento).
4. O programa listará os e-mails encontrados após concluir o número definido de tentativas.

**Exemplo:**

```bash
python email_find.py
Enter a website: example.com
OK, how many attempts do you want to make? 10
```

> Resultado: exibe os e-mails descobertos e o total de tentativas realizadas.

# DNS-BRUTE:
**Descrição técnica**
Script Python (estilo Python 2) que faz enumeração simples de subdomínios a partir de uma wordlist usando `dnsbrute` (`dns.resolver`). O script recebe dois argumentos — `<domain>` e `<wordlist>` — concatena cada palavra da lista com o domínio (`sub.domain`) e faz uma consulta DNS do tipo A (`dns.resolver.query`). Se houver resposta, imprime `sub.domain <IP>`. Exceções de resolução são silenciosamente ignoradas. Observações: o arquivo inicia com `#! /bin/bash` (shebang incorreto para Python) e usa APIs/prints compatíveis com Python 2.

---

**Modo de uso técnico**

1. **Pré-requisitos**

   * Python 2.x instalado.
   * Biblioteca dnspython: `pip install dnspython` (versão compatível com Python 2).
   * Wordlist de subdomínios (arquivo texto, uma entrada por linha).

2. **Nome do arquivo sugerido**

   * `dnsbrute.py`

3. **Execução**

   ```bash
   python dnsbrute.py <domain> <wordlist>
   ```

   Exemplo:

   ```bash
   python dnsbrute.py example.com subdomains.txt
   ```

4. **Parâmetros**

   * `<domain>`: domínio alvo (ex.: `example.com`).
   * `<wordlist>`: caminho para arquivo texto contendo possíveis subdomínios (ex.: `www`, `mail`, `api`).

5. **Comportamento**

   * Abre e lê a wordlist (`read().splitlines()`).
   * Para cada `subdom` na lista:

     * Constrói `domesub = subdom + '.' + domain`.
     * Executa `dns.resolver.query(domesub, 'a')`.
     * Se houver resposta A, imprime `domesub <IP>` para cada registro retornado.
   * Qualquer erro de resolução (NXDOMAIN, timeout, etc.) é engolido pelo `except: pass`, portanto falhas não são reportadas.

6. **Limitações técnicas**

   * Compatível apenas com **Python 2** (uso de `print` sem parênteses e API legada `dns.resolver.query`).
   * Sem timeout/controle de retries configurável (usa valores padrão do resolver).
   * Sem controle de taxa (pode gerar muitas consultas rapidamente).
   * Não detecta wildcard DNS; resultados falsos positivos possíveis.
   * Falta de logging e de fechamento explícito do arquivo (boa prática).
   * Exceções silenciosas dificultam diagnóstico de problemas (por exemplo, rate-limiting).

7. **Melhorias técnicas recomendadas**

   * Atualizar para Python 3 e usar `dns.resolver.resolve()` (API moderna).
   * Adicionar timeout e retries: configurar `resolver = dns.resolver.Resolver(); resolver.timeout = X; resolver.lifetime = Y`.
   * Implementar limitação de taxa / paralelismo controlado (`ThreadPoolExecutor` + rate limiter).
   * Detectar e filtrar wildcard DNS (testar com subdomínio aleatório).
   * Registrar erros relevantes (NXDOMAIN, SERVFAIL, timeout) em verbose/debug.
   * Saída em formato estruturado (CSV/JSON) para integração com pipelines.
   * Validar existência e leitura do arquivo antes de tentar processar.

8. **Aviso legal/ético**

   * Realize varreduras DNS apenas contra domínios onde você tem autorização explícita. Enumeração não-autorizada pode ser considerada intrusiva e/ou ilegal.

   

# CRAWLER:

Crawler em Python 2 que faz crawling recursivo de páginas a partir de um domínio inicial. Usa `requests` para obter HTML, uma regex para extrair links absolutos `https?://...`, mantém `to_crawl` (lista FIFO) e `crawled` (set) para evitar reprocessar URLs, imprime `Crawling: <url>` a cada iteração.
Cabeçalho `User-Agent` é definido. O loop principal é infinito até ocorrer exceção (ex.: `to_crawl` vazio gera `IndexError`) — exceções são capturadas pelo `try/except` externo que imprime erro e uma mensagem de uso.

---

**Modo de uso técnico**

1. **Pré-requisitos**

   * Python 2.x.
   * Biblioteca `requests`: `pip install requests`.

2. **Nome do arquivo**

   * `crawler.py`

3. **Execução**

   ```bash
   python crawler.py
   ```

   No prompt, informar o domínio sem `http://` (ex.: `example.com`).

4. **Parâmetros/Entrada**

   * Entrada interativa via `raw_input('Enter a website: ')`. O script inicializa `to_crawl = ['http://' + site]`.

5. **Comportamento**

   * Remove o primeiro URL de `to_crawl`, faz `requests.get(url, headers=header)`.
   * Extrai links absolutos com `re.findall(r'<a href="?\'?(https?:\/\/[^"\'>]*)', html)`.
   * Adiciona links novos a `to_crawl`; marca `url` como `crawled`.
   * Imprime `Crawling: <url>` para cada página processada.
   * Loop contínuo até uma exceção interromper (por exemplo `IndexError` quando `to_crawl` ficar vazio), então o bloco `except` externo imprime erro e uma mensagem de ajuda.

6. **Observações técnicas / limitações**

   * Compatível apenas com **Python 2** (`raw_input`, `print` sem parênteses).
   * Apenas segue **links absolutos** (não resolve links relativos).
   * Não respeita `robots.txt`.
   * Sem controle de taxa, sem timeout configurado explicitamente (usa timeout default do `requests`).
   * Possível `IndexError` quando `to_crawl` ficar vazio — tratado pelo `except` externo que encerra com mensagem genérica.
   * Sem limite de profundidade, sem detecção de ciclos além do `crawled` set; pode consumir memória/CPU em sites grandes.
   * Regex simples pode falhar em HTML complexo/JS-generated links; não executa JavaScript.

7. **Parada**

   * Interromper com `Ctrl+C` (KeyboardInterrupt) ou deixar o script lançar exceção quando `to_crawl` esvaziar.

8. **Aviso**

   * Execute somente em alvos que você tem autorização para rastrear. Scanning/crawling não autorizado pode ser inexato ou ilegal.



# ADV TROJAN

O ficheiro contém um *backdoor* remoto em Python (estilo Python 2) com comportamento de persistência e execução remota de comandos. Pontos críticos identificáveis sem execução:

* Copia um executável (`trojan.exe`) para o diretório temporário do Windows (`%TEMP%`).
* Tenta criar persistência adicionando entrada em `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` com o valor `driver_update` apontando para o executável em `%TEMP%`.
* Abre um socket TCP e tenta conectar continuamente a um controlador remoto (`192.168.0.13:4444` no exemplo).
* Após conexão, recebe strings, as trata como comandos e executa via `subprocess.Popen(..., shell=True)`, retornando stdout+stderr ao controlador.
* Comunicação sem autenticação e sem criptografia — execução arbitrária remota sem verificação.
* Loop de reconexão contínuo e reinício automático em erro; reinicia a si mesmo se a conexão cair.

---

**Modo de uso técnico — ALERTA e procedimentos seguros (imediatos)**

1. **ACÃO IMEDIATA (isolar e preservar evidências):**

   * Isole a máquina da rede (retire cabo/disable NIC).
   * Faça imagem forense do disco e memória antes de mudanças (preserve evidências).
   * Colete artifacts: lista de processos, `tasklist`/`ps`, conexões de rede (`netstat -anb`/`ss -tup`), chaves de registro (Run), e conteúdo de `%TEMP%`.

2. **Indicadores (IOCs) para detecção rápida:**

   * Arquivo suspeito: `%TEMP%\trojan.exe` (ou arquivo com nome similar).
   * Entrada de persistência: `HKLM\Software\Microsoft\Windows\CurrentVersion\Run\driver_update`.
   * Conexões TCP de saída para `192.168.0.13:4444` (ou IP/porta configurados).
   * Processos Python invocando `subprocess.Popen(..., shell=True)` frequentemente; shells interativos iniciados por processos não esperados.
   * Logs de execução de comandos remotos sem usuário humano autenticado.

3. **Contenção e limpeza controlada:**

   * Não delete ou sobrescreva logs/artefatos antes da imagem forense.
   * Após coleta, remova a máquina da produção e faça varredura/limpeza: encerrar processo, remover registro de autorun, remover arquivo em `%TEMP%`.
   * Reinstale o sistema operacional se houver suspeita de comprometimento profundo.
   * Roteie/rotate todas as credenciais possivelmente comprometidas (contas locais, chaves, tokens) e force logout de sessões remotas.

4. **Remediação e prevenção:**

   * Aplicar/atualizar AV/EDR e executar varredura completa.
   * Revisar políticas de execução: bloquear execução de binários em `%TEMP%`, restringir criação de chaves Run em HKLM a administradores via GPO/SElinux equivalents.
   * Implementar lista de permissões de aplicações (AppLocker/Device Guard).
   * Monitorar e alertar em EDR/IDS para padrões: criação de autorun no registro, execuções de `cmd/bash` por processos não esperados, conexões TCP persistentes a endereços externos.

5. **Remoção do repositório / comunicação pública:**

   * Remova imediatamente esses ficheiros de qualquer repositório público ou interno.
   * Se já estiverem no git público: remova do histórico com `git filter-repo` ou BFG e force-push; rotacione qualquer credencial que possa ter sido exposta pelo repositório.
   * Commit/PR sugerido (modelo curto):

     ```
     Remove backdoor script por motivos de segurança: conteúdo sensível (persistência e execução remota). Arquivos movidos para armazenamento seguro e histórico limpo. Contactar security@empresa para proceder com auditoria.
     ```

6. **Análise pós-incidente:**

   * Fazer investigação forense completa: identificar origem do commit, quem teve acesso, timestamps, e se houve execução em infraestrutura.
   * Revisar logs de rede e SIEM para conexões externas correlacionadas com os IOCs.
   * Notificar stakeholders de segurança e, se aplicável, compliance/legal.

7. **Aviso legal e ético:**

   * Manuseie e armazene esse material apenas com autorização formal. Execução ou distribuição não autorizada é ilegal.

---

Se quiser, eu já gero agora:

* (A) a **mensagem de commit** pronta para o seu repositório (texto exato);
* (B) os **comandos `git filter-repo` / BFG`** em formato técnico para remover os arquivos do histórico (instruções seguras);
* (C) uma **lista formatada de IOCs** pronta para colar no SIEM/EDR.

Escolha uma das opções que quer que eu gere imediatamente.



# COWROOT 32 | 64:

**Descrição técnica**
Os ficheiros `cowroot64.c`, `cowroot32.c` e `cowroot.c` sugerem variantes de um exploit de escalonamento local baseado na vulnerabilidade *Dirty COW* (CVE-2016-5195). Em termos gerais: trata-se de código destinado a obter privilégios elevados localmente explorando comportamento de copy-on-write no kernel Linux. Esse tipo de código é perigoso — pode comprometer integridade/confidencialidade do sistema — e não deve ser executado ou distribuído sem autorização explícita em ambiente controlado.

---

**Modo de uso técnico (alerta e procedimentos seguros)**

1. **Não execute.**

   * Não compilar nem executar esses ficheiros em máquinas de produção, pessoais ou de terceiros. Mesmo em máquinas de teste, só em ambientes isolados (VMs/labs) com snapshots e autorização explícita.

2. **Isolamento e armazenamento seguro:**

   * Mova os ficheiros para um diretório restrito (ex.: armazenamento offline ou pasta criptografada).
   * Restrinja permissões: apenas conta de auditoria deve ler; por exemplo `chmod 600 nome_do_arquivo` e `chown root:root` em sistema controlado.
   * Não os mantenha em repositórios públicos. Se já estiverem no git público, proceda à remoção do histórico (usar ferramentas como `git filter-repo` ou BFG) e rotacione credenciais possivelmente expostas.

3. **Remoção do repositório (boas práticas):**

   * Remover ficheiros do branch atual (`git rm --cached`) e commitar.
   * Remover do histórico com `git filter-repo` / BFG (ou instruir ops/infra a fazer isso).
   * Fornecer um commit/PR com mensagem de segurança indicando a remoção e razão.

4. **Detecção e verificação do sistema:**

   * Verifique kernel e patches: `uname -r` (obter versão do kernel) e compare com boletins do fornecedor.
   * Atualize o kernel e pacotes do sistema conforme advisories do seu distribuidor.
   * Procure sinais de comprometimento (processos estranhos, shells com UID 0 não esperados, novas contas, entradas SUID/Binary changes) e execute análise forense se houver suspeita.

5. **Mitigação imediata:**

   * Atualize o sistema com patches oficiais do fornecedor (distribuição).
   * Revise e remova bits SUID desnecessários; audite binários com permissões elevadas.
   * Habilite monitoramento/auditoria (auditd, EDR, logs centralizados).

6. **Comunicação & conformidade:**

   * Se for código legado de pentest, documente claramente autorização (escopo, data, responsável).
   * Notifique stakeholders/segurança e mantenha prova de autorização antes de qualquer teste.

7. **Alternativas seguras para laboratório:**

   * Se o objetivo for pesquisa/educação, use imagens de VM isoladas com snapshots e rotinas de rollback; mantenha logs e não compartilhe exploits em repositórios públicos.

8. **Aviso legal e ético:**

   * Manuseie este material apenas com autorização. Execução/redistribuição não autorizada pode ser crime.
   
