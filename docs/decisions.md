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

## 2026-10-08: Einstufung und Pflichten als Vorlage für Legal, nicht als Entscheidung

Kontext: Schritt 2 und 3 ordnen den Agent nach AI Act und DSGVO ein. Mehrere Fragen haben keine eindeutige Antwort in Gesetz oder Leitlinien (Art. 22 bei begünstigenden Entscheidungen, Art. 50(1) bei asynchronem Ticketportal, Erforderlichkeit eines LLM für Art. 6(1)(b), Handelsbrief-Eigenschaft von Support-Korrespondenz).

Optionen: (a) jede Frage selbst entscheiden, (b) einschätzen und offene Auslegungen als „mit Legal klären“ markieren.

Entscheidung: (b). Keine Rechtsberatung. Die Vorlage plant im Zweifel die vorsichtigere Variante in den Backlog ein (z. B. KI-Hinweis auch im asynchronen Portal, Ablehnungen über die Konsole) und kennzeichnet das mit „ja*“.

Begründung: Eine Produktvorlage soll zeigen, was zu tun ist und wo eine Auslegung fehlt. Entscheiden muss jemand mit Mandat.

## 2026-10-08: Quellenregeln für Schritt 2 und 3

- **Nur Primärquellen:** EUR-Lex (Gesetzestexte, Beschlüsse, EuGH), Kommission und AI Office, EDPB / Art.-29-Gruppe, deutsche Aufsichtsbehörden (DSK), gesetze-im-internet.de.
- **Selbst am Original geprüft** werden die tragenden Aussagen: Omnibus (Datum, Inkrafttreten 27.7.2026, Art. 4, Art. 113, Art. 111(4)), HGB §257 Abs. 4, DSK-Muss-Liste Nr. 11. Die übrigen Zitate stammen aus Recherche-Abrufen derselben Quellen und sind so gekennzeichnet.
- **Entwürfe als Entwurf:** Die Leitlinien zu Art. 6 (Hochrisiko) gibt es nur als Entwurf vom 19.5.2026. Sie werden als Indiz zitiert, nicht als Beleg.
- **Korrektur:** Buchungsbelege sind nach geltendem HGB/AO 8 Jahre aufzubewahren, nicht 10.
