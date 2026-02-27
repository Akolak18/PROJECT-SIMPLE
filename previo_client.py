"""
Previo PMS API client.
Docs: https://rest.apidocs.previo.app
Auth: Basic Auth (username:password base64-encoded)
"""

import os
import requests
from datetime import datetime, timedelta


BASE_URL = "https://api.previo.app/x1"


def _auth():
    return (os.environ["PREVIO_USERNAME"], os.environ["PREVIO_PASSWORD"])


def _hotel_id():
    return int(os.environ["PREVIO_HOTEL_ID"])


def get_reservations(date_from: str = None, date_to: str = None) -> list[dict]:
    """
    Fetch room reservations from Previo.

    date_from / date_to: 'YYYY-MM-DD', defaults to today ± 30 days.

    Returns a flat list of dicts ready for display / Excel export.
    """
    today = datetime.today()
    date_from = date_from or today.strftime("%Y-%m-%d")
    date_to = date_to or (today + timedelta(days=30)).strftime("%Y-%m-%d")

    params = {
        "hotelId": _hotel_id(),
        "dateFrom": date_from,
        "dateTo": date_to,
        "lang": "en",
    }

    resp = requests.get(
        f"{BASE_URL}/reservation",
        params=params,
        auth=_auth(),
        timeout=15,
    )
    resp.raise_for_status()

    data = resp.json()

    # Previo wraps results under various keys depending on version.
    # Handle both {"reservations": [...]} and a bare list.
    if isinstance(data, list):
        raw = data
    else:
        raw = (
            data.get("reservations")
            or data.get("roomReservations")
            or data.get("data")
            or []
        )

    return [_flatten(r) for r in raw]


def _flatten(r: dict) -> dict:
    """Normalise a Previo reservation record into the fields we care about."""
    # Support both the full reservation wrapper and a bare roomReservation.
    room_reservations = r.get("roomReservations") or []

    if room_reservations:
        # Multiple rooms in one booking — expand each room separately.
        rows = []
        for rr in room_reservations:
            rows.append(_room_row(r, rr))
        return rows  # caller will need to flatten the list of lists

    # Already a flat roomReservation record.
    return [_room_row({}, r)]


def _room_row(reservation: dict, rr: dict) -> dict:
    guest = reservation.get("guest") or rr.get("guest") or {}
    room = rr.get("room") or {}

    return {
        "reservation_id": reservation.get("id") or rr.get("reservationId") or "",
        "room_reservation_id": rr.get("id") or rr.get("roomReservationId") or "",
        "room": room.get("name") or rr.get("roomName") or "",
        "room_type": room.get("type") or rr.get("roomType") or "",
        "check_in": _fmt_date(rr.get("arrival") or rr.get("dateFrom")),
        "check_out": _fmt_date(rr.get("departure") or rr.get("dateTo")),
        "nights": rr.get("nights") or _calc_nights(rr),
        "adults": rr.get("adults") or rr.get("personsAdult") or 0,
        "children": rr.get("children") or rr.get("personsChild") or 0,
        "guest_name": _guest_name(guest),
        "guest_email": guest.get("email") or "",
        "guest_phone": guest.get("phone") or "",
        "status": _status_label(
            reservation.get("status") or reservation.get("commissionStatus") or
            rr.get("status") or rr.get("commissionStatus") or 0
        ),
        "note": rr.get("note") or reservation.get("note") or "",
        "meal_plan": rr.get("mealPlan") or rr.get("board") or "",
        "price": rr.get("price") or rr.get("totalPrice") or "",
        "currency": rr.get("currency") or reservation.get("currency") or "",
        "channel": reservation.get("channel") or rr.get("channel") or "",
        "created_at": _fmt_date(reservation.get("createdAt") or rr.get("createdAt")),
    }


def _guest_name(guest: dict) -> str:
    parts = [guest.get("firstName") or "", guest.get("lastName") or ""]
    name = " ".join(p for p in parts if p).strip()
    return name or guest.get("name") or guest.get("fullName") or ""


def _fmt_date(value) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        # Strip time component if present
        return value[:10]
    return str(value)


def _calc_nights(rr: dict) -> int:
    try:
        d1 = datetime.strptime((rr.get("arrival") or rr.get("dateFrom") or "")[:10], "%Y-%m-%d")
        d2 = datetime.strptime((rr.get("departure") or rr.get("dateTo") or "")[:10], "%Y-%m-%d")
        return (d2 - d1).days
    except Exception:
        return 0


STATUS_MAP = {
    1: "Option",
    2: "Confirmed",
    3: "Checked In",
    7: "Cancelled",
    8: "No-show",
    9: "Checked Out",
}


def _status_label(code) -> str:
    try:
        return STATUS_MAP.get(int(code), str(code))
    except (TypeError, ValueError):
        return str(code)


def flatten_reservations(reservations: list) -> list[dict]:
    """
    get_reservations() returns a list where each element may itself be a list
    (one entry per room in a multi-room booking). Flatten everything to a single
    list of row dicts.
    """
    rows = []
    for item in reservations:
        if isinstance(item, list):
            rows.extend(item)
        else:
            rows.append(item)
    return rows
