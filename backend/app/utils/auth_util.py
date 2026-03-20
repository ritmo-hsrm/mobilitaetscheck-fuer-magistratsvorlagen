from __future__ import annotations

from app.crud.exceptions import AuthorizationError

ADMIN_ROLLE_NAME = "Admin"


def check_user_authorization(user: User, gemeinde_id: int):
    """
    Check if a user is authorized to access a specific municipality.

    :param user: The user instance to check.
    :param municipality_id: The ID of the municipality to access.
    :raises AuthorizationError: If the user is not authorized to access the resource.
    """
    grant_access = gemeinde_id == user.gemeinde_id

    # Gemeinde Admins (is_superuser + Verwaltung role) bypass Gemeinde checks.
    # Platform Admins (is_superuser + Admin role) do NOT get access to Gemeinde resources.
    if user.is_superuser and user.rolle.name != ADMIN_ROLLE_NAME:
        grant_access = True

    if not grant_access:
        raise AuthorizationError()
