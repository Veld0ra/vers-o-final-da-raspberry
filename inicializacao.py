import requests
import time
from datetime import datetime

URL = "https://cliente-clound.onrender.com"

URL_USUARIOS = f"{URL}/usuarios"
URL_NOVO = f"{URL}/novo-usuario"
URL_LOGIN = f"{URL}/login"


# =========================
# LISTAR USUÁRIOS
# =========================
def listar_usuarios():

    try:

        r = requests.get(
            URL_USUARIOS,
            timeout=10
        )

        if r.status_code != 200:
            return []

        return r.json()

    except Exception as e:

        print("Erro ao buscar usuários:", e)

        return []


# =========================
# CRIAR USUÁRIO
# =========================
def criar_usuario():

    print("\n==================")
    print("NOVO USUÁRIO")
    print("==================\n")

    nome = input("Nome: ").strip()
    pronome = input("Pronome: ").strip()
    memoria = input("Fale sobre você: ").strip()

    if not nome:

        print("Nome inválido.")
        return None

    try:

        r = requests.post(
            URL_NOVO,
            json={
                "nome": nome,
                "pronome": pronome,
                "memoria": memoria
            },
            timeout=10
        )

        dados = r.json()

        if "erro" in dados:

            print(dados["erro"])
            return None

        print("\n✓ Usuário criado com sucesso.\n")

        return {
            "id": None,
            "nome": nome,
            "pronome": pronome,
            "memoria": memoria,
            "tipo": "usuario"
        }

    except Exception as e:

        print("Erro ao criar usuário:", e)

        return None


# =========================
# LOGIN
# =========================
def login_usuario():

    usuarios = listar_usuarios()

    if not usuarios:

        print("\nNenhum usuário encontrado.\n")

        return None

    usuarios = sorted(
        usuarios,
        key=lambda u: u["id"]
    )

    print("\n==================")
    print("USUÁRIOS CADASTRADOS")
    print("==================\n")

    for u in usuarios:
        print(f"[{u['id']}] {u['nome']}")

    print("\n[0] Voltar\n")

    escolha = input("> ").strip()

    if escolha == "0":
        return None

    usuario = next(
        (
            u
            for u in usuarios
            if str(u["id"]) == escolha
        ),
        None
    )

    if not usuario:

        print("Usuário não encontrado.")

        return None

    try:

        r = requests.post(
            URL_LOGIN,
            json={
                "nome": usuario["nome"]
            },
            timeout=10
        )

        dados = r.json()

        if "erro" in dados:

            print(dados["erro"])

            return None

        print("\nCarregando perfil...")
        time.sleep(1)

        print(
            f"✓ Bem-vindo(a), "
            f"{dados['nome']}.\n"
        )

        return dados

    except Exception as e:

        print("Erro no login:", e)

        return None


# =========================
# VISITANTE
# =========================
def modo_visitante():

    print("\n==================")
    print("MODO VISITANTE")
    print("==================\n")

    print(
        "Nenhuma memória será salva.\n"
    )

    input("Continuar? (Enter) ")

    return {
        "id": None,
        "nome": "Visitante",
        "pronome": "não informado",
        "memoria": "",
        "tipo": "visitante"
    }


# =========================
# BOOT DA SEMA
# =========================
def tela_boot():

    agora = datetime.now()

    print("\nSEMA INICIANDO...\n")

    print("Verificando sistemas...")
    time.sleep(0.5)

    print("✓ Núcleo carregado")
    time.sleep(0.5)

    print("✓ Conexão estabelecida")
    time.sleep(0.5)

    if agora.hour < 12:
        saudacao = "Bom dia"
    elif agora.hour < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    print()
    print(f"{saudacao}!")
    print(f"Hoje é {agora.strftime('%d/%m/%Y')}")
    print(f"São {agora.strftime('%H:%M')}.\n")

    print("Pronta para auxiliar.\n")


# =========================
# MENU DE USUÁRIO
# =========================
def selecionar_usuario():

    while True:

        print("==================")
        print("USUÁRIO")
        print("==================\n")

        print("[1] Usuário conhecido")
        print("[2] Cadastrar novo usuário")
        print("[3] Modo visitante\n")

        escolha = input("> ").strip()

        if escolha == "1":

            usuario = login_usuario()

            if usuario:
                return usuario

        elif escolha == "2":

            usuario = criar_usuario()

            if usuario:
                return usuario

        elif escolha == "3":

            return modo_visitante()

        else:

            print("\nOpção inválida.\n")


# =========================
# INICIAR SESSÃO
# =========================
def iniciar_sessao():

    tela_boot()

    return selecionar_usuario()
