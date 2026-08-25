"""
seed_data.py — popula o banco tracker.db com casos de teste e bugs de exemplo.
Rodar depois de criar o schema: python seed_data.py
"""
import sqlite3

conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

# Casos de teste de exemplo
test_cases = [
    (
        "Login com credenciais válidas",
        "Usuário cadastrado e ativo no sistema",
        "1. Acessar a tela de login\n2. Inserir usuário e senha válidos\n3. Clicar em 'Entrar'",
        "Usuário é redirecionado para o dashboard com sessão ativa",
        "passed",
    ),
    (
        "Login com senha incorreta",
        "Usuário cadastrado no sistema",
        "1. Acessar a tela de login\n2. Inserir usuário válido e senha incorreta\n3. Clicar em 'Entrar'",
        "Sistema exibe mensagem de erro e não realiza login",
        "failed",
    ),
    (
        "Criação de reserva com datas inválidas",
        "Usuário autenticado no sistema de reservas",
        "1. Selecionar hotel\n2. Informar check-out anterior ao check-in\n3. Confirmar reserva",
        "Sistema deve bloquear a reserva e exibir mensagem de validação",
        "failed",
    ),
    (
        "Consulta de disponibilidade de quartos",
        "Hotel cadastrado com quartos disponíveis",
        "1. Selecionar hotel e período\n2. Consultar disponibilidade",
        "Sistema retorna lista de tipos de quarto com unidades disponíveis",
        "passed",
    ),
    (
        "Cancelamento de reserva confirmada",
        "Reserva existente com status 'confirmed'",
        "1. Acessar reserva\n2. Clicar em 'Cancelar'\n3. Confirmar ação",
        "Status da reserva muda para 'cancelled'",
        "not_run",
    ),
]

cur.executemany(
    """INSERT INTO test_cases (title, preconditions, steps, expected_result, status)
       VALUES (?, ?, ?, ?, ?)""",
    test_cases,
)

# Bugs de exemplo (alguns vinculados a casos de teste que falharam)
bugs = [
    (
        "Login aceita senha incorreta em alguns casos",
        "Ao inserir senha incorreta com determinados caracteres especiais, o sistema autentica o usuário indevidamente.",
        "critical",
        "open",
        "1. Acessar login\n2. Inserir usuário válido\n3. Inserir senha incorreta contendo caractere ';'\n4. Clicar em Entrar",
        "Produção - Chrome 126",
        2,
    ),
    (
        "Reserva com check-out anterior ao check-in é aceita",
        "O sistema não valida a ordem das datas ao criar uma reserva, permitindo salvar dados inconsistentes.",
        "high",
        "in_progress",
        "1. Criar nova reserva\n2. Informar check-in 10/09 e check-out 08/09\n3. Confirmar",
        "Staging - API v1",
        3,
    ),
    (
        "Botão 'Cancelar reserva' sem confirmação visual",
        "Após cancelar uma reserva, a tela não exibe nenhuma mensagem de sucesso, gerando dúvida se a ação foi concluída.",
        "low",
        "open",
        "1. Acessar reserva confirmada\n2. Clicar em Cancelar\n3. Confirmar ação",
        "Produção - Firefox 128",
        5,
    ),
    (
        "Disponibilidade não atualiza em tempo real",
        "Após uma reserva ser criada, a consulta de disponibilidade em outra aba ainda mostra a unidade como livre por ~2 minutos.",
        "medium",
        "resolved",
        "1. Abrir consulta de disponibilidade em duas abas\n2. Criar reserva em uma delas\n3. Atualizar a outra aba",
        "Produção - cache de API",
        4,
    ),
]

cur.executemany(
    """INSERT INTO bugs (title, description, severity, status, steps_to_reproduce, environment, test_case_id)
       VALUES (?, ?, ?, ?, ?, ?, ?)""",
    bugs,
)

conn.commit()
conn.close()

print("Banco populado com sucesso: 5 casos de teste e 4 bugs.")
