# Entscheidungen

<!-- Format:
## YYYY-MM-DD: Kurztitel
Kontext, Optionen, Entscheidung, Begründung
-->

## 2026-09-18: Status-Vokabular für meta.json

Kontext: meta.json legt "status": "planned" fest, ohne definierte erlaubte Werte —
das driftet über mehrere Repos auseinander (planned/in-progress/wip/...).

Optionen: (a) einfach: planned → active → done, (b) zusätzlich mit
parked/abandoned für verworfene Use Cases, (c) feiner: research →
building → evaluating → shipped.

Entscheidung: (a) — planned, active, done. Zusätzlich in CLAUDE.md verankert.

Begründung: Bei einem Solo-Portfolio mit meist einem aktiven Repo lohnt sich
keine feinere Staffelung. CLAUDE.md-Verankerung, damit der Agent das Vokabular
bei jedem neuen Repo automatisch mitliest statt dass ich mich erinnern muss.

## 2026-10-08: UC9 als Pflichtenvorlage, erst Datenfluss, dann Einstufung

Kontext: Der UC7-Agent soll so geprüft werden, als gingen ab morgen echte Kundentickets hinein. Die Fragen aus DSGVO und AI Act hängen davon ab, welche Daten wohin fließen. Das war bisher nirgends zusammengetragen.

Optionen: (a) direkt mit der AI-Act-Einstufung beginnen, (b) erst den Datenfluss aus dem Code inventarisieren, mit Belegen und Anbieter-Primärquellen, dann einstufen.

Entscheidung: (b). Kein Produktcode, keine API-Aufrufe, UC7 bleibt unverändert. Die Anfragen an Anthropic für T01 baut ein Skript mit den Funktionen der App nach (`scripts/t01_anfragen.py`), statt einen neuen Lauf zu bezahlen.

Begründung: Die Einstufung braucht als Grundlage, welche personenbezogenen Daten wohin gehen, wie lange sie dort liegen und auf welcher Vertragsgrundlage. Ein Nachbau aus dem gespeicherten Lauf ist exakt für die Teile, die der App-Code baut (Judge, Neuschreiben, Werkzeug-Ergebnisse). Was die CLI des Agent SDK selbst ergänzt, ist nur über das lokale CLI-Protokoll belegt und als offen markiert.

## 2026-10-08: Regeln der Inventur

- **Stationen:** die elf aus dem Auftrag. Build (Cloud Build, Artifact Registry) und Secret Manager stehen unter Cloud Run mit drin, eigene Stationen bekommen sie nicht.
- **Personenbezug:** Name, E-Mail, Kunden-ID, Konto- und Zahlungsdaten werden einzeln markiert. Freitext, Entwürfe und Antworten zählen als Ganzes, weil sie sich auf eine Person beziehen. Pseudonyme (Kunden-ID, Link-Code) bleiben personenbezogen.
- **Primärquellen:** nur Seiten der Anbieter selbst. Bei Neon zählen die Databricks-Seiten mit, weil `neon.com/dpa` und `neon.com/subprocessors` dorthin weiterleiten. Widersprüche zwischen zwei Anbieterseiten werden genannt, nicht aufgelöst.
- **Logs:** Abfragen nur zählend. IP-Adressen und Link-Codes kommen nicht ins Repo.
