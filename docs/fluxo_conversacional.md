# Fluxos Conversacionais — Som na Nuvem Chatbot

Este documento descreve todos os fluxos de conversa implementados no chatbot.

---

## Componentes Fundamentais

### Entity: `problema`
Extraída automaticamente do texto livre do usuário pelo modelo NLU (DIETClassifier).

| Valor da Entidade   | Exemplos de frases que a disparam                              |
|---------------------|----------------------------------------------------------------|
| `acesso_conta`      | "não consigo fazer login", "esqueci minha senha"               |
| `mudanca_plano`     | "quero mudar meu plano", "quais são os planos?"                |
| `falha_app`         | "o app não abre", "aplicativo travando"                        |
| `cancelamento`      | "quero cancelar minha assinatura"                              |
| `conteudo_ausente`  | "música sumiu", "playlist desapareceu"                         |
| `problema_pagamento`| "fui cobrado errado", "cartão recusado"                        |

### Slot: `problema`
Armazena o valor da entidade extraída e mantém o contexto durante toda a conversa. Preenchido automaticamente pelo mapeamento `from_entity`.

### Action: `action_fornecer_suporte`
Lógica central do chatbot:

```
action_fornecer_suporte(slot["problema"])
  │
  ├── SE requer_escalamento == True
  │     └── Envia mensagem pré-escalamento
  │         └── action_escalar_atendente()
  │
  └── SE requer_escalamento == False
        ├── Busca solução na knowledge_base
        ├── Formata resposta com passos / info de planos
        └── Envia resposta + pergunta se resolveu
```

---

## Fluxo Principal

```
Usuário envia mensagem
        │
        ▼
   [NLU Pipeline]
   Tokenização → Features → DIETClassifier
        │
        ▼
   Intent classificada + Entity extraída
   Ex: intent=relatar_problema_acesso
       entity=problema: "acesso_conta"
        │
        ▼
   [Rasa Core]
   Slot "problema" = "acesso_conta"
        │
        ▼
   [action_fornecer_suporte]
   Consulta knowledge_base["acesso_conta"]
        │
        ├── escalamento=False → Envia passos → Pergunta se resolveu
        │                           │
        │                    ┌──────┴──────┐
        │                    │             │
        │                 Resolveu     Não resolveu
        │                    │             │
        │                utter_ok    action_escalar_atendente
        │
        └── escalamento=True → Msg pré-escalamento → action_escalar_atendente
```

---

## Fluxos por Categoria

### Fluxo A — Acesso à Conta (Resolução Automática)
```
Usuário: "não consigo fazer login"
  ↓ NLU: intent=relatar_problema_acesso, entity=acesso_conta
  ↓ Slot preenchido: problema=acesso_conta
  ↓ action_fornecer_suporte → knowledge_base["acesso_conta"]
  ↓ Bot: Passos 1→5 para recuperar senha
  ↓ Bot: "Isso resolveu?"
  ↓ Usuário: "Sim"
  ↓ Bot: "Ótimo! Aproveite o Som na Nuvem!"
```

### Fluxo B — Cancelamento (Escalamento Automático)
```
Usuário: "quero cancelar minha assinatura"
  ↓ NLU: intent=relatar_cancelamento, entity=cancelamento
  ↓ Slot preenchido: problema=cancelamento
  ↓ action_fornecer_suporte → escalamento=True
  ↓ Bot: "Lamento saber... sabia que pode pausar por 3 meses?"
  ↓ action_escalar_atendente → Gera ticket #ABC123
  ↓ Bot: "Conectando com atendente... ticket #ABC123"
```

### Fluxo C — Fallback (Intent não reconhecida)
```
Usuário: "qual a previsão do tempo?"
  ↓ NLU: intent=fora_do_escopo (ou nlu_fallback se confiança < 70%)
  ↓ RulePolicy → utter_fora_do_escopo
  ↓ Bot: "Não entendi. Posso ajudar com acesso, planos, app..."
```

---

## Critérios de Escalamento

| Categoria          | Escalamento Automático | Motivo                                      |
|--------------------|------------------------|---------------------------------------------|
| `acesso_conta`     |   Não                  | Resolvível com instruções de senha          |
| `mudanca_plano`    |   Não                  | Informação pública, usuário faz sozinho     |
| `falha_app`        |   Não                  | Resolvível com troubleshooting padrão       |
| `conteudo_ausente` |   Não                  | Resolvível com cache/sync                   |
| `cancelamento`     |   Sim                  | Requer verificação de identidade            |
| `problema_pagamento|   Sim                  | Dados bancários exigem agente especializado |
| `outro`            |   Sim                  | Não categorizado — atendimento manual       |

---

## Diagrama de Estados do Slot `problema`

```
[vazio] → (entity extraída) → [preenchido com categoria]
                                        │
                          action_fornecer_suporte()
                                        │
                          ┌─────────────┴─────────────┐
                          │                           │
                    Não escala                    Escala
                          │                           │
                  Resposta + pergunta         action_escalar_atendente
                          │                           │
               ┌──────────┴──────────┐           [vazio] ← SlotSet reset
               │                    │
          Confirmou              Não confirmou
               │                    │
           utter_ok         utter_problema_nao_resolvido
                                    │
                            action_escalar_atendente
```
