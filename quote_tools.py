import io
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from calendar_tools import TOOL_FUNCTIONS, _to_json

_last_quote = None


def pop_last_quote():
    global _last_quote
    quote, _last_quote = _last_quote, None
    return quote


def _money(value):
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + " €"


def _p(text):
    return escape(str(text)).replace("\n", "<br/>")


def _build_pdf(number, issuer, client, lines, vat_rate, validity_days,
               total_ht, vat, total_ttc, notes):
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, title=f"Devis {number}",
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    )

    now = datetime.now()
    valid_until = now + timedelta(days=validity_days)
    story = [
        Paragraph(f"DEVIS {number}", styles["Title"]),
        Paragraph(f"Date : {now:%d/%m/%Y} - valable jusqu'au {valid_until:%d/%m/%Y}", normal),
        Spacer(1, 16),
    ]

    parties = Table(
        [[Paragraph(f"<b>Émetteur</b><br/>{_p(issuer or '-')}", normal),
          Paragraph(f"<b>Client</b><br/>{_p(client)}", normal)]],
        colWidths=[8.5 * cm, 8.5 * cm],
    )
    parties.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story += [parties, Spacer(1, 20)]

    rows = [["Description", "Qté", "PU HT", "Total HT"]]
    for line in lines:
        rows.append([
            Paragraph(_p(line["description"]), normal),
            f"{line['quantity']:g}",
            _money(line["unit_price"]),
            _money(line["total"]),
        ])
    table = Table(rows, colWidths=[8 * cm, 1.8 * cm, 3.6 * cm, 3.6 * cm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story += [table, Spacer(1, 14)]

    totals = Table(
        [["Total HT", _money(total_ht)],
         [f"TVA ({vat_rate:g} %)", _money(vat)],
         ["Total TTC", _money(total_ttc)]],
        colWidths=[4 * cm, 4 * cm], hAlign="RIGHT",
    )
    totals.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
        ("LINEABOVE", (0, 2), (-1, 2), 0.8, colors.black),
    ]))
    story.append(totals)

    if notes:
        story += [Spacer(1, 20), Paragraph(f"<b>Notes</b><br/>{_p(notes)}", normal)]

    doc.build(story)
    return buffer.getvalue()


def generate_quote(client, lines, issuer="", vat_rate=20.0, validity_days=30, notes=""):
    global _last_quote

    if not lines:
        raise ValueError("Le devis doit contenir au moins une ligne.")

    clean = []
    for line in lines:
        quantity = float(line.get("quantity", 1))
        unit_price = float(line["unit_price"])
        if quantity <= 0 or unit_price < 0:
            raise ValueError("Quantité ou prix invalide.")
        clean.append({
            "description": line["description"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total": round(quantity * unit_price, 2),
        })

    total_ht = round(sum(line["total"] for line in clean), 2)
    vat = round(total_ht * vat_rate / 100, 2)
    total_ttc = round(total_ht + vat, 2)
    number = f"DEV-{datetime.now():%Y%m%d-%H%M%S}"

    _last_quote = {
        "filename": f"{number}.pdf",
        "data": _build_pdf(number, issuer, client, clean, vat_rate, validity_days,
                           total_ht, vat, total_ttc, notes),
    }

    return _to_json({
        "statut": "devis généré et disponible au téléchargement",
        "numero": number,
        "total_ht": total_ht,
        "tva": vat,
        "total_ttc": total_ttc,
    })


TOOL_FUNCTIONS["generate_quote"] = generate_quote