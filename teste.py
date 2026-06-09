import os
import requests
from datetime import datetime
from inicializacao import iniciar_sessao, selecionar_usuario

BASE_URL = "https://cliente-clound.onrender.com"


# =========================
# UTILIDADES
# =========================
def limpar_tela():
    os.system("clear")


def mostrar_saudacao(usuario):
    hora = datetime.now().hour

    if hora < 12:
        saudacao = "Bom dia"
    elif hora < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    print(f"\n{saudacao}, {usuario['nome']}.")
    print("No que posso auxiliar hoje?\n")


def encerrar_sessao(usuario):
    """Envia comando /sair para salvar memória no backend"""
    try:
        r = requests.post(
            f"{BASE_URL}/chat",
            json={
                "texto": "/sair",
                "id": usuario.get("id"),
                "nome": usuario["nome"],
                "pronome": usuario["pronome"],
                "memoria": usuario["memoria"],
                "tipo": usuario["tipo"]
            },
            timeout=30
        )

        resposta = r.json().get("resposta", "")
        print("SEMA:", resposta)

    except Exception as e:
        print("Erro ao encerrar sessão:", e)


def trocar_usuario(usuario):
    print("\nSalvando conversa atual...\n")

    encerrar_sessao(usuario)

    novo_usuario = selecionar_usuario()

    limpar_tela()
    mostrar_saudacao(novo_usuario)

    return novo_usuario


# =========================
# LOGIN INICIAL
# =========================
usuario = iniciar_sessao()

limpar_tela()
mostrar_saudacao(usuario)


# =========================
# CHAT LOOP
# =========================
while True:

    texto = input("Você: ").strip()

    if not texto:
        continue

    # =========================
    # TROCAR USUÁRIO
    # =========================
    if texto.lower() == "/trocar usuario":
        usuario = trocar_usuario(usuario)
        continue

    # =========================
    # SAIR DO PROGRAMA
    # =========================
    if texto.lower() == "/sair":
        encerrar_sessao(usuario)
        print("Encerrando...")
        break

    # =========================
    # CHAT NORMAL
    # =========================
    try:
        r = requests.post(
            f"{BASE_URL}/chat",
            json={
                "texto": texto,
                "id": usuario.get("id"),
                "nome": usuario["nome"],
                "pronome": usuario["pronome"],
                "memoria": usuario["memoria"],
                "tipo": usuario["tipo"]
            },
            timeout=30
        )

        resposta = r.json().get("resposta", "")

    except Exception as e:
        resposta = f"Erro de conexão: {e}"

    print("SEMA:", resposta)
