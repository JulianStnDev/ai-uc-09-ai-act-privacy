# Ergebnisse

## Schritt 1: Datenfluss-Inventur (2026-10-08)

Kein Modell, keine API-Kosten. Der „Datensatz“ ist der aufgezeichnete Lauf T01 (`ai-uc-07-deployment/app/replay/aufzeichnung.json`, Lauf `20260928-190527-a9c291`).

| Anfrage an Anthropic | Zeichen | Markierte Fundstellen | davon direkte Identifikatoren (Name, Vorname, E-Mail) |
|---|---|---|---|
| Agent, letzter von 6 Turns | 10.228 | 64 | 8 |
| Judge (Sonnet 5) | 8.521 | 53 | 4 |
| Haiku, endgültige Antwort | 8.447 | 50 | 4 |

Erzeugt mit `scripts/t01_anfragen.py`, Inhalt in [t01_anfragen.md](t01_anfragen.md). Markiert werden die bekannten Werte des Kunden K001. Der Freitext ist zusätzlich als Ganzes personenbezogen.

Stationen mit personenbezogenen Daten: 11. Davon ohne Zusage eines EU-Standorts: 5 (Anthropic Agent, Judge und Neuschreiben mit Speicherung in den USA; Cloud Logging am Ort „global“; Replay im öffentlichen GitHub-Repo). Details: [docs/DATENFLUSS.md](../docs/DATENFLUSS.md).

## Schritt 2 und 3: Einstufung und Backlog (2026-10-08)

Keine API-Kosten. Ergebnis der Einstufung: begrenztes Risiko mit Transparenzpflichten (Art. 50(1), 50(2)) und KI-Kompetenz (Art. 4). Keine Verbote, kein Hochrisiko ([docs/AI_ACT.md](../docs/AI_ACT.md)).

| Backlog | Anzahl |
|---|---|
| Einträge gesamt | 28 |
| vor dem Go-live („ja“ oder „ja*“) | 19 (3 davon „ja*“) |
| heute erfüllt / teilweise / fehlt / nicht gebaut | 0 / 8 / 19 / 1 |
| Punkte „mit Legal klären“ | 4 (AI Act) + 7 (DSGVO) |

Gezählt aus [docs/BACKLOG.md](../docs/BACKLOG.md).

## Abschluss (2026-10-08)

- Pseudonymisierung (B13) als Ausblick mit Messplan: frische Kontrolle gegen Branch, je 45 Läufe, Judge j2, geschätzt 4,31–4,86 USD, Freigabegrenze ca. 5,20 USD. **Nicht gelaufen.**
- Gesamtkosten UC9: 0 USD.
