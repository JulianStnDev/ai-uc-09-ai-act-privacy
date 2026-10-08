🇬🇧 [English version](README.md)

# UC9: AI Act & Datenschutz für den Support-Agent

> Entscheidungs- und Pflichtenvorlage, kein Produktcode. Die Frage: Was müsste gelten, wenn ab morgen echte Kundentickets in den UC7-Support-Agent gingen? Schritt 1 ist eine Datenfluss-Inventur aus dem Code. Jede Aussage ist mit Datei und Zeile oder mit einer Primärquelle des Anbieters belegt. Kosten: 0 USD, keine API-Aufrufe.

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
- Qualitätsmetrik: 5 von 11 Stationen ohne Zusage eines EU-Standorts. Die letzte T01-Anfrage des Agents hat 64 personenbezogene Fundstellen, 8 davon direkte Identifikatoren.

## Nächste Schritte
- Die offenen Punkte klären: Unterauftragsverarbeiter von Anthropic, den Widerspruch zur Aufbewahrung, den Neon-DPA und was das SDK im Container tut.
- Den Agent nach dem AI Act einstufen, danach die Pflichtenvorlage schreiben.

Details: [Datenfluss](docs/DATENFLUSS.md) · [Datenminimierung](docs/DATENMINIMIERUNG.md) · [T01-Anfragen](evals/t01_anfragen.md) · [Entscheidungen](docs/decisions.md)
