# 🤖 Agente de Organização de Tarefas com Google ADK + Trello

Projeto desenvolvido como parte do desafio da [Digital Innovation One (DIO)](https://www.dio.me/), utilizando o **Google Agent Development Kit (ADK)** com o modelo **Gemini 2.5 Flash** para criar um agente inteligente de gerenciamento de tarefas integrado ao **Trello**.

---

## 📌 Descrição do Projeto

Este agente conversacional automatiza o gerenciamento de tarefas no Trello por meio de linguagem natural. Ao ser ativado, ele pergunta quais são as tarefas do dia, cria os cards automaticamente e permite gerenciá-los ao longo do tempo — tudo via conversa.

---

## 🚀 Funcionalidades

| Função | Descrição |
|---|---|
| `get_temporal_context` | Retorna a data e hora atual para contextualizar as tarefas do dia |
| `adicionar_tarefa` | Cria um novo card na lista "A FAZER" do board Trello |
| `listar_tarefas` | Lista os cards filtrando por status, com o total de tarefas encontradas |
| `mudar_status_tarefa` | Move um card entre listas (ex: "A FAZER" → "EM ANDAMENTO" → "CONCLUÍDO") |

---

## 🧠 Arquitetura

```
Usuário (linguagem natural)
        │
        ▼
  Google ADK Agent
  (Gemini 2.5 Flash)
        │
        ├──► get_temporal_context()
        ├──► adicionar_tarefa()
        ├──► listar_tarefas()
        └──► mudar_status_tarefa()
                │
                ▼
          Trello API (py-trello)
                │
                ▼
          Board "dio-ademar"
```

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- [Gemini 2.5 Flash](https://deepmind.google/technologies/gemini/)
- [py-trello](https://github.com/sarumont/py-trello)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚙️ Como Executar

### 1. Pré-requisitos

- Python 3.11 ou superior
- Conta no [Trello](https://trello.com) com um board criado
- Credenciais da API do Trello ([veja o guia de configuração](#-configuração-das-credenciais-do-trello))
- Chave de API do Google (Gemini)

### 2. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 3. Instale as dependências

```bash
pip install google-adk py-trello python-dotenv
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
TRELLO_API_KEY=sua_api_key
TRELLO_API_SECRET=seu_api_secret
TRELLO_TOKEN=seu_token
GOOGLE_API_KEY=sua_google_api_key
```

### 5. Execute o agente

```bash
adk run web
```

---

## 🔑 Configuração das Credenciais do Trello

✅ Acesse [https://trello.com/app-key](https://trello.com/app-key) para obter sua **API Key** e **API Secret**.

✅Gere o **Token** de acesso clicando em "Token" na mesma página.

✅Certifique-se de que o seu board no Trello se chama **`dio-ademar`** e contém as listas:
   - `A FAZER`
   - `EM ANDAMENTO`
   - `CONCLUÍDO`


---

## 💬 Exemplo de Uso


![Getting Started](./Images/ADE%20Telas%20de%20tarefas%20A%20FAZER.png)

---

## 🐛 Problemas Conhecidos e Soluções

### `Cannot serialize unknown type: <class 'trello.card.Card'>`
O Google ADK exige que as ferramentas retornem tipos serializáveis em JSON. A solução foi converter os objetos `Card` da biblioteca `py-trello` em dicionários Python antes de retornar.

### `503 UNAVAILABLE — High demand`
Erro temporário da API do Gemini. Aguarde alguns minutos e tente novamente, ou use `gemini-2.0-flash` como alternativa.

### `401 Unauthorized (JWT)`
Se estiver usando FastAPI com autenticação JWT em paralelo, certifique-se de que o campo `sub` do token seja uma `string` — o PyJWT 2.x rejeita valores inteiros.

---

## 📄 Imagens capturadas

#### ✅ Evidência do AGENTE com as tarefas "A FAZER"


![Getting Started](./Images/ADE%20Telas%20de%20tarefas%20A%20FAZER.png)


#### ✅ Evidências do AGENTE com a tarefa Ir ao dentista "CONCLUÍDO"


![Getting Started](./Images/ADK%20Ir%20ao%20dentista%20CONCLUÍDO.png)


#### ✅ Evidência de tarefas a fazer no TRELLO


![Getting Started](./Images/ADK%20TRELLO%20A%20FAZER.png)


#### ✅ Evidência de tarefas de de Ir ao dentista "EM ANDAMENTO"


![Getting Started](./Images/ADK%20TRELLO%20Ir%20ao%20dentista%20EM%20ANDAMENTO.png)


#### ✅ Evidência de tarefas de Ir ao dentista "CONCLUÍDO"


![Getting Started](./Images/ADK%20TRELLO%20Ir%20ao%20dentista%20CONCLUÍDO.png)


---

## 👨‍💻 Autor

#### Desenvolvido como parte do bootcamp da [DIO — Digital Innovation One](https://www.dio.me/).

#### Autor: LinkedIn (https://www.linkedin.com/in/ademarsilvabarretojunior/)
