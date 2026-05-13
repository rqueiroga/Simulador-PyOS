#imports
import time
import sys
import random

# ==========================================
# ESTRUTURAS DE DADOS DO KERNEL
# ==========================================

# Tabela global de processos (Nossa "RAM")
tabela_processos = []
# Nível Supremo: Memória Compartilhada
espaco_ipc = {}
# PIDs na vida real começam em 1000 
pid_counter = 1000 

class PCB:
    def __init__(self, nome, pai=None, prioridade=1):
        global pid_counter
        self.pid = pid_counter
        self.nome = nome
        self.estado = "PRONTO"
        self.ciclos_restantes = random.randint(2, 6)
        self.prioridade = prioridade  # Nível 4
        self.pai = pai  # Nível 8
        pid_counter += 1

# Recurso compartilhado 
recurso_em_uso_por = None

# ==========================================
# FUNÇÕES DO KERNEL E ESCALONADOR
# ==========================================

def boot():
    """Simula a inicialização do Sistema Operacional"""
    print("Iniciando PyOS Kernel v1.0...")
    time.sleep(1)
    print("Carregando módulos de memória [OK]")
    time.sleep(0.5)
    print("Iniciando escalonador de processos [OK]")
    time.sleep(0.5)
    print("Bem-vindo ao terminal. Digite 'help' para comandos.\n")

def spawn_process(nome, prioridade=1):
    """Cria um novo processo respeitando o limite de 5 (OOM)"""
    if len(tabela_processos) >= 5:
        print(f"[ERRO] Out of Memory: Não foi possível criar '{nome}'.")
        return

    novo_processo = PCB(nome, prioridade=prioridade)
    tabela_processos.append(novo_processo)
    print(f"[Kernel] Processo '{nome}' criado (PID {novo_processo.pid}, Prioridade {prioridade})")

def escalonador_tick():
    
    prontos = [p for p in tabela_processos if p.estado == "PRONTO"]
    
    if not prontos:
        return  # Sai da função se não houver ninguém pronto

    # Nível 4: Ordena por prioridade (Garante que o maior número rode antes)
    prontos.sort(key=lambda p: p.prioridade, reverse=True)
    p = prontos[0]
    
    p.estado = "EXECUTANDO"
    print(f"[CPU] Executando PID {p.pid} ({p.nome}) | Prioridade: {p.prioridade}")
    time.sleep(0.2) # Diminuí o tempo para ser mais rápido
    
    p.ciclos_restantes -= 1
    
    if p.ciclos_restantes <= 0:
        p.estado = "ZUMBI" # Nível 7
        print(f"[Kernel] PID {p.pid} finalizou e virou um ZUMBI.")
    else:
        p.estado = "PRONTO"
        # Move para o fim da lista para o Round Robin (Nível 2)
        tabela_processos.remove(p)
        tabela_processos.append(p)

# ==========================================
# INTERFACE COM O USUÁRIO (SHELL)
# ==========================================

def fork_process(pid_pai):
    """Nível 8: Clona um processo existente"""
    pai = next((p for p in tabela_processos if p.pid == pid_pai), None)
    if pai:
        filho = PCB(f"{pai.nome}_filho", pai=pai.pid, prioridade=pai.prioridade)
        tabela_processos.append(filho)
        print(f"[Kernel] Fork: {pai.pid} clonado para {filho.pid}")

def wait_process():
    """Nível 7: Coleta processos Zumbi da memória"""
    global tabela_processos
    antes = len(tabela_processos)
    tabela_processos = [p for p in tabela_processos if p.estado != "ZUMBI"]
    depois = len(tabela_processos)
    print(f"[Kernel] Wait: {antes - depois} processos Zumbi removidos.")

def shell():
    """Terminal interativo do PyOS"""
    global tabela_processos, recurso_em_uso_por
    
    while True:
        try:
            # Prompt estilizado
            entrada = input("\nroot@pyos:~# ").strip().split()
            if not entrada:
                continue
            
            acao = entrada[0].lower()
            comando = entrada
            
            if acao == "exit":
                print("Desligando PyOS...")
                sys.exit()

            elif acao == "help":
                print("\nComandos disponíveis:")
                print("spawn [nome] [pri] - Cria processo (limite 5)")
                print("ps                 - Lista processos e estados")
                print("run                - Execução automática total")
                print("cpu                - Executa 1 ciclo de clock")
                print("kill [PID]         - Remove um processo")
                print("block/unblock [PID]- Gerencia Espera de E/S")
                print("lock/unlock [PID]  - Uso de recurso (Mutex)")
                print("fork [PID]         - Clona um processo")
                print("wait               - Limpa processos ZUMBI")
                print("write [ref] [msg]  - Grava na memória IPC")
                print("read [ref]         - Lê da memória IPC")
                print("clear              - Limpa a tela")

            elif acao == "clear":
                print("\n" * 50)

            elif acao == "spawn":
                if len(comando) > 1:
                    nome = comando[1]
                    # Nível 4: Prioridade opcional (padrão 1)
                    pri = int(comando[2]) if len(comando) > 2 else 1
                    spawn_process(nome, pri)
                else:
                    print("Uso: spawn [nome] [prioridade]")

            elif acao == "ps":
                print(f"\n{'PID':<6} | {'NOME':<12} | {'ESTADO':<10} | {'PRI':<4} | {'RESTO'}")
                print("-" * 50)
                for p in tabela_processos:
                    print(f"{p.pid:<6} | {p.nome[:12]:<12} | {p.estado:<10} | {p.prioridade:<4} | {p.ciclos_restantes}")
                if not tabela_processos:
                    print("Memória RAM vazia.")

            elif acao == "run":
                print("[Kernel] Iniciando execução automática...")
                # Só roda enquanto existir alguém no estado PRONTO
                while any(p.estado == "PRONTO" for p in tabela_processos):
                    escalonador_tick()
                print("[Kernel] Execução pausada. Use 'ps' para ver os Zumbis ou 'wait' para limpar.")

            elif acao == "cpu":
                escalonador_tick()

            elif acao == "block":
                if len(comando) > 1:
                    pid = int(comando[1])
                    for p in tabela_processos:
                        if p.pid == pid:
                            p.estado = "BLOQUEADO"
                            print(f"[Kernel] PID {pid} bloqueado.")

            elif acao == "unblock":
                if len(comando) > 1:
                    pid = int(comando[1])
                    for p in tabela_processos:
                        if p.pid == pid:
                            p.estado = "PRONTO"
                            print(f"[Kernel] PID {pid} desbloqueado.")

            elif acao == "kill":
                if len(comando) > 1:
                    alvo = int(comando[1])
                    tabela_processos = [p for p in tabela_processos if p.pid != alvo]
                    print(f"[Kernel] PID {alvo} removido.")

            elif acao == "lock":
                if len(comando) > 1:
                    pid = int(comando[1])
                    if recurso_em_uso_por is None:
                        recurso_em_uso_por = pid
                        print(f"[Mutex] Recurso reservado para PID {pid}")
                    else:
                        print(f"[ALERTA] Conflito! Recurso em uso por PID {recurso_em_uso_por}")

            elif acao == "unlock":
                recurso_em_uso_por = None
                print("[Mutex] Recurso liberado.")

            elif acao == "fork":
                if len(comando) > 1:
                    fork_process(int(comando[1]))

            elif acao == "wait":
                wait_process()

            elif acao == "write":
                if len(comando) > 2:
                    chave = comando[1]
                    valor = " ".join(comando[2:])
                    espaco_ipc[chave] = valor
                    print(f"[IPC] Dados salvos em '{chave}'")

            elif acao == "read":
                if len(comando) > 1:
                    print(f"[IPC] Conteúdo de '{comando[1]}': {espaco_ipc.get(comando[1], 'Vazio')}")

            else:
                print(f"Comando '{acao}' não reconhecido.")

        except Exception as e:
            print(f"Erro de execução: {e}")
        except KeyboardInterrupt:
            print("\nUse 'exit' para encerrar.")

# ==========================================
# INÍCIO DO SISTEMA
# ==========================================

if __name__ == "__main__":
    boot()
    shell()