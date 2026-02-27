"""
Generate a cleaner-friendly Excel file from a list of reservation row dicts.
"""

import io
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    PatternFill,
    Side,
)
from openpyxl.utils import get_column_letter


# ── Colour palette ──────────────────────────────────────────────────────────
HEADER_BG = "1F4E79"   # dark blue
HEADER_FG = "FFFFFF"   # white
CHECKIN_BG = "D9EAD3"  # light green  – checking-IN today
CHECKOUT_BG = "FCE5CD"  # light orange – checking-OUT today
ALT_ROW_BG = "F0F4F8"  # very light blue for alternating rows

# ── Columns shown in the cleaner sheet ─────────────────────────────────────
COLUMNS = [
    ("Room",          "room"),
    ("Check-in",      "check_in"),
    ("Check-out",     "check_out"),
    ("Nights",        "nights"),
    ("Guest",         "guest_name"),
    ("Adults",        "adults"),
    ("Children",      "children"),
    ("Status",        "status"),
    ("Meal plan",     "meal_plan"),
    ("Note",          "note"),
    ("Channel",       "channel"),
]


def build_excel(rows: list[dict], date_from: str = "", date_to: str = "") -> bytes:
    """
    Build an Excel workbook from the reservation rows and return it as bytes.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Reservations"

    today = datetime.today().strftime("%Y-%m-%d")

    # ── Title row ────────────────────────────────────────────────────────────
    title = f"Cleaning schedule  |  {date_from} → {date_to}  |  generated {today}"
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(COLUMNS))
    title_cell = ws.cell(row=1, column=1, value=title)
    title_cell.font = Font(bold=True, size=13, color="1F4E79")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 24

    # ── Header row ───────────────────────────────────────────────────────────
    header_fill = PatternFill("solid", fgColor=HEADER_BG)
    header_font = Font(bold=True, color=HEADER_FG, size=11)
    thin = Side(style="thin", color="CCCCCC")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for col_idx, (label, _) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=2, column=col_idx, value=label)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border
    ws.row_dimensions[2].height = 20

    # ── Sort rows: by check-in date, then room name ──────────────────────────
    rows = sorted(rows, key=lambda r: (r.get("check_in") or "", r.get("room") or ""))

    # ── Data rows ────────────────────────────────────────────────────────────
    checkin_fill  = PatternFill("solid", fgColor=CHECKIN_BG)
    checkout_fill = PatternFill("solid", fgColor=CHECKOUT_BG)
    alt_fill      = PatternFill("solid", fgColor=ALT_ROW_BG)

    for row_idx, reservation in enumerate(rows, start=3):
        check_in  = reservation.get("check_in", "")
        check_out = reservation.get("check_out", "")

        if check_in == today:
            row_fill = checkin_fill
        elif check_out == today:
            row_fill = checkout_fill
        elif row_idx % 2 == 0:
            row_fill = alt_fill
        else:
            row_fill = None

        for col_idx, (_, field) in enumerate(COLUMNS, start=1):
            value = reservation.get(field, "")
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = Alignment(vertical="center", wrap_text=(field == "note"))
            cell.border = border
            if row_fill:
                cell.fill = row_fill

        ws.row_dimensions[row_idx].height = 18

    # ── Auto-size columns ────────────────────────────────────────────────────
    col_widths = {
        "Room":       14,
        "Check-in":   13,
        "Check-out":  13,
        "Nights":      7,
        "Guest":      24,
        "Adults":      7,
        "Children":    9,
        "Status":     14,
        "Meal plan":  14,
        "Note":       36,
        "Channel":    16,
    }
    for col_idx, (label, _) in enumerate(COLUMNS, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = col_widths.get(label, 14)

    # ── Legend sheet ─────────────────────────────────────────────────────────
    legend = wb.create_sheet("Legend")
    legend["A1"] = "Colour legend"
    legend["A1"].font = Font(bold=True, size=12)

    legend_data = [
        (CHECKIN_BG,  "Green  – guest checking IN today"),
        (CHECKOUT_BG, "Orange – guest checking OUT today (room needs cleaning)"),
        ("FFFFFF",    "White  – future reservation"),
        (ALT_ROW_BG,  "Light blue – alternating row for readability"),
    ]
    for i, (colour, description) in enumerate(legend_data, start=3):
        cell = legend.cell(row=i, column=1, value=description)
        cell.fill = PatternFill("solid", fgColor=colour)
        cell.border = border
        cell.alignment = Alignment(vertical="center")
        legend.row_dimensions[i].height = 18
    legend.column_dimensions["A"].width = 56

    # ── Return as bytes ───────────────────────────────────────────────────────
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
