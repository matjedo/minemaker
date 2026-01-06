import os
import shutil
import subprocess
import threading
from file_manager import abrir_gerenciador

SERVERS_DIR = "servers"
processos = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print("=" * 55)
    print("              Mine Maker - v0.4")
    print("      Host local e gerenciador de servidores")
    print("=" * 55)

def listar_servidores():
    if not os.path.exists(SERVERS_DIR):
        return []
    return [
        d for d in os.listdir(SERVERS_DIR)
        if os.path.isdir(os.path.join(SERVERS_DIR, d))
    ]

def criar_servidor():
    clear()
    header()

    nome = input("Nome do servidor: ").strip()
    pasta = os.path.join(SERVERS_DIR, nome)
    os.makedirs(pasta, exist_ok=True)

    jar = input("Caminho do server.jar: ").strip()
    if not os.path.isfile(jar):
        print("❌ server.jar não encontrado.")
        input("ENTER...")
        return

    shutil.copy(jar, os.path.join(pasta, "server.jar"))

    with open(os.path.join(pasta, "eula.txt"), "w") as f:
        f.write("eula=true\n")

    print("✅ Servidor criado com sucesso!")
    input("ENTER...")

def iniciar_servidor(nome):
    pasta = os.path.join(SERVERS_DIR, nome)
    jar = os.path.join(pasta, "server.jar")

    if nome in processos:
        print("⚠️ Servidor já está ligado.")
        return

    if not os.path.exists(jar):
        print("❌ server.jar não encontrado.")
        return

    proc = subprocess.Popen(
        ["java", "-jar", "server.jar", "nogui"],
        cwd=pasta,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    processos[nome] = proc

    def log_reader():
        for line in proc.stdout:
            print(line, end="")

    threading.Thread(target=log_reader, daemon=True).start()
    print("▶️ Servidor iniciado.")

def console_servidor(nome):
    proc = processos.get(nome)
    if not proc:
        print("❌ Servidor não está ligado.")
        input("ENTER...")
        return

    clear()
    print(f"📟 Console do servidor: {nome}")
    print("Digite comandos (/gm1, /say, etc)")
    print("Digite 'exit' para voltar ao menu\n")

    while True:
        cmd = input()
        if cmd.lower() == "exit":
            break
        try:
            proc.stdin.write(cmd + "\n")
            proc.stdin.flush()
        except:
            print("❌ Erro ao enviar comando.")
            break

def parar_servidor(nome):
    proc = processos.get(nome)
    if not proc:
        print("❌ Servidor não está ligado.")
        return

    proc.stdin.write("stop\n")
    proc.stdin.flush()
    proc.wait()
    processos.pop(nome)
    print("⏹️ Servidor parado com segurança.")

def matar_servidor(nome):
    proc = processos.get(nome)
    if not proc:
        print("❌ Servidor não está ligado.")
        return

    proc.terminate()
    processos.pop(nome)
    print("☠️ Servidor encerrado à força.")

def deletar_servidor(nome):
    pasta = os.path.join(SERVERS_DIR, nome)

    print("\n⚠️ ATENÇÃO ⚠️")
    print("Isso irá APAGAR o servidor PERMANENTEMENTE.")
    print("Mundos, plugins e configs serão perdidos.")
    confirm = input(f"Digite '{nome}' para confirmar: ")

    if confirm != nome:
        print("❌ Nome incorreto. Cancelado.")
        return

    if nome in processos:
        matar_servidor(nome)

    shutil.rmtree(pasta)
    print("🗑️ Servidor deletado com sucesso.")

def menu_servidores():
    servidores = listar_servidores()
    if not servidores:
        print("Nenhum servidor encontrado.")
        input("ENTER...")
        return

    for i, s in enumerate(servidores, 1):
        status = "ON" if s in processos else "OFF"
        print(f"{i} - {s} [{status}]")

    escolha = input("> ")
    if not escolha.isdigit():
        return

    nome = servidores[int(escolha) - 1]

    print("\n1 - Ligar servidor")
    print("2 - Console do servidor")
    print("3 - Parar servidor")
    print("4 - Matar servidor (FORÇA)")
    print("5 - Deletar servidor ⚠️")
    print("6 - Gerenciar arquivos (GUI)")
    print("7 - Voltar")

    op = input("> ")

    if op == "1":
        iniciar_servidor(nome)
    elif op == "2":
        console_servidor(nome)
    elif op == "3":
        parar_servidor(nome)
    elif op == "4":
        matar_servidor(nome)
    elif op == "5":
        deletar_servidor(nome)
    elif op == "6":
        abrir_gerenciador(os.path.join(SERVERS_DIR, nome))

    input("\nENTER...")

def menu():
    while True:
        clear()
        header()
        print("1 - Criar servidor")
        print("2 - Gerenciar servidores")
        print("3 - Sair")

        op = input("> ")

        if op == "1":
            criar_servidor()
        elif op == "2":
            menu_servidores()
        elif op == "3":
            break

if __name__ == "__main__":
    menu()
