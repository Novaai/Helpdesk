from ..models import Tag #importation of data for 

#Execute on ticket creation. Allow for manual tagging as well though
#Lexicon

KEYWORDS = {
    "technical_hardware": [
        "broken", "damaged", "monitor", "keyboard", "printer", "scanner","copier","repair","cpu","desktop","laptop","tower"
    ],
        "network_connectivity": [
        "slow", "freeze", "lag", "loading", "reconnect","network", "connection"
    ],
        "telecommunications": [
        "phone", "telephone", "extension", "line"
    ],
        "technical_software": [
        "error", "crash", "bug", "issue", "freeze", "update",
        "install", "loading",  "glitch", "Word", "Excel",
    ],
    "account": [
        "login", "logout", "password", "username", "reset", "locked", "access",
        "mfa", "2fa", "email verification", "credentials","Authentication","Reset","mail","email","account","domain"
    ],
    "installation": [
        "SAP", "Office", "Word", "Excel", "VPN", "Windows", "new",
        "setup", "status", "fulfillment"
    ],
    "general_inquiry": [
        "question", "ask", "query", "info", "information", "support", "help",
        "how to", "guidance"
    ]
}

#Stemmer
KEYWORD_SYNONYMS = {
    "laggy": "lag",
    "lagging":"lag",
    "slow": "lag",
    "crashed": "crash",
    "crush": "crash",
    "crushing": "crash",
    "overcharge":"overcharged",
    "resetting": "reset",
    "cancelled": "cancel",
    "refunded": "refund",
    "log in": "login",
    "loggin": "login",
    "net": "network",
    "internet":"network",
    "wifi":"network",
    "wi-fi":"network",
    "lan":"network",
    "set up":"setup",
    "set-up":"setup",
    "rest":"reset",
    "guthib":"you spelled it wrong",
    "installation":"install",
    "repairing":"repair",
    "lines":"line"
}

def normalize_text(text: str) -> str:
    for variant, canonical in KEYWORD_SYNONYMS.items():
        text = text.replace(variant, canonical)
    return text


def assign_tags_to_ticket(ticket):
    """
    Given a Ticket instance, auto-assign appropriate tags.
    """
    text = normalize_text(f"{ticket.title} {ticket.ticketDesc}").lower()
    matched_tags = set()

    for tag_name, keywords in KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matched_tags.add(tag_name)

    for tag_name in matched_tags:
        tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
        ticket.tags.add(tag_obj)

    ticket.save()