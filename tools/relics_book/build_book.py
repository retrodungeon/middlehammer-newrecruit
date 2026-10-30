#!/usr/bin/env python3
"""Relics of the Age of Darkness — rules supplement PDF (docs/Relics_of_the_Age_of_Darkness.pdf), styled after the Forge World
Horus Heresy "Red Books" (typography, colours and page furniture only; no GW text or art).

Measured from the Legiones Astartes: Age of Darkness Army List PDF (411 x 539 pt pages):
headings Goudy Old Style Bold (red #841912, small caps), body Warnock Pro 5.7/7.25 pt,
crimson sidebar #981614 with parchment text #D9C899, cream parchment pages. Scaled x1.4477
to a 595 pt wide page. Free stand-ins: Sorts Mill Goudy (emboldened) and Crimson Text (SIL
OFL, licences in fonts/). parchment.jpg and cover.jpg are procedurally generated originals.

Rebuilt by tools/build_middlehammer.py on every build, from the Relics unit data, so the unit
tables always match the catalogues; the rules text is written here and must be edited by hand
when a ruling changes. build-check fails if the committed PDF differs from a fresh build.
"""
import json
from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Flowable,
                                NextPageTemplate, PageBreak, Table, TableStyle, KeepTogether,
                                CondPageBreak, FrameBreak)

HERE = Path(__file__).parent
S = 595.0 / 411.024                      # scale from the reference page
PW, PH = 595.0, 538.583 * S              # page size (Red Book proportions)

RED = HexColor("#841912")                # heading red (measured)
CRIMSON = HexColor("#981614")            # sidebar (measured)
PARCH = HexColor("#D9C899")              # sidebar text (measured)
GOLD = HexColor("#CC9E4D")               # cover frame (measured)
GOLD_TXT = HexColor("#C2995C")           # cover lettering (measured)
INK = HexColor("#000000")
RULE = HexColor("#9A5B48")               # boxed panel border
BAND = HexColor("#6B2A1A")

VERSION = "Version 1.0"
DATE = "30 October 2026"

# ------------------------------------------------------------------ fonts
for name, f in [("Goudy", "SortsMillGoudy-Regular.ttf"), ("Goudy-It", "SortsMillGoudy-Italic.ttf"),
                ("Body", "CrimsonText-Regular.ttf"), ("Body-Bold", "CrimsonText-Bold.ttf"),
                ("Body-It", "CrimsonText-Italic.ttf"), ("Body-BoldIt", "CrimsonText-BoldItalic.ttf")]:
    pdfmetrics.registerFont(TTFont(name, str(HERE / "fonts" / f)))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-It", boldItalic="Body-BoldIt")

BODY = 5.7 * S + 0.3      # Crimson Text sets slightly small next to Warnock
LEAD = 7.25 * S
st = {
    "body": ParagraphStyle("body", fontName="Body", fontSize=BODY, leading=LEAD, alignment=TA_LEFT, textColor=INK),
    "just": ParagraphStyle("just", fontName="Body", fontSize=BODY, leading=LEAD, alignment=TA_JUSTIFY, textColor=INK),
    "flav": ParagraphStyle("flav", fontName="Body-It", fontSize=BODY, leading=LEAD, alignment=TA_JUSTIFY, textColor=INK),
    "sub": ParagraphStyle("sub", fontName="Body-Bold", fontSize=BODY, leading=LEAD, spaceBefore=LEAD * 0.6, textColor=INK),
    "bullet": ParagraphStyle("bullet", fontName="Body", fontSize=BODY, leading=LEAD, leftIndent=9, bulletIndent=0.5,
                             textColor=INK),
    "side": ParagraphStyle("side", fontName="Body-It", fontSize=BODY, leading=LEAD, textColor=PARCH),
    "sideR": ParagraphStyle("sideR", fontName="Body", fontSize=BODY, leading=LEAD, textColor=PARCH, alignment=TA_RIGHT),
    "cell": ParagraphStyle("cell", fontName="Body", fontSize=BODY - 0.3, leading=LEAD - 0.6, textColor=INK),
    "cellB": ParagraphStyle("cellB", fontName="Body-Bold", fontSize=BODY - 0.3, leading=LEAD - 0.6, textColor=INK),
    "small": ParagraphStyle("small", fontName="Body", fontSize=BODY - 1.2, leading=LEAD - 1.6, textColor=INK),
}


def P(text, s="body"):
    return Paragraph(text, st[s])


def bullets(items, s="bullet"):
    return [Paragraph(t, st[s], bulletText="•") for t in items]


for k in ("bullet",):
    st[k].bulletFontName, st[k].bulletFontSize, st[k].bulletColor = "Body", BODY * 0.8, RED


# ------------------------------------------------------------------ headings (faux-bold Goudy small caps)
def smallcaps_runs(text, size, ratio=0.8):
    runs = []
    for word_i, word in enumerate(text.split(" ")):
        if word_i:
            runs.append((" ", size * ratio))
        for i, ch in enumerate(word):
            if ch.isalpha() and ch.islower():
                runs.append((ch.upper(), size * ratio))
            elif ch.isalpha() and i > 0 and word[:i].isupper() is False:
                runs.append((ch, size))
            else:
                runs.append((ch, size))
    return runs


def draw_goudy(c, x, y, text, size, color=RED, smallcaps=True, align="left", bold=True, ratio=0.8):
    runs = smallcaps_runs(text, size, ratio) if smallcaps else [(text, size)]
    width = sum(pdfmetrics.stringWidth(t, "Goudy", s) for t, s in runs)
    if align == "right":
        x -= width
    elif align == "center":
        x -= width / 2
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(size * 0.032 if bold else 0)
    for t, s in runs:
        to = c.beginText(x, y)
        to.setTextRenderMode(2 if bold else 0)
        to.setFont("Goudy", s)
        to.textOut(t)
        c.drawText(to)
        x += pdfmetrics.stringWidth(t, "Goudy", s)
    c.restoreState()
    return width


class Heading(Flowable):
    """Red Goudy small-caps line, optional right-aligned text (points), like a unit header."""

    def __init__(self, text, size=7.2 * S, right=None, space_before=LEAD * 0.9, space_after=1.5):
        super().__init__()
        self.text, self.size, self.right = text, size, right
        self.spaceBefore, self.spaceAfter = space_before, space_after

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.size * 1.05

    def draw(self):
        draw_goudy(self.canv, 0, self.size * 0.2, self.text, self.size)
        if self.right:
            draw_goudy(self.canv, self.aw, self.size * 0.2, self.right, self.size, align="right")


class Boxed(Flowable):
    """Section opener: big heading and intro text inside a thin rule box."""

    def __init__(self, title, paras, pad=7):
        super().__init__()
        self.title, self.paras, self.pad = title, paras, pad
        self.spaceAfter = LEAD

    def wrap(self, aw, ah):
        self.aw = aw
        self.th = 12 * S * 1.05
        self.hs = [p.wrap(aw - 2 * self.pad, ah)[1] for p in self.paras]
        self.h = self.pad + self.th + 2 + sum(self.hs) + 3 * (len(self.paras) - 1) + self.pad
        return aw, self.h

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.rect(0, 0, self.aw, self.h, stroke=1, fill=0)
        c.restoreState()
        y = self.h - self.pad - self.th
        draw_goudy(c, self.pad, y + 12 * S * 0.18, self.title, 12 * S)
        y -= 2
        for p, h in zip(self.paras, self.hs):
            y -= h
            p.drawOn(c, self.pad, y)
            y -= 3


class Sidebar(Flowable):
    """Zero-size marker: sets the crimson sidebar's label and quote from this page on."""

    def __init__(self, label, quote=None, source=None):
        super().__init__()
        self.label, self.quote, self.source = label, quote, source

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        doc = self.canv._doctemplate
        doc.side_marks.setdefault(doc.page, []).append((self.label, self.quote, self.source))


# ------------------------------------------------------------------ page furniture
M_L = 0.095 * PW
M_R_MAIN = 0.680 * PW
SB_X0, SB_X1 = 0.706 * PW, 0.881 * PW
TOP = PH - 0.105 * PH
BOT = 0.075 * PH


def page_number(c, doc):
    n = str(doc.page)
    w = pdfmetrics.stringWidth(n, "Goudy", 6 * S) + 8
    x, y = PW / 2 - w / 2, 0.028 * PH
    c.saveState()
    c.setStrokeColor(RED)
    c.setLineWidth(0.5)
    c.setFillColor(HexColor("#F1E6C8"))
    c.rect(x, y, w, 6 * S * 1.35, stroke=1, fill=1)
    c.restoreState()
    draw_goudy(c, PW / 2, y + 3.0, n, 6 * S, bold=False, smallcaps=False, align="center")


def band(c):
    """Top band: two thin rules with faint script between (an original motif)."""
    y0, y1 = PH - 0.030 * PH, PH - 0.052 * PH
    c.saveState()
    c.setStrokeColor(BAND)
    c.setLineWidth(0.5)
    c.line(0.035 * PW, y0, 0.965 * PW, y0)
    c.line(0.035 * PW, y1, 0.965 * PW, y1)
    c.setFillColor(Color(0.42, 0.16, 0.10, alpha=0.32))
    c.setFont("Goudy-It", 4.6)
    phrase = "relicta aetatis tenebrarum · in memoriam legionum · unitas per legem · "
    x = 0.04 * PW
    while x < 0.96 * PW:
        c.drawString(x, (y0 + y1) / 2 - 1.5, phrase)
        x += pdfmetrics.stringWidth(phrase, "Goudy-It", 4.6)
    c.restoreState()


def background(c, doc):
    c.drawImage(str(HERE / "parchment.jpg"), 0, 0, PW, PH)
    band(c)
    page_number(c, doc)


def sidebar(c, doc):
    label, quote, source = getattr(doc, "side", ("", None, None))
    top = PH - 0.098 * PH
    c.saveState()
    c.setFillColor(CRIMSON)
    c.rect(SB_X0, 0, SB_X1 - SB_X0, top, stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    for dx in (3, SB_X1 - SB_X0 - 3):
        c.line(SB_X0 + dx, 0, SB_X0 + dx, top - 6)
    # bar and roundel (original ornament)
    cx, cy = (SB_X0 + SB_X1) / 2, top
    c.setLineWidth(1.2)
    c.line(SB_X0 - 10, cy, SB_X1 + 10, cy)
    c.setFillColor(HexColor("#7A1410"))
    c.setLineWidth(1.1)
    c.circle(cx, cy, 15, stroke=1, fill=1)
    c.setLineWidth(0.5)
    c.circle(cx, cy, 11.5, stroke=1, fill=0)
    p = c.beginPath()
    p.moveTo(cx, cy + 8); p.lineTo(cx + 5, cy); p.lineTo(cx, cy - 8); p.lineTo(cx - 5, cy); p.close()
    c.setFillColor(GOLD)
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()
    if label:
        draw_goudy(c, cx, top - 34, label, 6.7 * S, color=PARCH, align="center")
    y = top - 46
    w = SB_X1 - SB_X0 - 16
    if quote:
        q = Paragraph(quote, st["side"])
        h = q.wrap(w, 400)[1]
        y -= h
        q.drawOn(c, SB_X0 + 8, y)
        if source:
            s = Paragraph(source, st["sideR"])
            h = s.wrap(w, 200)[1]
            y -= h + 6
            s.drawOn(c, SB_X0 + 8, y)


def on_side_page(c, doc):
    background(c, doc)


def on_side_end(c, doc):
    # The first section that starts on a page names its sidebar; otherwise the page carries
    # on the last section of the page before.
    marks = doc.side_marks.get(doc.page, [])
    doc.side = marks[0] if marks else doc.side_carry
    sidebar(c, doc)
    if marks:
        doc.side_carry = marks[-1]


def cover(c, doc):
    c.drawImage(str(HERE / "cover.jpg"), 0, 0, PW, PH)
    c.saveState()
    c.setStrokeColor(GOLD)
    m = 0.075 * PW
    c.setLineWidth(1.6)
    c.rect(m, m, PW - 2 * m, PH - 2 * m)
    c.setLineWidth(0.6)
    c.rect(m + 5, m + 5, PW - 2 * m - 10, PH - 2 * m - 10)
    c.restoreState()
    draw_goudy(c, PW / 2, PH * 0.80, "Middlehammer", 22 * S * 0.82, color=GOLD_TXT, align="center", ratio=0.78)
    # original emblem: a sword-like spine through a broken ring
    cx, cy = PW / 2, PH * 0.52
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setFillColor(GOLD)
    c.setLineWidth(2.2)
    c.arc(cx - 70, cy - 70, cx + 70, cy + 70, 20, 140)
    c.arc(cx - 70, cy - 70, cx + 70, cy + 70, 200, 140)
    c.setLineWidth(0.8)
    c.circle(cx, cy, 56, stroke=1, fill=0)
    p = c.beginPath()
    p.moveTo(cx, cy + 105); p.lineTo(cx + 7, cy + 70); p.lineTo(cx + 4, cy - 95); p.lineTo(cx, cy - 112)
    p.lineTo(cx - 4, cy - 95); p.lineTo(cx - 7, cy + 70); p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.setLineWidth(3)
    c.line(cx - 30, cy + 62, cx + 30, cy + 62)
    c.setFillColor(HexColor("#7A1410"))
    c.circle(cx, cy + 62, 6, stroke=1, fill=1)
    c.restoreState()
    draw_goudy(c, PW / 2, PH * 0.215, "Relics of the Age of Darkness", 12.5 * S, color=GOLD_TXT, align="center")
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(PW * 0.30, PH * 0.195, PW * 0.70, PH * 0.195)
    c.restoreState()
    draw_goudy(c, PW / 2, PH * 0.165, "A Book of the Unification Supplement", 8.5 * S, color=GOLD_TXT, align="center")
    draw_goudy(c, PW / 2, PH * 0.115, VERSION, 6 * S, color=GOLD_TXT, align="center", bold=False)


# ------------------------------------------------------------------ content
# Unit data: the "relicsHH1" section of build/middlehammer-build-report.json, set by build().
U = {}
HOSTS = ["Space Marines", "Dark Angels", "Blood Angels", "Space Wolves", "Chaos Space Marines"]
SLOTS = ["HQ", "Troops", "Elites", "Fast Attack", "Heavy Support", "Heavy Support (LoW)", "Lords of War",
         "No Force Org Slot"]
SLOT_LABEL = {"Lords of War": "Super-Heavy (Lord of War)", "Heavy Support (LoW)": "Heavy Support (Lord of War)",
              "No Force Org Slot": "Bodyguard (no slot)"}
MASTER_OF_ARMOUR = "Master of Armour"


def parse(units):
    out = []
    for u in units:
        slot, rest = u.split(": ", 1)
        legion = None
        if rest.endswith("]"):
            rest, legion = rest[:-1].rsplit(" [", 1)
        out.append((slot, rest, legion))
    return out


def tidy(n):
    import re
    m = re.match(r"^(.*?), (The|Legion)(?: Unit)?\s*$", n.strip())
    return f"{m.group(2)} {m.group(1).strip()}" if m else n.strip()


NOT_SH = set()


def fix_slot(slot, name):
    return ("Heavy Support (LoW)" if name in NOT_SH else slot) if slot == "Lords of War" else slot


def parse(units, _parse=parse):
    return [(fix_slot(sl, n), n, l) for sl, n, l in _parse(units)]


GENERIC = set()


def load(relics):
    """Take the Relics unit data from the build report; fail loudly if the data has hosts the
    book does not describe (a new Heresy list needs its own section here)."""
    global U, NOT_SH, GENERIC
    unknown = sorted(set(relics) - set(HOSTS))
    if unknown:
        raise SystemExit(f"Relics book: no section for {unknown}; update tools/relics_book/build_book.py")
    U = {h: {"units": v["units"], "lords": v.get("lordsOfWar") or {}, "sp": v.get("profileNotes") or []}
         for h, v in relics.items()}
    NOT_SH = {tidy(n) for h in U.values() for n in h["lords"].get("Heavy Support", [])}
    GENERIC = {(s, n) for s, n, l in parse(U["Space Marines"]["units"]) if l is None}


def slot_table(rows, legion_col=False):
    data = [[P("<b>Slot</b>", "cellB"), P("<b>Unit</b>", "cellB")] + ([P("<b>Legion</b>", "cellB")] if legion_col else [])]
    order = {s: i for i, s in enumerate(SLOTS)}
    for slot, name, legion in sorted(rows, key=lambda r: (order.get(r[0], 99), r[2] or "", r[1])):
        row = [P(SLOT_LABEL.get(slot, slot), "cell"), P(name, "cell")]
        if legion_col:
            row.append(P(legion or "", "cell"))
        data.append(row)
    widths = [0.27, 0.73] if not legion_col else [0.24, 0.52, 0.24]
    t = Table(data, colWidths=[w * (M_R_MAIN - M_L) for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, RED),
    ]))
    return t


def story():
    s = []
    s.append(NextPageTemplate("side"))
    s.append(PageBreak())

    # ---- Introduction
    s.append(Sidebar("Introduction",
                     "“The Legions that broke the galaxy did not vanish. Their arms were hung in "
                     "reliquaries, their engines entombed beneath forge-cathedrals, waiting.”",
                     "From a remembrancer’s fragment, unattributed"))
    s.append(Boxed("Relics of the Age of Darkness", [
        P("An optional supplement for <i>The Book of the Unification</i>. It lets 6th and 7th Edition "
          "Imperium and Chaos armies field units from the Horus Heresy 1st Edition army lists, the "
          "wargear of an older age brought out of the vaults ten thousand years later.", "just"),
        P("This document follows the same approach as the Unification itself: the 5th Edition core rules "
          "are the baseline, and anything from another game is changed only as far as it must be to fit.", "just"),
    ]))
    s.append(Heading("Why an Add-on?"))
    s.append(P("The Horus Heresy 1st Edition was written alongside 6th and 7th Edition Warhammer 40,000 and "
               "uses the same core rules, profiles and vehicle rules as the codexes of that era. Its units "
               "therefore fit the Unification with few changes, unlike the later Heresy editions, which are "
               "games of their own.", "just"))
    s.append(Heading("Optional by Design"))
    s.append(P("Nothing in this supplement is on by default. Both players should agree before Heresy units "
               "are used, in the same way the Unification treats super-heavy vehicles in smaller games.", "just"))
    s.append(Heading("Using This Supplement"))
    s += bullets([
        "Choose a 6th or 7th Edition Army List for an Imperium or Chaos faction that receives Heresy units "
        "(see <i>Successor Factions</i>).",
        "In New Recruit, tick <b>Configuration → Relics of the Age of Darkness → Use Horus Heresy 1st "
        "Edition units</b>. The option only appears for 6th and 7th Edition lists.",
        "Heresy units appear in the normal sections of the army, marked <b>(Heresy)</b> in the same way Forge "
        "World and Imperial Armour units are marked <b>(FW)</b> and <b>(IA)</b>.",
        "Build the army on the standard Force Organization Chart of the 5th Edition rulebook (p. 87), exactly "
        "as for any other list.",
    ])
    s.append(Heading("Design Philosophy"))
    s.append(P("Heresy units are brought across as printed in their army list, with three kinds of change only: "
               "what the Unification already changes for every 6th and 7th Edition codex; what belongs to "
               "Heresy army construction and has no meaning on the 5th Edition chart; and one ruling, "
               "<i>Relics of the Age of Darkness</i>, that replaces the Heresy Legion traits. Everything else "
               "– profiles, wargear, options and points – is unchanged.", "just"))

    # ---- Rulings
    s.append(PageBreak())
    s.append(Sidebar("Rulings",
                     "“What was forbidden then is merely obsolete now. Obsolete is not the same as "
                     "forgotten.”", "Attributed to a Magos of the Divisio Militaris"))
    s.append(Boxed("Army Construction", [
        P("Heresy units join an army; they never form one. The army is built from its own 6th or 7th Edition "
          "Army List on the 5th Edition chart, and the rules below decide which Heresy units it may add.", "just"),
    ]))
    s.append(Heading("The Force Organization Chart"))
    s.append(P("Heresy units use the standard 5th Edition Force Organization Chart only, taking the slot "
               "shown for them in their army list. The Heresy Crusade chart, its compulsory choices and its "
               "alternative charts (Zone Mortalis, Strategic Raid, Onslaught, Leviathan and Castellan) are "
               "not used. Units keep any slot change granted by their own options, such as a Primus "
               "Nullificator Consul allowing Nullificators to be taken as Troops.", "just"))
    s.append(Heading("No Rites of War"))
    s.append(P("Rites of War are detachment rules and are treated as Command Benefits (<i>Unification</i>, "
               "p. 9): they are not used. Units and options that exist only through a Rite of War cannot be "
               "taken; for example, a Master of Armour requires the Armoured Breakthrough Rite.", "just"))
    s.append(Heading("No Named Characters or Primarchs"))
    s.append(P("Heresy special characters and Primarchs are not available. A Legion’s generic leaders "
               "(Praetors, Centurions and their Consul upgrades) are.", "just"))
    s.append(Heading("Successor Factions"))
    s.append(P("Units of a single Legion are offered only to that Legion’s successor:", "just"))
    s += bullets([
        "<b>Dark Angels</b>, <b>Blood Angels</b> and <b>Space Wolves</b>: their own Legion.",
        "<b>Space Marines</b>: Ultramarines, Imperial Fists, White Scars, Iron Hands, Salamanders and "
        "Raven Guard.",
        "<b>Chaos Space Marines</b>: the nine Traitor Legions.",
        "Generic Legion units are offered to all five. Blackshields have no successor and are not used.",
    ])
    s.append(P("In Dark Angels, Blood Angels and Space Wolves armies every Heresy unit may take that "
               "Legion’s options. In Space Marines and Chaos Space Marines armies a Legion’s own units "
               "take that Legion’s options; generic units take none.", "just"))
    s.append(Heading("Bodyguards"))
    s.append(P("Command Squads and Legion retinues (Invictarus Suzerains, Huscarls, the Dark Sons of Death, "
               "Deathwing Companions and the like) do not use a Force Organization slot. Each such unit may be "
               "taken once for every model in the army with the Master of the Legion special rule: a Legion "
               "Praetor, a Praetor Tribune, or a Centurion upgraded to a Herald or Delegatus Consul.", "just"))
    s.append(Heading("Warlords"))
    s.append(P("No Warlord Traits are used (<i>Unification</i>, p. 10). A Heresy model may still be named "
               "the army’s Warlord for missions that score <i>Slay the Warlord</i>; the army has one "
               "Warlord in total.", "just"))

    # ---- The special rule
    s.append(CondPageBreak(160))
    s.append(Sidebar("Special Rules",
                     "“The gene-seed remembers its father. The armour remembers only its maker. "
                     "Both will serve.”", "From the margins of a Chapter armoury ledger"))
    s.append(Heading("Relics of the Age of Darkness", size=9.6 * S, space_before=LEAD * 1.4))
    s.append(P("Heresy armies choose a Legion and gain its traits. That choice does not exist in a 6th or "
               "7th Edition army, so every Heresy unit instead has the following special rule:", "just"))
    s.append(Boxed("Relics of the Age of Darkness", [
        P("This unit counts as having the army-wide special rules that the units of its Army List have (for "
          "example Chapter Tactics or <i>And They Shall Know No Fear</i>), and is affected by that list’s "
          "army-wide rules as if it were a unit from that list. It does not gain Legion traits from the Horus "
          "Heresy army lists.", "flav"),
    ]))
    s.append(P("Units keep all of their own special rules, including <i>Legiones Astartes</i>. Options that "
               "would give a unit a Legion’s traits (for example <i>Legion Inductees</i> for a "
               "Praevian’s battle-automata) are not used.", "just"))
    s.append(P("<i>This rule is a Middlehammer ruling, not printed text.</i>", "small"))

    # ---- Cross-edition amendments
    s.append(PageBreak())
    s.append(Sidebar("Amendments",
                     "“It was built to fight a war that ended before the Imperium had a name. It "
                     "fights this one well enough.”", "Tech-priest’s annotation, Ryza archive"))
    s.append(Boxed("Cross-Edition Compatibility", [
        P("Heresy army lists are 7th Edition publications. Everything the Unification says about 6th and 7th "
          "Edition codexes (pp. 9–10) applies to them in full. The points below are the ones that touch "
          "Heresy units most often.", "just"),
    ]))
    for title, text in [
        ("No Hull Points", "Heresy vehicles have no Hull Points. A rule that removes a Hull Point instead "
         "inflicts a Glancing Hit at AP – (<i>Unification</i>, p. 9)."),
        ("Super-Heavy Structure Points", "Super-heavy vehicles have Structure Points equal to one third of "
         "their Hull Points, rounded to the nearest whole number (<i>Unification</i>, p. 10). The values are "
         "given in the table below and in New Recruit."),
        ("Lords of War", "Lords of War that are super-heavies are taken as the army’s super-heavy without "
         "using a slot; any other Lord of War is a Heavy Support choice (<i>Unification</i>, p. 10). Super-heavies "
         "are not used at 1,500 points or less unless both players agree (p. 8)."),
        ("Melee Weapon AP", "AP 1–3 melee weapons are power weapons, AP 4 reduces armour saves by 1, and AP "
         "5, 6 and – are ignored (<i>Unification</i>, p. 10)."),
        ("D-Strength Weapons", "Destroyer weapons, such as the volcano cannon of the Falchion, use the "
         "Unification’s D-Strength rule (p. 10)."),
        ("Psykers", "Legion psykers choose their powers from the Unification’s discipline tables and may "
         "cast Mastery Level − 1 powers per turn, minimum 1 (p. 10). There is no Warp Charge (p. 9)."),
        ("Reactions to the Enemy", "There is no Overwatch, no Snap Shots and no Challenges (<i>Unification</i>, "
         "p. 9). Heresy rules that refer to them work as the Unification describes."),
    ]:
        s.append(Heading(title))
        s.append(P(text, "just"))

    sp_rows = []
    for host in ("Space Marines",):
        for line in U[host]["sp"]:
            if "Structure Points" in line and "Questoris" not in line:
                name, rest = line.split(": ")
                hp, spv = rest.replace(" HP -> ", "|").replace(" Structure Points", "").split("|")
                sp_rows.append((name.replace("Mastadon", "Legion Mastodon"), hp, spv))
    data = [[P("<b>Super-heavy</b>", "cellB"), P("<b>Hull Points</b>", "cellB"), P("<b>Structure Points</b>", "cellB")]]
    data += [[P(n, "cell"), P(h, "cell"), P(v, "cell")] for n, h, v in sorted(sp_rows)]
    t = Table(data, colWidths=[(M_R_MAIN - M_L) * w for w in (0.6, 0.2, 0.2)])
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0.6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6), ("LINEBELOW", (0, 0), (-1, 0), 0.5, RED)]))
    s.append(Heading("Structure Points", space_before=LEAD * 1.2))
    s.append(t)

    # ---- Patched out
    s.append(PageBreak())
    s.append(Sidebar("Patched Out",
                     "“Some doors in the archive are sealed for good reason. Others were sealed by "
                     "people who simply never wrote the reason down.”", "Inscription, Vault Seventeen"))
    s.append(Boxed("The “Patched Out” List", [
        P("Content in the Heresy army lists that is not used, and why. As in the Unification, the aim is to "
          "keep this list short.", "just"),
    ]))
    for title, text in [
        ("Heresy Army Construction", "The Crusade Force Organization Chart and its compulsory choices, "
         "alternative charts, Allied Detachments, Rites of War, Master of the Legion’s Rite of War choice "
         "and one-per-1,000-points limit, Legion and allegiance choices, and army themes such as the Shattered "
         "Legions and the Armies of Dark Compliance."),
        ("Legion Traits", "Replaced by the <i>Relics of the Age of Darkness</i> special rule."),
        ("Named Characters and Primarchs", "Not available."),
        ("Fortifications", "Not used, as for 7th Edition lists."),
        ("Unofficial Material", "Fan-made lists sometimes found alongside the Heresy data (Necron, Asuryani "
         "and the Mournival units) are not used, nor is the Varangian Heresy Legions list, whose source could "
         "not be confirmed."),
    ]:
        s.append(Heading(title))
        s.append(P(text, "just"))

    # ---- Units
    s.append(PageBreak())
    s.append(Sidebar("Legiones Astartes",
                     "“Twenty Legions marched out. What came back fills these pages.”",
                     "Unattributed"))
    s.append(Boxed("Legiones Astartes", [
        P("The Heresy units each faction may add. Points, profiles and wargear are given in New Recruit. "
          "“Legion” units are generic; units listed against a Legion belong to it alone.", "just"),
    ]))
    s.append(Heading("All Five Factions"))
    s.append(P("Available to Space Marines, Dark Angels, Blood Angels, Space Wolves and Chaos Space Marines "
               "armies, except where noted under each faction.", "just"))
    s.append(Spacer(1, 3))
    gen_rows = [(slot if slot != "Lords of War" else "Lords of War", n, None) for slot, n in sorted(GENERIC)]
    s.append(slot_table(gen_rows))
    for host in HOSTS:
        rows = parse(U[host]["units"])
        mine = {(sl, n) for sl, n, _ in rows}
        extra = [(sl, n, l or host_legion(host)) for sl, n, l in rows if (sl, n) not in GENERIC]
        missing = sorted(n for sl, n in GENERIC - mine)
        s.append(CondPageBreak(90))
        s.append(Heading(host, size=9.6 * S, space_before=LEAD * 1.5))
        if missing:
            s.append(P("<b>Not available:</b> " + ", ".join(sorted(set(missing))) + ".", "body"))
        if extra:
            s.append(Spacer(1, 2))
            s.append(slot_table(extra, legion_col=True))

    # ---- Known limits & credits
    s.append(PageBreak())
    s.append(Sidebar("Notes",
                     "“Record what you know. Mark what you do not. Never confuse the two.”",
                     "Archivist’s rule"))
    s.append(Boxed("Known Limits", [
        P("What this supplement does not do, or does not yet do.", "just"),
    ]))
    s += bullets([
        "Only the Legiones Astartes army list is included so far. Mechanicum, Questoris Knights, Solar "
        "Auxilia, Imperialis Militia, the Talons of the Emperor, the Daemons of the Ruinstorm and the Agents of "
        "the Emperor are planned.",
        "The number of super-heavies is not limited by New Recruit; players should take one per detachment "
        "(<i>Unification</i>, p. 10), as with any other list.",
        "Several Heresy vehicles also exist as Forge World units in 40k lists. Both versions are offered.",
        "Points, options and unit availability come from community data for the Heresy army lists and have "
        "not been checked against the printed books.",
        "A Heresy Warlord and the army list’s own Warlord option are separate in New Recruit; choose one.",
    ])
    s.append(Heading("Sources"))
    s += bullets([
        "<i>The Book of the Unification</i> v1.7.2 and the <i>Middlehammer Mission Pack</i> v1.4.1.",
        "Horus Heresy 1st Edition army list data: BSData/horus-heresy-1st-edition (archived), as converted for "
        "the Middlehammer New Recruit data.",
    ])
    s.append(Heading("Typefaces"))
    s.append(P("Set in Sorts Mill Goudy and Crimson Text, both under the SIL Open Font License.", "body"))
    s.append(Spacer(1, 10))
    s.append(P("Unofficial fan supplement for private play. Not affiliated with or endorsed by Games "
               "Workshop or Forge World. Warhammer 40,000 and The Horus Heresy are trademarks of Games "
               "Workshop Limited.", "small"))
    s.append(P(f"{VERSION} – {DATE}", "small"))
    return s


def host_legion(host):
    return {"Dark Angels": "Dark Angels", "Blood Angels": "Blood Angels", "Space Wolves": "Space Wolves"}.get(host)


def build(out, relics):
    """Write the book to out. relics: report["relicsHH1"] from the Middlehammer build.
    invariant=1 makes the PDF byte-identical for identical input (build-check compares it)."""
    load(relics)
    doc = BaseDocTemplate(str(out), pagesize=(PW, PH), title="Relics of the Age of Darkness",
                          author="Middlehammer", subject="A Book of the Unification supplement",
                          creator="tools/relics_book/build_book.py", invariant=1)
    doc.side = doc.side_carry = ("", None, None)
    doc.side_marks = {}
    main = Frame(M_L, BOT, M_R_MAIN - M_L, TOP - BOT, id="main", leftPadding=0, rightPadding=0,
                 topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[Frame(0, 0, PW, PH, id="c")], onPage=cover),
        PageTemplate(id="side", frames=[main], onPage=on_side_page, onPageEnd=on_side_end),
    ])
    doc.build(story())


def page_texts(path):
    from pypdf import PdfReader
    return [pg.extract_text() for pg in PdfReader(str(path)).pages]


def build_if_changed(out, relics):
    """Rebuild the book; replace out only if its text differs. PDF bytes can differ between
    machines (compression libraries), the content cannot. Returns True if out was written."""
    import tempfile, shutil
    out = Path(out)
    with tempfile.TemporaryDirectory() as tmp:
        new = Path(tmp) / out.name
        build(new, relics)
        if out.exists() and page_texts(out) == page_texts(new):
            return False
        shutil.copyfile(new, out)
        return True


ROOT = HERE.parents[1]
OUTPUT = ROOT / "docs" / "Relics_of_the_Age_of_Darkness.pdf"


if __name__ == "__main__":
    # Rebuild from the last build report (python tools/build_middlehammer.py writes it and
    # also rebuilds this book).
    report = json.loads((ROOT / "build" / "middlehammer-build-report.json").read_text())
    changed = build_if_changed(OUTPUT, report["relicsHH1"])
    print(f"{OUTPUT.relative_to(ROOT)}: {'updated' if changed else 'unchanged'}")
