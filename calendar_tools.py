import json
import os
from datetime import datetime, timedelta

import win32com.client

OUTLOOK_CALENDAR_FOLDER = 9
OUTLOOK_DRAFTS_FOLDER = 16
OUTLOOK_APPOINTMENT_ITEM = 1
OUTLOOK_MAIL_ITEM = 0
LLM_DATE_FORMAT = "%Y-%m-%d %H:%M"
OUTLOOK_FILTER_FORMAT = "%d/%m/%Y %H:%M"
MAX_DAYS = 90
MAX_DURATION_MINUTES = 24 * 60
MAX_RECIPIENTS = 10
MAX_BODY_CHARS = 10000


def _to_json(data):
    return json.dumps(data, ensure_ascii=False)


def _error(message):
    return _to_json({"erreur": message})


def _format(date):
    return date.strftime(LLM_DATE_FORMAT)


def _midnight(date):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def _clamp(value, low, high):
    return max(low, min(int(value), high))


def _outlook():
    return win32com.client.Dispatch("Outlook.Application")


def _account_store():
    account = os.environ.get("CALENDAR_ACCOUNT", "").strip()
    if not account:
        raise ValueError("CALENDAR_ACCOUNT est absent du fichier .env")

    stores = _outlook().GetNamespace("MAPI").Stores
    names = [store.DisplayName for store in stores]
    for store in stores:
        if store.DisplayName.lower() == account.lower():
            return store
    raise ValueError(
        f"Compte introuvable dans Outlook : {account}. "
        f"Comptes disponibles : {names}"
    )


def _calendar_folder():
    return _account_store().GetDefaultFolder(OUTLOOK_CALENDAR_FOLDER)


def _events_between(start, end):
    items = _calendar_folder().Items
    items.Sort("[Start]")
    items.IncludeRecurrences = True
    date_filter = (
        f"[Start] >= '{start:{OUTLOOK_FILTER_FORMAT}}' "
        f"AND [Start] < '{end:{OUTLOOK_FILTER_FORMAT}}'"
    )
    return items.Restrict(date_filter)


def get_calendar_events(days=7):
    days = _clamp(days, 1, MAX_DAYS)
    start = _midnight(datetime.now())
    events = [
        {
            "titre": item.Subject,
            "debut": _format(item.Start),
            "fin": _format(item.End),
            "lieu": item.Location,
        }
        for item in _events_between(start, start + timedelta(days=days))
    ]
    return _to_json(events)


def create_calendar_event(title, start, duration_minutes=60, location=""):
    start_dt = datetime.strptime(start, LLM_DATE_FORMAT)
    duration_minutes = _clamp(duration_minutes, 1, MAX_DURATION_MINUTES)

    appointment = _calendar_folder().Items.Add(OUTLOOK_APPOINTMENT_ITEM)
    appointment.Subject = title
    appointment.Start = _format(start_dt)
    appointment.Duration = duration_minutes
    appointment.Location = location
    appointment.ReminderSet = True
    appointment.ReminderMinutesBeforeStart = 15
    appointment.Save()

    return _to_json({
        "statut": "créé",
        "titre": title,
        "debut": _format(start_dt),
        "duree_minutes": duration_minutes,
    })


def delete_calendar_event(title, start):
    start_dt = datetime.strptime(start, LLM_DATE_FORMAT)
    day_start = _midnight(start_dt)

    matches = [
        item
        for item in _events_between(day_start, day_start + timedelta(days=1))
        if item.Subject.strip().lower() == title.strip().lower()
        and _format(item.Start) == _format(start_dt)
    ]

    if not matches:
        return _error(
            "Aucun rendez-vous ne correspond à ce titre et à cette heure."
        )
    if len(matches) > 1:
        return _error("Plusieurs rendez-vous correspondent, "
                      "suppression annulée.")
    if matches[0].IsRecurring:
        return _error("Rendez-vous récurrent : à supprimer manuellement "
                      "dans Outlook.")

    matches[0].Delete()

    return _to_json({
        "statut": "supprimé",
        "titre": title,
        "debut": _format(start_dt),
    })


def create_email_draft(to, subject, body):
    recipients = [address.strip() for address in to.split(";")]
    recipients = [address for address in recipients if address]

    if not recipients or len(recipients) > MAX_RECIPIENTS:
        return _error(f"Entre 1 et {MAX_RECIPIENTS} destinataires attendus.")
    if any("@" not in address for address in recipients):
        return _error("Adresse de destinataire invalide.")

    drafts = _account_store().GetDefaultFolder(OUTLOOK_DRAFTS_FOLDER)
    mail = drafts.Items.Add(OUTLOOK_MAIL_ITEM)
    mail.To = "; ".join(recipients)
    mail.Subject = subject
    mail.Body = body[:MAX_BODY_CHARS]
    mail.Save()  # brouillon uniquement : jamais de mail.Send()

    return _to_json({
        "statut": "brouillon enregistré, non envoyé",
        "destinataires": recipients,
        "objet": subject,
    })


TOOL_FUNCTIONS = {
    "get_calendar_events": get_calendar_events,
    "create_calendar_event": create_calendar_event,
    "delete_calendar_event": delete_calendar_event,
    "create_email_draft": create_email_draft,
}


def run_tool(name, arguments):
    function = TOOL_FUNCTIONS.get(name)
    if function is None:
        return _error("outil inconnu")

    try:
        return function(**arguments)
    except Exception as error:  # l'erreur est renvoyée au LLM, pas à l'UI
        return _error(str(error))