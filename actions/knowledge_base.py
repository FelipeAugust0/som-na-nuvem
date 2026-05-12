"""
knowledge_base.py
─────────────────
Base de dados de soluções do chatbot Som na Nuvem.

Contém informações sobre problemas comuns, soluções passo a passo,
informações sobre planos e critérios de escalamento para atendente humano.
"""

# ──────────────────────────────────────────────────────────────────
# BASE DE CONHECIMENTO PRINCIPAL
# Mapeamento: tipo de problema → solução / escalamento
# ──────────────────────────────────────────────────────────────────

KNOWLEDGE_BASE = {

    # ────────────────────────────────────────
    # ACESSO À CONTA
    # ────────────────────────────────────────
    "acesso_conta": {
        "titulo": "Recuperação de acesso à conta",
        "escalamento": False,
        "passos": [
            "Acesse **som-na-nuvem.com** e clique em **'Entrar'**",
            "Clique em **'Esqueci minha senha'**",
            "Digite o **e-mail cadastrado** na sua conta",
            "Verifique sua **caixa de entrada** (verifique também a pasta de spam)",
            "Clique no link recebido e **crie uma nova senha**",
        ],
        "dica": "Dica: Sua senha deve ter pelo menos 8 caracteres, com letras e números.",
        "link_ajuda": "https://ajuda.som-na-nuvem.com/acesso",
        "tempo_estimado": "2 minutos",
    },

    # ────────────────────────────────────────
    # MUDANÇA DE PLANO
    # ────────────────────────────────────────
    "mudanca_plano": {
        "titulo": "Planos disponíveis",
        "escalamento": False,
        "info_planos": [
            {
                "nome": "Básico",
                "preco": "R$ 14,90/mês",
                "dispositivos": 1,
                "perfis": 1,
                "downloads": False,
                "qualidade": "Alta (320kbps)",
            },
            {
                "nome": "Família",
                "preco": "R$ 24,90/mês",
                "dispositivos": 3,
                "perfis": 6,
                "downloads": True,
                "qualidade": "Alta (320kbps)",
            },
            {
                "nome": "Estudante",
                "preco": "R$ 9,90/mês",
                "dispositivos": 1,
                "perfis": 1,
                "downloads": True,
                "qualidade": "Alta (320kbps)",
                "obs": "Requer comprovante de matrícula",
            },
        ],
        "como_mudar": [
            "Acesse o app ou site do Som na Nuvem",
            "Vá em **Configurações → Assinatura**",
            "Clique em **'Alterar plano'**",
            "Escolha o novo plano e confirme",
        ],
        "link_ajuda": "https://ajuda.som-na-nuvem.com/planos",
        "tempo_estimado": "3 minutos",
    },

    # ────────────────────────────────────────
    # FALHA NO APLICATIVO
    # ────────────────────────────────────────
    "falha_app": {
        "titulo": "Corrigindo problemas no aplicativo",
        "escalamento": False,
        "passos": [
            "**Feche completamente** o aplicativo e reabra",
            "Verifique se sua **conexão com a internet** está funcionando",
            "**Atualize o app** para a versão mais recente na loja",
            "**Limpe o cache** do aplicativo: Configurações → Apps → Som na Nuvem → Limpar cache",
            "Se o problema persistir, **desinstale e reinstale** o aplicativo",
        ],
        "dica": "Dica: A maioria dos problemas técnicos é resolvida limpando o cache.",
        "link_ajuda": "https://ajuda.som-na-nuvem.com/app",
        "tempo_estimado": "5 minutos",
        "sistemas_suportados": ["Android 8+", "iOS 14+", "Windows 10+", "macOS 11+"],
    },

    # ────────────────────────────────────────
    # CANCELAMENTO (sempre escala)
    # ────────────────────────────────────────
    "cancelamento": {
        "titulo": "Cancelamento de assinatura",
        "escalamento": True,
        "motivo_escalamento": (
            "O cancelamento requer verificação de identidade e "
            "pode envolver análise de reembolso proporcional."
        ),
        "mensagem_pre_escalamento": (
            "Lamento saber que deseja cancelar.\n"
            "Antes de prosseguir, sabia que você pode **pausar sua assinatura** "
            "por até 3 meses ou migrar para um plano mais acessível?\n\n"
            "Vou te conectar com nossa equipe para encontrar a melhor solução."
        ),
        "link_ajuda": "https://ajuda.som-na-nuvem.com/cancelamento",
    },

    # ────────────────────────────────────────
    # CONTEÚDO AUSENTE
    # ────────────────────────────────────────
    "conteudo_ausente": {
        "titulo": "Conteúdo não encontrado",
        "escalamento": False,
        "passos": [
            "Verifique se está logado na **conta correta**",
            "**Atualize a biblioteca**: puxe a tela para baixo (pull to refresh)",
            "Aguarde até **24 horas** — mudanças de licença de conteúdo são comuns",
            "Para músicas baixadas: **reconecte à internet** para sincronizar",
            "Limpe o cache do app: Configurações → Apps → Som na Nuvem → Limpar cache",
        ],
        "dica": (
            "💡 Dica: Algumas músicas podem ser removidas do catálogo por questões "
            "de licenciamento, independente da nossa vontade."
        ),
        "link_ajuda": "https://ajuda.som-na-nuvem.com/conteudo",
        "tempo_estimado": "3 minutos",
    },

    # ────────────────────────────────────────
    # PROBLEMA DE PAGAMENTO (sempre escala)
    # ────────────────────────────────────────
    "problema_pagamento": {
        "titulo": "Problema de pagamento",
        "escalamento": True,
        "motivo_escalamento": (
            "Problemas financeiros exigem verificação segura de dados bancários "
            "e devem ser tratados por um atendente humano."
        ),
        "mensagem_pre_escalamento": (
            "Entendi que você tem um problema relacionado ao pagamento.\n"
            "Por segurança, esse tipo de questão precisa ser tratado "
            "por um de nossos atendentes especializados."
        ),
        "link_ajuda": "https://ajuda.som-na-nuvem.com/pagamento",
    },

    # ────────────────────────────────────────
    # CATEGORIA GENÉRICA (fallback)
    # ────────────────────────────────────────
    "outro": {
        "titulo": "Problema não identificado",
        "escalamento": True,
        "motivo_escalamento": "Problema não categorizado automaticamente.",
        "mensagem_pre_escalamento": (
            "Não consegui identificar exatamente seu problema. "
            "Vou te conectar com um atendente para um atendimento personalizado."
        ),
    },
}


# ──────────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# ──────────────────────────────────────────────────────────────────

def get_solucao(tipo_problema: str) -> dict:
    """
    Retorna a solução para um tipo de problema.
    Usa 'outro' como fallback se o tipo não for encontrado.
    """
    return KNOWLEDGE_BASE.get(tipo_problema, KNOWLEDGE_BASE["outro"])


def requer_escalamento(tipo_problema: str) -> bool:
    """
    Verifica se o problema deve ser escalado automaticamente
    para um atendente humano.
    """
    solucao = get_solucao(tipo_problema)
    return solucao.get("escalamento", True)


def formatar_passos(passos: list) -> str:
    """
    Formata uma lista de passos como texto numerado.
    """
    return "\n".join(f"{i + 1}. {passo}" for i, passo in enumerate(passos))


def formatar_planos(planos: list) -> str:
    """
    Formata a lista de planos para exibição no chat.
    """
    linhas = []
    for plano in planos:
        linhas.append(f"**{plano['nome']}** — {plano['preco']}")
        linhas.append(f"   • {plano['dispositivos']} dispositivo(s) | {plano['perfis']} perfil(is)")
        linhas.append(f"   • Downloads offline: {'✅' if plano['downloads'] else '❌'}")
        if "obs" in plano:
            linhas.append(f"   • ⚠️ {plano['obs']}")
        linhas.append("")
    return "\n".join(linhas)
