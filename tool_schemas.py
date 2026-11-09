def _tool(name, description, properties, required=()):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": list(required),
            },
        },
    }


_TITLE = {"type": "string", "description": "Titre du rendez-vous"}
_START = {
    "type": "string",
    "description": "Date et heure de début au format YYYY-MM-DD HH:MM",
}

CALENDAR_TOOLS = [
    _tool(
        "get_calendar_events",
        "Récupère les événements du calendrier de l'utilisateur "
        "pour les prochains jours.",
        {
            "days": {
                "type": "integer",
                "description": "Nombre de jours à partir d'aujourd'hui "
                "(défaut : 7)",
            }
        },
    ),
    _tool(
        "create_calendar_event",
        "Crée un rendez-vous dans le calendrier de l'utilisateur. "
        "À n'appeler qu'après confirmation explicite de l'utilisateur "
        "sur le titre, la date et l'heure.",
        {
            "title": _TITLE,
            "start": _START,
            "duration_minutes": {
                "type": "integer",
                "description": "Durée en minutes (défaut : 60)",
            },
            "location": {
                "type": "string",
                "description": "Lieu (optionnel)",
            },
        },
        required=["title", "start"],
    ),
    _tool(
        "delete_calendar_event",
        "Supprime un rendez-vous du calendrier de l'utilisateur. "
        "À n'appeler qu'après avoir retrouvé le rendez-vous dans le "
        "calendrier et obtenu la confirmation explicite de l'utilisateur. "
        "Le titre et l'heure doivent être exactement ceux du calendrier.",
        {"title": _TITLE, "start": _START},
        required=["title", "start"],
    ),
    _tool(
        "create_email_draft",
        "Enregistre un mail en brouillon dans la boîte de l'utilisateur. "
        "Le mail n'est jamais envoyé : l'utilisateur le relit et l'envoie "
        "lui-même. À n'appeler qu'après avoir montré le texte à "
        "l'utilisateur et obtenu son accord.",
        {
            "to": {
                "type": "string",
                "description": "Adresse du destinataire, ou plusieurs "
                "adresses séparées par des points-virgules",
            },
            "subject": {"type": "string", "description": "Objet du mail"},
            "body": {"type": "string", "description": "Texte du mail"},
        },
        required=["to", "subject", "body"],
    ),
    _tool(
        "generate_image",
        "Génère une image à partir d'une description. L'image est affichée "
        "directement à l'utilisateur. À n'appeler que si l'utilisateur "
        "demande explicitement une image.",
        {
            "prompt": {
                "type": "string",
                "description": "Description détaillée de l'image à générer",
            }
        },
        required=["prompt"],
    ),
]

CALENDAR_TOOLS.append({
    "type": "function",
    "function": {
        "name": "generate_quote",
        "description": (
            "Génère un devis PDF téléchargeable. À appeler uniquement quand le client "
            "et au moins une ligne (description, quantité, prix unitaire HT) sont connus. "
            "Sinon, demande les informations manquantes. N'invente jamais un prix."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "client": {"type": "string", "description": "Nom et adresse du client"},
                "issuer": {"type": "string", "description": "Nom et adresse de l'émetteur"},
                "lines": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "quantity": {"type": "number"},
                            "unit_price": {"type": "number", "description": "Prix unitaire HT en euros"},
                        },
                        "required": ["description", "quantity", "unit_price"],
                    },
                },
                "vat_rate": {"type": "number", "description": "Taux de TVA en %, 20 par défaut"},
                "validity_days": {"type": "integer", "description": "Durée de validité, 30 par défaut"},
                "notes": {"type": "string", "description": "Conditions ou remarques"},
            },
            "required": ["client", "lines"],
        },
    },
})