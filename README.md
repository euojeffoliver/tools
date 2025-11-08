# SSHCLI:
Script em Python que estabelece uma sessão SSH interativa com um host remoto utilizando autenticação por senha.
Ele utiliza a biblioteca **Paramiko** para criar uma conexão segura (`SSHClient()`), define a política `AutoAddPolicy()` para aceitar automaticamente novas chaves de host e executa comandos recebidos via entrada padrão (`raw_input`) em loop contínuo.
Cada comando é enviado ao host e executado com `exec_command()`, retornando a saída capturada em `stdout` e impressa na tela.

---

**Modo de uso técnico**

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

**Modo de uso técnico**

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
**Descrição técnica (adenda)**
Nome do binário: `peshell`. Código tenta `setresuid(0,0,0)` e em seguida chama `system("/bin/bash")`. Elevação só ocorre se o processo já tiver capacidade/privilegios para assumir UID 0 no momento da execução.

---

**Modo de uso técnico — compilação e execução**

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


