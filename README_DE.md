🇬🇧 [English version](README.md)

# UC9: AI Act & Datenschutz für den Support-Agent

> Entscheidungs- und Pflichtenvorlage, kein Produktcode. Die Frage: Was müsste gelten, wenn ab morgen echte Kundentickets in den UC7-Support-Agent gingen? Schritt 1 ist eine Datenfluss-Inventur aus dem Code, Schritt 2 die AI-Act-Einstufung, Schritt 3 die DSGVO-Prüfung mit Pflichten-Backlog. Keine Rechtsberatung. Jede Aussage ist mit Datei und Zeile oder mit einer Primärquelle des Anbieters belegt. Kosten: 0 USD, keine API-Aufrufe.

## Problem
Der UC7-Agent läuft auf Cloud Run und bearbeitet Support-Tickets. In der Demo sind die Kunden fiktiv. Mit echten Kunden liefen Namen, E-Mail-Adressen, Zahlungen und Freitext durch elf Stationen, drei davon bei Anthropic. Bevor man das System nach dem AI Act einstufen oder DSGVO-Pflichten aufsetzen kann, muss eines klar sein: welche personenbezogenen Daten wo landen, wie lange sie dort liegen und auf welcher Vertragsgrundlage.

## Schritt 1: Datenfluss-Inventur

**5 von 11 Stationen ohne Zusage eines EU-Standorts.**
App und Datenbank laufen in Frankfurt (Cloud Run `europe-west3`, Neon `aws-eu-central-1`). Anthropic speichert API-Daten in den USA und bietet keine EU-Option an. Haiku 4.5, das den Agent und das Neuschreiben ausführt, lässt sich auf gar keine Region festlegen. Cloud Logging speichert Request-Logs mit IP-Adresse, Browser-Kennung und vollständiger URL in einem Bucket am Ort „global“. Der aufgezeichnete Fall T01 ist ein vollständiger Kundendatensatz und liegt im öffentlichen GitHub-Repo.

| Station | Personenbezogene Daten | Ort | Aufbewahrung |
|---|---|---|---|
| Browser | Kunden-ID, Freitext; die Seiten zeigen alles | Gerät des Nutzers | Cookies 7 / 60 Tage |
| Cloud Run | alles, im Arbeitsspeicher und in Laufdateien | Frankfurt | bis Ende der Instanz |
| Neon | alles außer IP | Frankfurt | **keine Löschung im Code** |
| Anthropic Agent, Judge, Neuschreiben | E-Mail, Name, Konto, Zahlungen, Freitext, Entwurf | gespeichert in den USA | bis 30 Tage, bei Markierung bis 2 Jahre |
| Cloud Logging | IP, Browser-Kennung, URL mit Run-ID und Link-Code | „global“ | 30 Tage |
| Konsole, Betriebsseite | Name, E-Mail, Ticket, Entwurf, interne Notiz | aus Neon | wie Neon |
| Replay | der ganze Fall T01 | öffentliches Git-Repo, jeder Besucher | unbegrenzt |
| Persönliche Links | Link-Code, verknüpft mit dem Freitext des Besuchers | Neon, Logs, Cookie | Zeile bleibt |

Die vollständige Tabelle mit Code-Belegen, Anbieterquellen und offenen Punkten steht in [docs/DATENFLUSS.md](docs/DATENFLUSS.md). Die drei Anfragen an Anthropic für T01 stehen dort wörtlich, mit jedem personenbezogenen Feld markiert: [evals/t01_anfragen.md](evals/t01_anfragen.md).

**Pseudonymisierung würde alle 8 direkten Identifikatoren aus der T01-Anfrage des Agents entfernen.**
Der Agent braucht die Kunden-ID, die Kontodaten und die Zahlungen. Die E-Mail-Adresse braucht er nicht, denn der Code kennt den Absender schon. Den Namen braucht er auch nicht: Er dient nur der Anrede, und das kann ein Platzhalter übernehmen. Beträge, Daten und der Freitext selbst lassen sich nicht ersetzen. Im Goldset hat nur T14 eine E-Mail-Adresse im Text, und kein Ticket hat einen Namen. Echte E-Mails enden meist mit einer Grußzeile, die das Goldset nicht abbildet. Das ist nur eine Analyse, geändert wurde nichts: [docs/DATENMINIMIERUNG.md](docs/DATENMINIMIERUNG.md).

## Schritt 2: AI-Act-Einstufung

**Begrenztes Risiko: keine verbotene Praxis, kein Hochrisiko, Art. 50 gilt seit 2.8.2026.**
FocusFlow baut den Agent und nutzt ihn selbst, ist also **Anbieter und Betreiber** zugleich (Art. 3(3), 3(11); die Art.-50-Leitlinien der Kommission nennen genau diesen Fall). Anthropic ist Anbieter des Modells mit allgemeinem Verwendungszweck. Keines der Verbote aus Art. 5 greift. Kundenservice, Erstattungen und Kündigungen stehen nicht in Anhang III. Hochriskant würde es, wenn der Agent Zahlungsverhalten für Kreditentscheidungen bewertet (5(b)), Support-Mitarbeiter einzeln auswertet (4(b)) oder im Sprachsupport Emotionen erkennt (1(c)).

Was jetzt gilt:
- **Art. 50(1):** Kunden müssen erfahren, dass sie es mit KI zu tun haben. Die Leitlinien nennen Helpdesk-Chatbots ausdrücklich. Heute steht im Portal sogar „A human checks it before it is sent“, obwohl bei Entwürfen ohne Empfehlung niemand prüft.
- **Art. 50(2):** maschinenlesbare Kennzeichnung von KI-Text. Die Übergangsfrist bis 2.12.2026 gilt nur für Systeme, die vor dem 2.8.2026 in Verkehr gebracht wurden.
- **Art. 4:** Maßnahmen zur KI-Kompetenz, in der Fassung des Digital Omnibus (Verordnung (EU) 2026/1744, in Kraft seit 27.7.2026, in EUR-Lex geprüft): kein „ausreichendes Niveau“ mehr, die Pflicht bleibt. Hochrisiko-Pflichten verschieben sich auf 2.12.2027 (Anhang III) und 2.8.2028 (Anhang I).

Details: [docs/AI_ACT.md](docs/AI_ACT.md).

## Schritt 3: DSGVO-Prüfung und Pflichten-Backlog

- **Rechtsgrundlage:** Ticketbearbeitung Art. 6(1)(b), Judge-Stichprobe und Logs Art. 6(1)(f). Ob ein LLM für (b) „erforderlich“ ist, steht als „mit Legal klären“ drin.
- **DSFA nötig:** Die DSK-Muss-Liste nennt „Kundensupport mittels künstlicher Intelligenz“ (Nr. 11).
- **Transfer zu Anthropic:** SCC Modul 2/3 plus Transfer Impact Assessment, sofern Anthropic nicht DPF-zertifiziert ist (nicht geprüft).
- **Löschfristen:** Der Code löscht heute nichts. Buchungsbelege 8 Jahre, Handelsbriefe 6 Jahre (HGB §257, geprüft), alles andere braucht eine festgelegte Frist.
- **Art. 22:** Die Auto-Erstattung aus UC8 ist eine ausschließlich automatisierte Entscheidung; ob eine rein begünstigende Entscheidung erfasst ist, ist offen. Zwei Funde gibt es schon ohne die Option: Ablehnungen von Geldwünschen erreichen den Kunden ohne Menschen, und der Agent führt Kündigungen selbst aus.

**28 Pflichten, 19 vor dem Go-live, heute 0 erfüllt.** Jeder Eintrag hat eine Anforderung in Produktsprache, die Rechtsgrundlage, den heutigen Stand in UC7 mit Datei und Zeile, Aufwand und Priorität: [docs/BACKLOG.md](docs/BACKLOG.md). Für zwei Einträge steht der genaue Text dabei, den der Kunde sieht (Hinweis im Formular, Kennzeichnung einer autonomen Antwort).

## Funde, die nicht im Code stehen
- **Das Agent SDK ergänzt eigenen Kontext.** Bei einem lokalen Lauf hat die gebündelte CLI zwei Dinge in die Anfrage des Support-Agents gelegt: das Auto-Memory des Entwicklers und den Benutzerpfad des Rechners. Das geschah trotz `setting_sources=[]`. Laut Anthropic schreibt die CLI außerdem Klartext-Transkripte (standardmäßig 30 Tage) und erzeugt Sitzungstitel mit einem zusätzlichen Modellaufruf. Ob das im Container genauso passiert, ist offen.
- **Link-Codes landen in den Logs.** Der Code eines persönlichen Links steht in der URL. Cloud Run protokolliert ihn deshalb zusammen mit der IP-Adresse (4 Einträge in den letzten 30 Tagen).
- **Die Anthropic-Quellen widersprechen sich bei der Aufbewahrung.** Das Privacy Center sagt, Ein- und Ausgaben werden „within 30 days“ gelöscht. Die API-Doku sagt, Inhalte würden „not retained by default“. Die Planung geht von bis zu 30 Tagen aus.

## Anbieter (Primärquellen, 2026-10-08)

| | DPA | Rolle | Transfergrundlage | Ort |
|---|---|---|---|---|
| Anthropic | ja, Teil der Commercial Terms | Auftragsverarbeiter | SCC Modul 2/3; DPF nicht genannt | gespeichert in den USA, Inferenz „global“ oder „us“ |
| Google Cloud | ja, CDPA | Auftragsverarbeiter | SCC, sofern keine Alternativlösung gilt; Google LLC DPF-zertifiziert | gewählte Region für gelistete Dienste; Logs und Secrets „global“ |
| Neon (Databricks) | ja, über die Platform Terms | auf neon.com nicht ausdrücklich genannt | offen | eine Region je Projekt; Backups 30 Tage |

## Kosten & Latenz
- Kosten pro 1000 Requests: entfällt für diesen Schritt (0 USD, keine API-Aufrufe). Der untersuchte Agent kostet 34,1 USD je 1000 Anfragen (UC7).
- p95-Latenz: 39,7 s je Agent-Lauf (UC7, unverändert).
- Qualitätsmetrik: 5 von 11 Stationen ohne Zusage eines EU-Standorts. Die letzte T01-Anfrage des Agents hat 64 personenbezogene Fundstellen, 8 davon direkte Identifikatoren. Pflichten-Backlog: 28 Einträge, 19 vor dem Go-live, heute 0 erfüllt.

## Nächste Schritte
- Die Punkte „mit Legal klären“ mit Legal besprechen (am Ende von AI_ACT.md und DSGVO.md gelistet).
- Offene Recherche schließen: DPF-Status und Unterauftragsverarbeiter von Anthropic, Widerspruch zur Aufbewahrung, Neon-DPA, das SDK im Container.
- Die Go-live-Einträge des Backlogs bauen, zuerst die KI-Hinweise (B01-B03) und die SDK-Einstellungen (B20).

Details: [AI Act](docs/AI_ACT.md) · [DSGVO](docs/DSGVO.md) · [Backlog](docs/BACKLOG.md) · [Datenfluss](docs/DATENFLUSS.md) · [Datenminimierung](docs/DATENMINIMIERUNG.md) · [T01-Anfragen](evals/t01_anfragen.md) · [Entscheidungen](docs/decisions.md)
