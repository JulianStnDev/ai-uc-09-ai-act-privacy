"""Baut die Anfragen an Anthropic für den aufgezeichneten T01-Lauf (Anna Berger) nach und markiert jedes
personenbezogene Feld. Ohne API, ohne Datenbank, nur lesend.

Quelle: ai-uc-07-deployment, app/replay/aufzeichnung.json = Lauf 20260928-190527-a9c291 auf Cloud Run,
einmalig aus Neon exportiert (scripts/replay_export.py dort). Die Texte entstehen mit genau den Funktionen,
die die App in Produktion aufruft:
- Agent, erste Nachricht: uc4_agent.agent.ticket_prompt (lauf.py:131)
- Agent, Werkzeug-Ergebnisse: json.dumps(ergebnis) (uc4_agent/mcp_server.py:84), Ergebnisse aus dem Protokoll
- Judge auf der endgültigen Antwort: pruefung.judge_inhalt + mit_entscheidung (main.py:158-159)
- Haiku, endgültige Antwort: antwort.antwort_inhalt (antwort.py:63-67)

Aufruf (Python aus ai-uc-07-deployment/.venv wegen claude_agent_sdk):
    ../ai-uc-07-deployment/.venv/bin/python scripts/t01_anfragen.py
"""

import json
import re
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parents[1]
UC7 = HIER.parent / "ai-uc-07-deployment"
sys.path.insert(0, str(UC7))

from app import antwort, pruefung  # noqa: E402
from uc4_agent import agent  # noqa: E402

ZIEL = HIER / "evals" / "t01_anfragen.md"
HILFE_KUERZEN = True  # Hilfeartikel sind lang und ohne Personenbezug

A = json.loads((UC7 / "app" / "replay" / "aufzeichnung.json").read_text(encoding="utf-8"))
LAUF, EMPFEHLUNGEN, ANTWORT = A["lauf"], A["empfehlungen"], A["antwort"]
KUNDE = next(k for k in json.loads((UC7 / "uc4_agent" / "data" / "kunden.json").read_text(encoding="utf-8"))["kunden"]
             if k["kunden_id"] == LAUF["kunden_id"])
ZAHLUNGEN = [z for z in json.loads((UC7 / "uc4_agent" / "data" / "zahlungen.json").read_text(encoding="utf-8"))["zahlungen"]
             if z["kunden_id"] == LAUF["kunden_id"]]


def _betrag_varianten(b: float) -> list[str]:
    return [f"{b:.2f}".replace(".", ","), f"{b:.2f}", str(b)]


def _datum_varianten(iso: str) -> list[str]:
    j, m, t = iso.split("-")
    return [iso, f"{t}.{m}.{j}", f"{t}.{m}."]


# Markierung: ⟦Kategorie: Wert⟧. Reihenfolge der Kategorien egal, längere Werte gewinnen (E-Mail vor Name).
MARKEN = {}
MARKEN[KUNDE["email"]] = "E-Mail"
MARKEN[KUNDE["name"]] = "Name"
MARKEN[KUNDE["name"] + "s"] = "Name"
MARKEN[KUNDE["name"].split()[0]] = "Vorname"
MARKEN[KUNDE["kunden_id"]] = "Kunden-ID"
for z in ZAHLUNGEN:
    MARKEN[z["zahlungs_id"]] = "Zahlungs-ID"
    for v in _betrag_varianten(z["betrag_usd"]):
        MARKEN.setdefault(v, "Betrag")
    for v in _datum_varianten(z["datum"]):
        MARKEN.setdefault(v, "Datum")
for feld in ("kunde_seit",):
    for v in _datum_varianten(KUNDE[feld]):
        MARKEN.setdefault(v, "Datum")
for feld in ("periode_start", "periode_ende"):
    for v in _datum_varianten(KUNDE["abo"][feld]):
        MARKEN.setdefault(v, "Datum")
for wert, art in ((KUNDE["login"], "Login-Methode"), (KUNDE["abo"]["stufe"], "Abo-Stufe")):
    MARKEN[wert] = art
# Nur ganze Tokens markieren (nicht "K001" in "E-20260928-...")
MUSTER = re.compile("|".join(rf"(?<![\w.]){re.escape(w)}(?![\w])" for w in sorted(MARKEN, key=len, reverse=True)))


def markieren(text: str) -> tuple[str, dict[str, int]]:
    zaehler: dict[str, int] = {}

    def ersetzen(m):
        art = MARKEN[m.group(0)]
        zaehler[art] = zaehler.get(art, 0) + 1
        return f"⟦{art}: {m.group(0)}⟧"
    return MUSTER.sub(ersetzen, text), zaehler


def hilfe_kuerzen(ereignisse: list[dict]) -> list[dict]:
    """Volltexte der Hilfeartikel durch einen Platzhalter ersetzen (nur für die Anzeige)."""
    if not HILFE_KUERZEN:
        return ereignisse
    neu = []
    for e in ereignisse:
        if e.get("werkzeug") == "hilfe_durchsuchen" and "treffer" in e.get("ergebnis", {}):
            e = {**e, "ergebnis": {"treffer": [{**t, "text": f"[Artikeltext, {len(t['text'])} Zeichen im JSON, kein Personenbezug, hier gekürzt]"}
                                               for t in e["ergebnis"]["treffer"]]}}
        neu.append(e)
    return neu


def agent_anfrage() -> str:
    """Was der Agent-Lauf an Anthropic schickt, in Gesprächsform: erste Nachricht + jeder Werkzeugaufruf mit Ergebnis.
    Jeder Turn schickt den gesamten bisherigen Verlauf erneut (Messages API ist zustandslos)."""
    teile = ["[system] SYSTEM_PROMPT_V3 aus uc4_agent/agent.py:84-102 (ohne personenbezogene Daten)",
             "[system-reminder, von der CLI ergänzt] Arbeitsverzeichnis, Plattform, Modell, Datum, Budget (siehe DATENFLUSS.md, Abschnitt CLI)",
             "[user] " + agent.ticket_prompt({"absender": LAUF["absender"], "text": LAUF["text"]})]
    for e in hilfe_kuerzen(LAUF["ereignisse"]):
        if e["art"] == "text":
            teile.append("[assistant, Text] " + e["text"])
        else:
            teile.append(f"[assistant, tool_use] mcp__focusflow__{e['werkzeug']}({json.dumps(e['eingabe'], ensure_ascii=False)})")
            teile.append(f"[user, tool_result] {json.dumps(e['ergebnis'], ensure_ascii=False)}")
    return "\n\n".join(teile)


def judge_anfrage() -> str:
    ablauf = pruefung.mit_entscheidung(LAUF["ereignisse"], EMPFEHLUNGEN)
    inhalt = pruefung.judge_inhalt(LAUF["text"], ANTWORT["text"], ablauf, antwort.entscheidungen_als_text(EMPFEHLUNGEN))
    return inhalt


def haiku_anfrage() -> str:
    return antwort.antwort_inhalt(LAUF, EMPFEHLUNGEN)


def hilfe_im_text_kuerzen(text: str) -> str:
    """Im Judge- und Haiku-Inhalt stehen die Artikel als JSON-Text; für die Anzeige kürzen."""
    if not HILFE_KUERZEN:
        return text
    return re.sub(r'"text": "# [^"]*(?:\\.[^"\\]*)*"', lambda m: f'"text": "[Artikeltext, {len(m.group(0))} Zeichen im JSON, kein Personenbezug, hier gekürzt]"', text)


def abschnitt(titel: str, quelle: str, text: str, laenge_voll: int) -> str:
    markiert, zaehler = markieren(text)
    summe = ", ".join(f"{k} {v}×" for k, v in sorted(zaehler.items(), key=lambda x: -x[1]))
    return (f"## {titel}\n\n{quelle}\n\nLänge des vollständigen Inhalts: {laenge_voll} Zeichen. "
            f"Markierte Fundstellen: {sum(zaehler.values())} ({summe}).\n\n```text\n{markiert}\n```\n")


def main() -> None:
    global HILFE_KUERZEN
    HILFE_KUERZEN = False
    laengen = {"agent": len(agent_anfrage()), "judge": len(judge_anfrage()), "haiku": len(haiku_anfrage())}
    HILFE_KUERZEN = True
    kopf = f"""# T01 (Anna Berger): Was bei Anthropic ankommt

Erzeugt von `scripts/t01_anfragen.py`, ohne API. Quelle: aufgezeichneter Lauf `{LAUF['run_id']}` (Cloud Run, {LAUF['erstellt'][:10]}),
`ai-uc-07-deployment/app/replay/aufzeichnung.json` (Commit `75c5ea3`). Die Inhalte entstehen mit denselben Funktionen wie in
Produktion. Hilfeartikel sind gekürzt (kein Personenbezug), alles andere steht wörtlich da.

Markierung: ⟦Kategorie: Wert⟧. Automatisch markiert werden die bekannten Werte von {KUNDE['kunden_id']} aus `kunden.json` und
`zahlungen.json` (Name, Vorname, E-Mail, Kunden-ID, Zahlungs-IDs, Beträge, Daten von Zahlungen, Kundenkonto und Abo, Login-Methode, Abo-Stufe).
**Nicht automatisch markierbar** ist der Freitext: Ticket, Agent-Texte, Entwurf und Antwort sind als Ganzes personenbezogen,
weil sie sich auf eine bestimmte Person beziehen (Art. 4 Nr. 1 DSGVO), auch an Stellen ohne Markierung.
Zusätzlich personenbezogen, aber nicht markiert: Plattform (`web`), Anbieter (`stripe`), Abo-Status, Run-ID (verknüpfbar).
"""
    teile = [kopf,
             abschnitt("1. Agent-Lauf (Haiku 4.5 über Agent SDK), letzter Turn",
                       "Quelle: `uc4_agent/agent.py:181-182` (erste Nachricht), `uc4_agent/mcp_server.py:84` (Ergebnisse), "
                       "Werkzeugaufrufe wörtlich aus `laeufe.ereignisse`. Rekonstruktion: Die CLI baut die Anfrage selbst, "
                       "die Thinking-Blöcke fehlen im Protokoll. Turn 1 enthält nur System-Prompt, Reminder und erste Nachricht, "
                       f"jeder weitere Turn den ganzen Verlauf bis dahin ({LAUF['ergebnis']['num_turns']} Turns).",
                       agent_anfrage(), laengen["agent"]),
             abschnitt("2. Judge (Sonnet 5) auf der endgültigen Antwort",
                       "Quelle: `app/pruefung.py:170-174` (`judge_inhalt`), `app/pruefung.py:151-167` (`mit_entscheidung`), "
                       "aufgerufen in `app/main.py:158-159`. System-Prompt `JUDGE_SYSTEM` (`app/pruefung.py:30-34`) ohne Personenbezug. "
                       f"Gemessen: {A['pruefungen'][1]['judge']['input_tokens']} Input-Tokens.",
                       hilfe_im_text_kuerzen(judge_anfrage()), laengen["judge"]),
             abschnitt("3. Haiku 4.5 schreibt die endgültige Antwort",
                       "Quelle: `app/antwort.py:63-67` (`antwort_inhalt`), aufgerufen in `app/main.py:178`. "
                       "System-Prompt `ANTWORT_SYSTEM` (`app/antwort.py:17-25`) ohne Personenbezug. Die interne Notiz der Konsole "
                       "ist nicht enthalten (`app/speicher.py:272-276`).",
                       hilfe_im_text_kuerzen(haiku_anfrage()), laengen["haiku"])]
    ZIEL.write_text("\n".join(teile), encoding="utf-8")
    print(f"{ZIEL.relative_to(HIER)}: Längen {laengen}")


if __name__ == "__main__":
    main()
