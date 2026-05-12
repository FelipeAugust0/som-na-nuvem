# Som na Nuvem — Chatbot de Suporte

Chatbot inteligente de suporte ao assinante da plataforma de streaming de música **Som na Nuvem**, desenvolvido com [Rasa Open Source](https://rasa.com/).

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Base de Dados](#base-de-dados)
- [Fluxos Conversacionais](#fluxos-conversacionais)
- [Testes](#testes)
- [Equipe](#equipe)

---

## Visão Geral

A equipe de suporte do Som na Nuvem estava sobrecarregada com consultas repetitivas de assinantes. Este chatbot automatiza o atendimento de **primeiro nível**, identificando o problema do usuário, fornecendo soluções passo a passo e escalando para atendentes humanos quando necessário.

## Arquitetura

```
Usuário
   │
   ▼
[Interface (Web/App/WhatsApp)]
   │
   ▼
[Rasa NLU] ──► Identifica Intent + Extrai Entity "problema"
   │
   ▼
[Rasa Core] ──► Preenche Slot "problema" + Seleciona Action
   │
   ▼
[action_fornecer_suporte]
   │
   ├──► Base de Dados ──► Solução passo a passo
   │
   └──► Escalamento ──► Atendente Humano (fila)
```
---

### Componentes principais

- **Entity `problema`** — extrai o tipo de problema da mensagem do usuário
- **Slot `problema`** — armazena e mantém o contexto ao longo da conversa
- **Action `action_fornecer_suporte`** — consulta a base de dados e decide entre solução automática ou escalamento

---

### Problemas suportados

| Categoria | Exemplos de frases |
|---|---|
| `acesso_conta` | "não consigo fazer login", "esqueci minha senha", "conta bloqueada" |
| `mudanca_plano` | "quero mudar meu plano", "ver planos disponíveis", "upgrade de assinatura" |
| `falha_app` | "o app não abre", "aplicativo travando", "erro no app" |
| `cancelamento` | "quero cancelar", "encerrar assinatura" |
| `conteudo_ausente` | "música sumiu", "playlist desapareceu", "não encontro meu álbum" |
| `problema_pagamento` | "cobrança errada", "não consigo pagar", "cartão recusado" |

---

## Estrutura do Projeto

```
som-na-nuvem-chatbot/
│
├── domain/
│   └── domain.yml              # Entidades, slots, actions, respostas
│
├── nlu/
│   └── nlu.yml                 # Dados de treinamento NLU
│
├── data/
│   ├── stories.yml             # Histórias de treinamento (fluxos)
│   └── rules.yml               # Regras determinísticas
│
├── actions/
│   ├── action_fornecer_suporte.py   # Action principal
│   └── knowledge_base.py            # Base de dados de soluções
│
├── tests/
│   └── test_stories.yml        # Histórias de teste
│
├── docs/
│   └── fluxo_conversacional.md # Documentação dos fluxos
│
├── config.yml                  # Configuração do pipeline NLU + políticas
├── endpoints.yml               # Endpoints do servidor de actions
├── credentials.yml             # Canais de comunicação
└── README.md
```

---

## Instalação

### Pré-requisitos

- Python 3.8+
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/FelipeAugust0/som-na-nuvem.git
cd som-na-nuvem

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install rasa==3.6.0
pip install rasa-sdk==3.6.0

# 4. Treine o modelo
rasa train

# 5. Inicie o servidor de actions (terminal separado)
rasa run actions

# 6. Inicie o chatbot
rasa shell
```

---

## Como Usar

### Modo shell (linha de comando)

```bash
rasa shell
```

### Modo API REST

```bash
rasa run --enable-api --cors "*"
```

Envie requisições POST para `http://localhost:5005/webhooks/rest/webhook`:

```json
{
  "sender": "usuario_123",
  "message": "não consigo acessar minha conta"
}
```

---

## Base de Dados

A base de dados (`actions/knowledge_base.py`) contém soluções estruturadas para cada categoria de problema:

```python
KNOWLEDGE_BASE = {
    "acesso_conta": {
        "titulo": "Recuperação de acesso",
        "passos": [...],
        "escalamento": False
    },
    "cancelamento": {
        "escalamento": True,
        "motivo": "Requer verificação de identidade"
    },
    ...
}
```

---

## Fluxos Conversacionais

Veja a documentação completa em [`docs/fluxo_conversacional.md`](docs/fluxo_conversacional.md).

Fluxo principal:

```
saudação → identificar_problema → fornecer_suporte → confirmar_resolução
                                                    └─► escalar_humano
```

---

## Testes

```bash
# Executar todos os testes
rasa test

# Testar apenas o NLU
rasa test nlu

# Testar histórias de conversação
rasa test core
```

---

## Equipe

Projeto desenvolvido como solução acadêmica para a disciplina de Chatbots e Processamento de Linguagem Natural.

---

## Licença

MIT License — veja o arquivo [LICENSE](LICENSE) para detalhes.
