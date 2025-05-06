# Aplicação de Chat

Este projeto é uma aplicação de chat desenvolvida em Python, com implementações de servidor e cliente. Siga os passos abaixo para configurar o ambiente virtual e instalar as dependências necessárias.

## Pré-requisitos

- Python 3.8 ou superior instalado no sistema.
- `pip` (gerenciador de pacotes do Python) instalado.

## Configurando o Ambiente Virtual

1. **Criar o Ambiente Virtual**:
   No diretório do projeto, execute o seguinte comando no terminal:
   ```bash
   python3 -m venv venv
   ```

2. **Ativar o Ambiente Virtual**:
   - No macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - No Windows (cmd):
     ```cmd
     venv\Scripts\activate
     ```
   - No Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

3. **Instalar as Dependências**:
   Com o ambiente virtual ativado, instale os pacotes necessários:
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o Servidor**:
   No terminal, execute:
   ```bash
   python servidor.py
   ```

5. **Executar o Cliente**:
   Em outro terminal (com o ambiente virtual ativado), execute:
   ```bash
   python cliente.py
   ```

6. **Desativar o Ambiente Virtual**:
   Após o uso, você pode desativar o ambiente virtual com:
   ```bash
   deactivate
   ```

## Observações

- Certifique-se de que o servidor esteja em execução antes de iniciar qualquer cliente.
- O cliente possui uma interface gráfica desenvolvida com `pygame` e `ttkbootstrap`, enquanto a troca de mensagens utiliza sockets TCP.
