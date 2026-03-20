from fastapi_mail import MessageSchema, MessageType

from app.core.config import settings
from app.models.user import User
from app.services.mail.config_mail import Mail
from app.utils.url_util import add_query_params



async def send_verification(user: User, token: str):
    url = add_query_params(
        f"{settings.HOST_URL}/auth/account-bestaetigen", {"token": token}
    )

    user_dict = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "gemeinde": user.gemeinde.name,
        "url": url,
    }

    message = MessageSchema(
        subject="Willkommen – bitte bestätigen Sie Ihren Account",
        recipients=[user.email],
        template_body=user_dict,
        subtype=MessageType.html,
    )

    try:
        await Mail.send_message(message, template_name="account-bestaetigen.html")
    except Exception as e:
        print(f"Error sending verification email: {e}")


def _format_gueltigkeitsdauer(hours: int) -> str:
    if hours == 1:
        return "1 Stunde"
    if hours < 24:
        return f"{hours} Stunden"
    days = hours // 24
    if days == 1:
        return "1 Tag"
    return f"{days} Tage"


async def send_einladung(
    email: str, gemeinde_name: str, rolle_name: str, token: str, valid_hours: int
):
    url = add_query_params(
        f"{settings.HOST_URL}/auth/registrieren/einladung", {"token": token}
    )

    invite_dict = {
        "rolle": rolle_name,
        "gemeinde": gemeinde_name,
        "url": url,
        "gueltigkeitsdauer": _format_gueltigkeitsdauer(valid_hours),
    }

    message = MessageSchema(
        subject="Einladung zur Registrierung beim Mobilitätscheck für Magistratsvorlagen",
        recipients=[email],
        template_body=invite_dict,
        subtype=MessageType.html,
    )
    try:
        await Mail.send_message(message, template_name="einladung.html")
    except:
        print("Error sending invite email")


async def send_reset_password(user: User, token: str):

    url = add_query_params(
        f"{settings.HOST_URL}/auth/passwort-zuruecksetzen", {"token": token}
    )

    user_dict = {
        "vorname": user.vorname,
        "nachname": user.nachname,
        "rolle": user.rolle.name,
        "url": url,
    }

    message = MessageSchema(
        subject="Passwort zurücksetzen",
        recipients=[user.email],  # List of recipients
        template_body=user_dict,
        subtype=MessageType.html,
    )

    await Mail.send_message(message, template_name="passwort-zuruecksetzen.html")
