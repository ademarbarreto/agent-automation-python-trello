from google.adk.agents.llm_agent import Agent
from trello import trelloclient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

# Suas credenciais
API_KEY=os.getenv('TRELLO_API_KEY')
API_SECRET=os.getenv('TRELLO_API_SECRET')
TOKEN=os.getenv('TRELLO_TOKEN')

def get_temporal_context():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def adicionar_tarefa(nome_da_task: str, descricao: str, due_date: str):
    client = trelloclient.TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == "dio-ademar"), None)

    listas = meu_board.list_lists()
    minha_lista = [l for l in listas if l.name.upper() == "A FAZER" or l.name.upper() == "TO-DO"][0]

    # ✅ Corrige defasagem de 1 dia causada pelo UTC vs horário de Brasília (UTC-3)
    data = datetime.strptime(due_date, "%Y-%m-%d") + timedelta(days=1)
    due_date_corrigido = data.strftime("%Y-%m-%d")

    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao,
        due=due_date_corrigido
    )

def listar_tarefas(status: str):
    """
    Lista tarefas do Trello filtrando pelo status fornecido.

    Args:
        status (str): O status das tarefas a serem listadas (ex: "A FAZER", "EM ANDAMENTO", "CONCLUÍDO").
    """
    client = trelloclient.TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == "dio-ademar"), None)
    if not meu_board:
        return {"erro": "Board não encontrado."}

    listas = meu_board.list_lists()
    lista_filtrada = next((l for l in listas if l.name.upper() == status.upper()), None)
    if not lista_filtrada:
        return {"erro": f"Lista com status '{status}' não encontrada."}

    cards = lista_filtrada.list_cards()
    tarefas = [
        {
            "nome": card.name,
            "descricao": card.desc,
            "due_date": card.due,
            "id": card.id,
            "url": card.url,
        }
        for card in cards
    ]

    # ✅ Retorna as tarefas junto com o total
    return {
        "status": status,
        "total": len(tarefas),
        "tarefas": tarefas,
    }
 
def mudar_status_tarefa(nome_da_task: str, novo_status: str):
    """
    Move um card do Trello para uma lista diferente, alterando seu status.

    Args:
        nome_da_task (str): O nome exato do card a ser movido.
        novo_status (str): O nome da lista de destino (ex: "EM ANDAMENTO", "CONCLUÍDO").
    """
    client = trelloclient.TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = next((b for b in boards if b.name == "dio-ademar"), None)
    if not meu_board:
        return {"erro": "Board não encontrado."}

    listas = meu_board.list_lists()

    # Busca o card em todas as listas
    card_encontrado = None
    for lista in listas:
        cards = lista.list_cards()
        card_encontrado = next((c for c in cards if c.name.upper() == nome_da_task.upper()), None)
        if card_encontrado:
            break

    if not card_encontrado:
        return {"erro": f"Tarefa '{nome_da_task}' não encontrada em nenhuma lista."}

    # Busca a lista de destino
    lista_destino = next((l for l in listas if l.name.upper() == novo_status.upper()), None)
    if not lista_destino:
        return {"erro": f"Lista de destino '{novo_status}' não encontrada."}

    # Move o card
    card_encontrado.change_list(lista_destino.id)

    return {
        "sucesso": True,
        "tarefa": nome_da_task,
        "novo_status": novo_status,
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de oraganização de tarefas.',
    instruction='''
        Você é um agente de organização de tarefas. 
        Sua função é criar um card no Trello com o nome e a descrição da tarefa.
        Você deve perguntar as atividades que tenho no dia e criar um card para cada uma delas.
        Você inicia a conversa assim que ativado,perguntando quais são as tarefas do dia.
        Sempre inicie a conversa perguntando quais são as tarefas do dia informando a data pela tool get_temporal_context,
        e depois vá perguntando se tem mais alguma tarefa, até que o usuário diga que não tem mais tarefas.
        Suas funções:
        1. Adicionar novas tarefas com nome e descrição.
        2. Listar todas as tarefas ou filtrar por status.
        3. Marcar as tarefas como concluídas.
        4. Removar as tarefas da lista.
        5. Mudar o status da tarefa (ex. de "A fazer" para "Em andamento" e de "Em andamento" para "Concluído").
        6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia.
    ''',

    tools=[get_temporal_context, adicionar_tarefa,listar_tarefas,mudar_status_tarefa],
)