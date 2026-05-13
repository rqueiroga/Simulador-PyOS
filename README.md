# PyOS - Simulador Educacional de Sistema Operacional

![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-green)

Este repositório contém a versão final do **PyOS**, um simulador lógico de Sistema Operacional desenvolvido em Python para fins didáticos. O projeto foi evoluído a partir de uma base educacional para implementar conceitos avançados de Kernel, cobrindo desde o gerenciamento básico de processos até comunicação entre processos (IPC).

## Objetivos do Projeto:
* Compreender o **Bloco Descritor de Processo (PCB)** e seu ciclo de vida.
* Implementar e visualizar o **Chaveamento de Contexto**.
* Praticar a **Sincronização de Processos** através de Mutex.
* Gerenciar estados críticos como **Deadlock** e **Processos Zumbi**.
* Simular chamadas de sistema (Syscalls) complexas como o `fork()`.

---

## Desafios Concluídos:

O simulador foi submetido a uma trilha de desafios técnicos, todos implementados com sucesso:

- [x] **🟢 Nível 1: Limite de Memória (OOM)**
  - Implementada proteção que impede o sistema de aceitar mais de 5 processos simultâneos, simulando falta de RAM.
- [x] **🟡 Nível 2: Automador de Clock (Comando `run`)**
  - Criação do comando `run` que automatiza os ciclos de CPU até que todos os processos prontos sejam executados.
- [x] **🟡 Nível 3: Gargalo de E/S (Estado BLOQUEADO)**
  - Implementação dos comandos `block` e `unblock` para gerenciar processos em espera de entrada/saída.
- [x] **🟠 Nível 4: O Fim da Democracia (Prioridades)**
  - O escalonador agora prioriza processos com maior nível de importância, garantindo execução preferencial.
- [x] **🔴 Nível 5 & 6: Sincronização e Deadlock**
  - Controle de acesso a recursos compartilhados via exclusão mútua (Mutex) com comandos `lock` e `unlock`.
- [x] **🟣 Nível 7: O Apocalipse Zumbi**
  - Processos finalizados agora permanecem na memória no estado `ZUMBI` até que o Kernel execute a limpeza via comando `wait`.
- [x] **💀 Nível 8: O Boss Final (`fork()`)**
  - Implementação da hierarquia de processos, permitindo que um processo pai clone seu contexto exato.
- [x] **🔥 Nível Supremo: Comunicação entre Processos (IPC)**
  - Criação de um espaço de memória compartilhada para troca de mensagens entre processos via comandos `write` e `read`.

---

## Como Executar:

## 🚀 Como Executar

Certifique-se de ter o Python 3 instalado em sua máquina.

1. Clone este repositório, navegue até a pasta e execute o Kernel:
   ```bash
   git clone [https://github.com/rqueiroga/Simulador-PyOS.git]
   cd Simulador-PyOS
   python init.py
   
## Créditos e Atribuições:
Este é um projeto educacional baseado no trabalho original do **Professor Filipe Araujo**.

* [cite_start]**Repositório Original:** [PyOS - FilipeHSAraujo](https://github.com/FilipeHSAraujo/PyOs) 
* **Docente Responsável:** [Filipe Araujo](https://github.com/FilipeHSAraujo)

[cite_start]A licença original (MIT) foi mantida, permitindo o uso e modificação para fins didáticos.
