import socket
import threading
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import requests

clientes = []
nomes = []

def detectar_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def detectar_ip_publico():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Não disponível"

def broadcast(mensagem, remetente, listbox_usuarios=None):
    for c in clientes:
        if c != remetente:
            try:
                c.sendall(mensagem.encode())
            except:
                c.close()
                if c in clientes:
                    clientes.remove(c)

    # Atualiza a lista de usuários online para todos os clientes
    if listbox_usuarios:
        usuarios = ",".join(nomes)
        for c in clientes:
            try:
                c.sendall(f"USER_LIST:{usuarios}".encode())
            except:
                c.close()
                if c in clientes:
                    clientes.remove(c)

def lidar_com_cliente(cliente, endereco, lista_texto=None, listbox_usuarios=None):
    try:
        nome = cliente.recv(1024).decode().strip()
        nomes.append(nome)
        clientes.append(cliente)

        entrada_msg = f"✅ {nome} ({endereco[0]}:{endereco[1]}) entrou no chat.\n"
        if lista_texto:
            lista_texto.insert(tk.END, entrada_msg)
        else:
            print(entrada_msg.strip())
        if listbox_usuarios:
            listbox_usuarios.insert(tk.END, nome)

        broadcast(f"🌟 {nome} entrou no chat!", cliente, listbox_usuarios)

        while True:
            dados = cliente.recv(1024)
            if not dados:
                break
            mensagem = dados.decode()
            exibir_msg = f"{nome}: {mensagem}"
            if lista_texto:
                lista_texto.insert(tk.END, exibir_msg + "\n")
            else:
                print(exibir_msg)
            broadcast(exibir_msg, cliente, listbox_usuarios)

    except Exception as e:
        print(f"⚠️ Erro com cliente {endereco}: {e}")
    finally:
        if cliente in clientes:
            clientes.remove(cliente)
        if nome in nomes:
            nomes.remove(nome)
        if listbox_usuarios:
            try:
                listbox_usuarios.delete(listbox_usuarios.get(0, tk.END).index(nome))
            except ValueError:
                pass
        saida_msg = f"❌ {nome} ({endereco[0]}:{endereco[1]}) saiu do chat.\n"
        if lista_texto:
            lista_texto.insert(tk.END, saida_msg)
        else:
            print(saida_msg.strip())
        broadcast(f"❌ {nome} saiu do chat.", cliente, listbox_usuarios)
        cliente.close()

def iniciar_servidor(ip, porta, lista_texto=None, botao_iniciar=None, listbox_usuarios=None):
    try:
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((ip, porta))
        servidor.listen(10)

        if lista_texto:
            lista_texto.insert(tk.END, f"🚀 Servidor iniciado em {ip}:{porta}. Aguardando conexões...\n")
        else:
            print(f"🚀 Servidor iniciado em {ip}:{porta}. Aguardando conexões...")

        if botao_iniciar:
            botao_iniciar.config(state=tk.DISABLED)

        def aceitar_conexoes():
            while True:
                cliente, endereco = servidor.accept()
                threading.Thread(target=lidar_com_cliente, args=(cliente, endereco, lista_texto, listbox_usuarios), daemon=True).start()

        threading.Thread(target=aceitar_conexoes, daemon=True).start()
    except Exception as e:
        msg = f"❌ Erro ao iniciar o servidor: {e}\n"
        if lista_texto:
            lista_texto.insert(tk.END, msg)
        else:
            print(msg)
        if botao_iniciar:
            botao_iniciar.config(state=tk.NORMAL)

def criar_interface():
    style = Style(theme="flatly")
    root = style.master
    root.title("Servidor de Chat")
    root.geometry("600x500")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    label_ip = ttk.Label(frame, text="IP do Servidor:")
    label_ip.pack(anchor="w")

    ip_frame = ttk.Frame(frame)
    ip_frame.pack(fill=tk.X, pady=5)

    entry_ip = ttk.Entry(ip_frame)
    entry_ip.insert(0, "0.0.0.0")
    entry_ip.pack(side=tk.LEFT, fill=tk.X, expand=True)

    btn_detectar_ip = ttk.Button(ip_frame, text="IP Local", width=12,
                                  command=lambda: entry_ip.delete(0, tk.END) or entry_ip.insert(0, detectar_ip_local()))
    btn_detectar_ip.pack(side=tk.RIGHT, padx=5)

    label_publico = ttk.Label(frame, text=f"🌐 IP Público: {detectar_ip_publico()}")
    label_publico.pack(anchor="w", pady=(0, 5))

    label_porta = ttk.Label(frame, text="Porta do Servidor:")
    label_porta.pack(anchor="w")

    entry_porta = ttk.Entry(frame)
    entry_porta.insert(0, "5050")
    entry_porta.pack(fill=tk.X, pady=(0, 5))

    botao_iniciar = ttk.Button(
        frame,
        text="Iniciar Servidor",
        command=lambda: iniciar_servidor(entry_ip.get().strip(), int(entry_porta.get()), lista_texto, botao_iniciar, listbox_usuarios)
    )
    botao_iniciar.pack(pady=(0, 10), fill=tk.X)

    lista_texto = tk.Text(frame, height=12, wrap=tk.WORD)
    lista_texto.pack(fill=tk.BOTH, expand=True)

    label_usuarios = ttk.Label(frame, text="Usuários Online:")
    label_usuarios.pack(anchor="w", pady=(5, 0))

    listbox_usuarios = tk.Listbox(frame, height=6)
    listbox_usuarios.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

def iniciar_modo_terminal():
    host = input("IP do servidor (deixe em branco para 0.0.0.0): ").strip() or "0.0.0.0"
    porta = input("Porta (padrão 5050): ").strip()
    porta = int(porta) if porta else 5050
    iniciar_servidor(host, porta)

if __name__ == "__main__":
    modo = input("Escolha o modo [1] Interface Gráfica | [2] Terminal: ").strip()
    if modo == "1":
        criar_interface()
    else:
        iniciar_modo_terminal()
