import socket
import threading
import os
import pygame
import emoji
from biblioteca.emoticons import meus_emojis  # biblioteca de emojis
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Entry, Label, Button, Frame
from tkinter import Toplevel, messagebox, StringVar, END, DISABLED, NORMAL

class ClienteChat:
    def __init__(self, root):
        self.root = root
        self.root.title("🟢 ChatApp - Cliente")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.client_socket = None
        self.nome_cliente = None
        self.categoria_atual = StringVar(value='Smile')

        pygame.mixer.init()
        self.caminho_ping = os.path.join('biblioteca', 'ping.wav')

        # Frame de entrada
        self.entry_frame = Frame(self.root, padding=20)
        self.entry_frame.pack()

        Label(self.entry_frame, text="Digite seu nome:", bootstyle="info").grid(row=0, column=0, pady=5, sticky="e")
        self.nome_entry = Entry(self.entry_frame, width=25)
        self.nome_entry.grid(row=0, column=1, pady=5)

        Label(self.entry_frame, text="IP do servidor:", bootstyle="info").grid(row=1, column=0, pady=5, sticky="e")
        self.ip_entry = Entry(self.entry_frame, width=25)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=1, column=1, pady=5)

        Label(self.entry_frame, text="Porta do servidor:", bootstyle="info").grid(row=2, column=0, pady=5, sticky="e")
        self.porta_entry = Entry(self.entry_frame, width=25)
        self.porta_entry.insert(0, "5050")
        self.porta_entry.grid(row=2, column=1, pady=5)

        self.connect_button = Button(self.entry_frame, text="Conectar", command=self.connect_to_server, width=20, bootstyle="success")
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame do chat principal
        self.chat_frame = Frame(self.root)
        
        # Painel esquerdo com usuários
        self.left_panel = Frame(self.chat_frame, padding=10)
        self.left_panel.pack(side='left', fill='y')

        Label(self.left_panel, text="Usuários Online", bootstyle="info").pack(anchor="w")
        self.user_listbox = ttk.Treeview(self.left_panel, height=25, show="headings", columns=["Usuários"], bootstyle="info")
        self.user_listbox.heading("#1", text="Usuário")
        self.user_listbox.pack(fill='y', expand=True, pady=5)

        # Painel direito com chat
        self.right_panel = Frame(self.chat_frame, padding=10)
        self.right_panel.pack(side='right', fill='both', expand=True)

        self.chat_display = ttk.Text(self.right_panel, height=22, width=60, wrap="word", state=DISABLED)
        self.chat_display.pack(pady=(0, 10))

        self.msg_entry = Entry(self.right_panel, width=58)
        self.msg_entry.pack(pady=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message_event)

        self.bottom_buttons = Frame(self.right_panel)
        self.bottom_buttons.pack()

        self.send_button = Button(self.bottom_buttons, text="Enviar", width=12, command=self.send_message, bootstyle="primary")
        self.send_button.pack(side='left', padx=5)

        self.emoji_button = Button(self.bottom_buttons, text="😀", width=3, command=self.abrir_teclado_emojis, bootstyle="warning")
        self.emoji_button.pack(side='left', padx=5)

    def connect_to_server(self):
        nome = self.nome_entry.get()
        ip = self.ip_entry.get()
        porta = self.porta_entry.get()

        if not nome or not ip or not porta:
            messagebox.showerror("Erro", "Por favor, preencha o nome, o IP e a porta.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, int(porta)))

            self.entry_frame.pack_forget()
            self.chat_frame.pack(fill='both', expand=True)

            self.client_socket.send(nome.encode())
            self.nome_cliente = nome
            self.connect_button.config(state=DISABLED)

            threading.Thread(target=self.listen_for_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")

    def send_message(self):
        msg = self.msg_entry.get()
        if msg:
            try:
                msg_com_emojis = emoji.emojize(msg)
                self.client_socket.send(msg_com_emojis.encode())
                self.chat_display.config(state=NORMAL)
                self.chat_display.insert(END, f"Você: {msg_com_emojis}\n")
                self.chat_display.see(END)
                self.chat_display.config(state=DISABLED)
                self.msg_entry.delete(0, END)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar mensagem: {e}")

    def send_message_event(self, event):
        self.send_message()

    def listen_for_messages(self):
        while True:
            try:
                dados = self.client_socket.recv(4096)
                if not dados:
                    break
                msg = dados.decode()

                # Separando a verificação de lista de usuários
                if msg.startswith("USER_LIST:"):
                    lista = msg.split(":", 1)[1].split(",")
                    self.atualizar_lista_usuarios(lista)
                    continue  # Não processa o restante da mensagem

                # Tratando mensagens de novos usuários e saída de usuários
                if msg.startswith("NEW_USER:"):
                    nome = msg.split(":", 1)[1]
                    msg = f"🌟 {nome} entrou no chat!"
                elif msg.startswith("EXIT_USER:"):
                    nome = msg.split(":", 1)[1]
                    msg = f"❌ {nome} saiu do chat."
            
                # Toca o som sempre que uma nova mensagem chegar
                self.tocar_som_ping()

                # Processa a mensagem com emojis
                msg_com_emojis = emoji.emojize(msg)
                self.chat_display.config(state=NORMAL)
                self.chat_display.insert(END, f"{msg_com_emojis}\n")
                self.chat_display.see(END)
                self.chat_display.config(state=DISABLED)

            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break

    def atualizar_lista_usuarios(self, usuarios):
        for item in self.user_listbox.get_children():
            self.user_listbox.delete(item)
        for nome in usuarios:
            self.user_listbox.insert("", "end", values=[nome])

    def abrir_teclado_emojis(self):
        self.janela_emoji = Toplevel(self.root)
        self.janela_emoji.title("Teclado de Emojis")

        self.categoria_frame = Frame(self.janela_emoji)
        self.categoria_frame.pack()

        self.emoji_frame = Frame(self.janela_emoji)
        self.emoji_frame.pack()

        categorias = {
            'Smile': '😄',
            'Corpo': '💪',
            'Animais': '🐶',
            'Comida': '🍕',
        }

        for nome, icone in categorias.items():
            botao = Button(self.categoria_frame, text=icone, command=lambda cat=nome: self.mostrar_emojis(cat), width=3)
            botao.pack(side='left', padx=5, pady=5)

        self.mostrar_emojis('Smile')

    def mostrar_emojis(self, categoria):
        for widget in self.emoji_frame.winfo_children():
            widget.destroy()

        emojis = emoji.emojize(meus_emojis(categoria))
        linha, coluna = 0, 0
        for e in emojis:
            botao = Button(self.emoji_frame, text=e, width=2, command=lambda emoji=e: self.inserir_emoji(emoji))
            botao.grid(row=linha, column=coluna, padx=2, pady=2)
            coluna += 1
            if coluna >= 10:
                coluna = 0
                linha += 1

    def inserir_emoji(self, emoji_char):
        self.msg_entry.insert(END, emoji_char)

    def tocar_som_ping(self):
        try:
            pygame.mixer.music.load(self.caminho_ping)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Erro ao tocar som: {e}")

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")  # Tema escuro
    ClienteChat(app)
    app.mainloop()
