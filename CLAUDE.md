# Projekt-Kontext

## Problem
Entscheidungs- und Pflichtenvorlage, kein Produktcode: Was muss gelten, damit der UC7-Support-Agent ab morgen echte Kundentickets bearbeiten darf (DSGVO, später AI Act)? Erster Schritt: Datenfluss-Inventur ohne API (docs/DATENFLUSS.md, docs/DATENMINIMIERUNG.md). Schritt 2/3: AI-Act-Einstufung (docs/AI_ACT.md), DSGVO-Prüfung (docs/DSGVO.md), Pflichten-Backlog (docs/BACKLOG.md).

Datenquellen (Nachbar-Repos unter `~/dev`, nur lesen, nie ändern):
- `ai-uc-07-deployment`: Code der Web-App und des Agents (`app/`, `uc4_agent/`), Aufzeichnung T01 (`app/replay/aufzeichnung.json`), Protokoll in Neon (`DATABASE_URL` aus dessen `.env`, nur Read-only-Transaktionen)
- Cloud Run / Cloud Logging: Projekt `focusflow-demo-510014`, Dienst `uc7`, nur lesend (`gcloud logging read`, `... describe`); Log-Werte mit IP-Adressen oder Link-Codes nie ins Repo schreiben
- Lokale CLI-Protokolle unter `~/.claude/projects/` nur als Beleg zitieren, nicht kopieren

Regeln:
- Jede Aussage über den Code mit Datei und Zeile (Commit nennen).
- Anbieterangaben (Anthropic, Google Cloud, Neon) nur aus Primärquellen mit URL und Abrufdatum; was dort nicht steht, als offen markieren.
- Rechtsquellen nur primär: EUR-Lex, Kommission/AI Office, EDPB/WP29, DSK und Landesaufsichten, gesetze-im-internet.de. Unklare Auslegung als „mit Legal klären“ markieren, nicht entscheiden.
- Keine Rechtsberatung: Einordnungen als Einschätzung kennzeichnen.
- Bezahlte Schritte (API-Läufe) vorher schätzen und freigeben lassen.

## Erwartete Artefakte
- README.md nach Schema (Problem, PM-Entscheidung, Architektur, Eval, Kosten/Latenz, Learnings)
- README.md auf Englisch, README_DE.md auf Deutsch, inhaltlich identisch (gleiche Zahlen, Tabellen, Fachbegriffe). Oben jeweils Sprachlink (🇩🇪 Deutsche Version / 🇬🇧 English version). Änderungen immer in beiden Dateien nachziehen.
- meta.json gepflegt (status ausschließlich: planned | active | done)
- meta.json auf Englisch (speist die Portfolio-Seite): title, summary = ein Satz „what it shows“, metrics = 1–2 Kennzahlen wörtlich aus dem README; optional demo {url, note} und screenshot (Pfad im Repo)
- evals/ mit Datensatz + Ergebnissen
- docs/decisions.md mit datierten Entscheidungen

## Erlaubte Libraries
- Direkt gegen das SDK, kein LangChain/LlamaIndex
- Skripte laufen mit dem Python aus `ai-uc-07-deployment/.venv` (importieren dessen Code)

## Stil
- Python, einfache Skripte statt Frameworks
- Drei Zahlen im README Pflicht: Kosten/1000 Requests, p95-Latenz, Qualitätsmetrik
