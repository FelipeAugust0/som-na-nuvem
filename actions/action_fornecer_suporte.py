"""
action_fornecer_suporte.py
──────────────────────────
Action personalizada principal do chatbot Som na Nuvem.

Esta action implementa a lógica de:
  1. Ler o slot "problema" preenchido pela entidade extraída
  2. Consultar a base de dados (knowledge_base.py)
  3. Decidir entre fornecer solução automática ou escalar para humano
  4. Construir e enviar a resposta ao usuário
"""

import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions.knowledge_base import (
    get_solucao,
    requer_escalamento,
    formatar_passos,
    formatar_planos,
)

logger = logging.getLogger(__name__)

class ActionForneceeSuporte(Action):
    """
    Action que fornece suporte ao assinante com base no tipo de problema.

    Fluxo:
      1. Lê o slot 'problema' (preenchido automaticamente pela entidade)
      2. Consulta a base de dados de soluções
      3. Se o problema requer escalamento → chama action_escalar_atendente
      4. Caso contrário → formata e envia a solução passo a passo
    """

    def name(self) -> Text:
        return "action_fornecer_suporte"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        tipo_problema = tracker.get_slot("problema")

        if not tipo_problema:
            # Slot não preenchido: pedir mais informações
            logger.warning("Slot 'problema' não preenchido. Solicitando descrição.")
            dispatcher.utter_message(
                text=(
                    "Entendi que você tem um problema, mas preciso de mais detalhes. "
                    "Pode me contar o que está acontecendo?\n\n"
                    "Por exemplo: *'não consigo fazer login'*, "
                    "*'o app está travando'*, *'quero mudar meu plano'*..."
                )
            )
            return []

        logger.info(f"Slot 'problema' identificado: {tipo_problema}")

        solucao = get_solucao(tipo_problema)

        if requer_escalamento(tipo_problema):
            msg_pre = solucao.get("mensagem_pre_escalamento")
            if msg_pre:
                dispatcher.utter_message(text=msg_pre)
            return [SlotSet("problema", tipo_problema)]

        titulo = solucao.get("titulo", "Suporte")
        mensagem_partes = [f"**{titulo}**\n"]

        if tipo_problema == "mudanca_plano":
            mensagem_partes.append(
                "Aqui estão os planos disponíveis no Som na Nuvem:\n"
            )
            planos = solucao.get("info_planos", [])
            mensagem_partes.append(formatar_planos(planos))
            mensagem_partes.append("\n**Como alterar seu plano:**")
            passos_mudanca = solucao.get("como_mudar", [])
            mensagem_partes.append(formatar_passos(passos_mudanca))

        elif "passos" in solucao:
            passos = solucao["passos"]
            mensagem_partes.append(
                f"Siga os passos abaixo para resolver em ~{solucao.get('tempo_estimado', 'alguns minutos')}:\n"
            )
            mensagem_partes.append(formatar_passos(passos))

        if "dica" in solucao:
            mensagem_partes.append(f"\n{solucao['dica']}")

        if "link_ajuda" in solucao:
            mensagem_partes.append(
                f"\nArtigo completo: {solucao['link_ajuda']}"
            )

        resposta_final = "\n".join(mensagem_partes)
        dispatcher.utter_message(text=resposta_final)

        return [SlotSet("problema", tipo_problema)]

class ActionEscalarAtendente(Action):
    """
    Action que encaminha o assinante para um atendente humano.

    Em produção, esta action pode:
      - Criar um ticket no sistema de CRM (ex: Zendesk, Freshdesk)
      - Adicionar o usuário a uma fila de atendimento
      - Enviar notificação para o time de suporte
      - Registrar o log da conversa para o atendente
    """

    def name(self) -> Text:
        return "action_escalar_atendente"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        tipo_problema = tracker.get_slot("problema")
        sender_id = tracker.sender_id

        logger.info(
            f"Escalando para atendente humano | "
            f"Usuário: {sender_id} | Problema: {tipo_problema}"
        )

        numero_ticket = self._criar_ticket_suporte(sender_id, tipo_problema, tracker)

        mensagem = (
            "👤 **Conectando com um atendente humano...**\n\n"
            f"Número do seu atendimento: **#{numero_ticket}**\n"
            "Tempo estimado de espera: **~3 minutos**\n\n"
            "Enquanto aguarda, tenha em mãos:\n"
            "• E-mail cadastrado na conta\n"
            "• Descrição detalhada do problema\n"
            "• Modelo do dispositivo que está usando\n\n"
            "_Você também pode entrar em contato pelo e-mail: "
            "suporte@som-na-nuvem.com_"
        )

        dispatcher.utter_message(text=mensagem)

        return [SlotSet("problema", None)]

    def _criar_ticket_suporte(
        self,
        sender_id: str,
        tipo_problema: str,
        tracker: Tracker,
    ) -> str:
        """
        Simula a criação de um ticket no sistema de CRM.
        Em produção, faria uma chamada à API do sistema de suporte.
        """
        import hashlib
        import time

        raw = f"{sender_id}-{tipo_problema}-{time.time()}"
        ticket_hash = hashlib.md5(raw.encode()).hexdigest()[:6].upper()

        logger.info(f"Ticket criado: {ticket_hash} para usuário {sender_id}")

        return ticket_hash

class ActionReiniciarConversa(Action):
    """
    Reinicia os slots da conversa para permitir um novo atendimento.
    """

    def name(self) -> Text:
        return "action_reiniciar_conversa"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Tudo certo! Podemos começar um novo atendimento. Como posso ajudar?"
        )

        return [
            SlotSet("problema", None),
            SlotSet("problema_resolvido", None),
        ]
