# Pflichten-Backlog für den Go-live mit echten Kunden

Stand 2026-10-08. **Keine Rechtsberatung.** Jeder Eintrag folgt aus [AI_ACT.md](AI_ACT.md), [DSGVO.md](DSGVO.md) oder der Inventur ([DATENFLUSS.md](DATENFLUSS.md), [DATENMINIMIERUNG.md](DATENMINIMIERUNG.md)). Code-Belege beziehen sich auf `ai-uc-07-deployment`, Commit `75c5ea3`.

**Legende**
- **Stand:** ✅ erfüllt · ◐ teilweise · ✗ fehlt
- **Aufwand:** S = bis 1 Tag, M = bis 1 Woche, L = länger. Grob geschätzt, nicht gemessen.
- **Go-live:** „ja“ = vor dem Go-live mit echten Kunden. „ja*“ = ja, solange Legal nicht anders entscheidet.

## Backlog

| ID | Anforderung (Produktsprache) | Rechtsgrundlage | Stand in UC7 | Aufwand | Go-live |
|---|---|---|---|---|---|
| **Transparenz und Kennzeichnung** |||||||
| B01 | **Ticket-Formular zeigt vor dem Absenden einen KI- und Datenschutz-Hinweis** (Text unten) mit Link zur Datenschutzerklärung | Art. 50(1), (5) KI-VO; Art. 13 DSGVO, WP260 Rn. 36 | ✗ Formular ohne Hinweis (`app/templates/anliegen.html:36-41`) | S | ja |
| B02 | **Jede Antwort, die der Agent ohne Menschen schreibt, trägt eine KI-Kennzeichnung** (Text unten) mit Knopf „Mit einem Menschen klären“. Die heutige Aussage „A human checks it before it is sent“ entfällt. | Art. 50(1) KI-VO; Art. 5(1)(a) DSGVO (Treu und Glauben) | ✗ und irreführend: Der Text behauptet eine Prüfung (`app/templates/_entwurf.html:6`), der Code zeigt den Entwurf ungeprüft (`app/main.py:212-214`) | S | ja |
| B03 | **Antwort nach einer Entscheidung nennt beides:** „Entschieden von unserem Team, formuliert von unserem KI-Assistenten“ | Art. 50(1) KI-VO | ◐ nennt die Entscheidung, nicht die KI-Formulierung (`app/templates/_entwurf.html:22-27`) | S | ja |
| B04 | **KI-Texte sind maschinenlesbar gekennzeichnet**, z. B. Metadaten im Portal-HTML und im E-Mail-Header. Vorher klären, ob Anthropic selbst markiert. | Art. 50(2) KI-VO; keine Übergangsfrist (Art. 111(4) greift nicht) | ✗ | M | ja* (Umsetzungsweg mit Legal klären) |
| B05 | **Ablehnungen von Geldwünschen gehen nicht autonom raus.** Sagt der Entwurf „keine Erstattung“, landet er in der Konsole wie heute schon Entwürfe mit Zusage. | Art. 22 DSGVO (mit Legal klären) | ✗ Die Ablehnung geht direkt an den Kunden (`app/main.py:212-214`, Regel `uc4_agent/werkzeuge.py:82-84`); das Prüfmuster gibt es schon für Zusagen (`app/main.py:632-650`) | M | ja* |
| B06 | **Datenschutzerklärung hat einen Abschnitt „Support und KI-Assistent“** mit allen Angaben aus DSGVO.md, Abschnitt 2 | Art. 13 DSGVO | ✗ nur Demo-Fuß (`app/templates/base.html:42`) | S | ja |
| **Verträge, Dokumentation, Kompetenz** |||||||
| B07 | **AVVs liegen abgelegt und geprüft vor:** Anthropic (DPA in den Commercial Terms), Google (CDPA), Neon / Databricks (Platform Terms, MCSA, DPA-PDF), je mit der Liste der Unterauftragsverarbeiter | Art. 28 DSGVO | ◐ per AGB akzeptiert, nicht dokumentiert; Neon-Rolle und Anthropic-Unterauftragsverarbeiter offen (DATENFLUSS.md) | S | ja |
| B08 | **Transfer Impact Assessment für Anthropic (USA)** mit DPF-Status, SCC Modul 2/3 und ergänzenden Maßnahmen (B13, B14) | Art. 44, 46(2)(c) DSGVO; SCC Klausel 14(d); EDPB 01/2020 | ✗ | M | ja |
| B09 | **Verzeichnis von Verarbeitungstätigkeiten** mit V1-V12 | Art. 30 DSGVO | ✗ | S | ja |
| B10 | **Datenschutz-Folgenabschätzung** vor dem Go-live | Art. 35 DSGVO; DSK Muss-Liste Nr. 11 | ◐ Die Inventur liefert Teil (a) von Art. 35(7) | M | ja |
| B11 | **Konsole-Mitarbeiter sind geschult:** Grenzen des Agents, Automation Bias, wann übergeben. Kurz dokumentiert. | Art. 4 KI-VO (Fassung Omnibus) | ◐ Die Konsole zeigt Regelprüfung und Warnungen (`app/main.py:594-610`), die Schulung fehlt | S | ja |
| B12 | **Judge-Stichprobe ist als berechtigtes Interesse dokumentiert** (Dreistufentest) und in der Datenschutzerklärung genannt | Art. 6(1)(f), 13(1)(d) DSGVO; EDPB 2/2019 Rn. 48-49 | ◐ Die Stichprobe läuft (`app/pruefung.py:26`, `:135-137`), die Abwägung fehlt | S | ja |
| **Datenminimierung** |||||||
| B13 | **Das Modell bekommt keine E-Mail und keinen Namen:** Ticketkopf mit Kunden-ID, Name als `{vorname}`, eingesetzt erst bei der Anzeige. Design, Testansatz und Messplan im [Ausblick unten](#ausblick-b13-pseudonymisierung-vor-dem-modell) (Messung ca. 5,20 USD, nach Freigabe). | Art. 5(1)(c), 25 DSGVO; ergänzende Maßnahme für B08 | ✗ E-Mail im Ticketkopf (`uc4_agent/agent.py:182`), Name im Werkzeug-Ergebnis (`uc4_agent/werkzeuge.py:268-270`), Anrede mit Vornamen (`app/antwort.py:24`) | M | nein (stärkt B08, empfohlen) |
| B14 | **Nur Zahlungen der letzten 13 Monate gehen ans Modell** | Art. 5(1)(c) DSGVO | ✗ ganze Historie (`uc4_agent/werkzeuge.py:272-275`) | S | nein |
| B15 | **Betriebsseite zeigt keine Namen und keine Freitext-Titel**, nur Run-ID und Kennzahlen | Art. 5(1)(c) DSGVO | ✗ Titel aus Freitext und Name (`app/hinweise.py:67-79`, `app/templates/betrieb.html:73`) | S | nein |
| B16 | **Der Kunde kommt aus dem Login, nicht aus einer Auswahlliste** aller Kunden | Art. 5(1)(f), 32 DSGVO | ✗ Liste aller 15 Kunden mit E-Mail (`app/templates/anliegen.html:26`); in der Demo gewollt | M | ja |
| **Logs, Speicher, Löschen** |||||||
| B17 | **Request-Logs: eigener Bucket in `europe-west3`, Frist festgelegt** (Vorschlag 7 Tage), `_Default` umgeleitet | Art. 5(1)(e), 6(1)(f) DSGVO | ✗ `_Default` am Ort „global“, 30 Tage (DATENFLUSS.md, Station 7) | S | ja |
| B18 | **Logs enthalten keine Link-Codes:** Code per POST statt Query-String, oder das Feld vor dem Logging entfernen | Art. 5(1)(c) DSGVO | ✗ Code in der URL (`app/main.py:282-292`), 4 Einträge im Log | S | nein (nur Demo-Funktion) |
| B19 | **Fälle werden nach Frist automatisch gelöscht oder anonymisiert** (Vorschlag 90 Tage, Ausnahmen für Belege), auch Link-Codes nach Ablauf | Art. 5(1)(e), 17 DSGVO | ✗ kein `DELETE` im Code (`app/speicher.py`), Rolle ohne `DELETE` (`docs/deploy.md:47-48`) | M | ja |
| B20 | **Das Agent-SDK im Container schreibt keine Transkripte und sendet keine Telemetrie:** `CLAUDE_CODE_SKIP_PROMPT_HISTORY`, `DISABLE_TELEMETRY` bzw. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` gesetzt; leeres `HOME` ohne Memory; Titel-Aufruf geprüft (ein Lauf ca. 0,03 USD) | Art. 5(1)(c), 28, 32 DSGVO | ✗ Die CLI schreibt nach `$HOME/.claude` (`Dockerfile:10-11`), keine dieser Variablen ist gesetzt (`docs/deploy.md:85`); Memory und Pfad im Kontext lokal belegt | S | ja |
| B21 | **Laufdateien `/daten/laeufe/<run_id>/` werden nicht mehr geschrieben**, das Protokoll liegt nur in Neon | Art. 5(1)(c) DSGVO | ✗ (`app/lauf.py:125`, `uc4_agent/werkzeuge.py:236-238`) | S | nein (Instanz ist flüchtig) |
| B22 | **Das Replay zeigt nur einen synthetischen Fall.** Regel: Echte Kundenfälle werden nie exportiert. | Art. 5(1)(b), 6 DSGVO | ◐ Heute fiktive Daten, aber der Export aus Neon ist vorgesehen (`scripts/replay_export.py:22-39`, `app/main.py:64`) | S | ja |
| B23 | **Die interne Notiz zeigt den Hinweis „keine Gesundheitsangaben, keine Bankdaten“** | Art. 5(1)(c) DSGVO | ◐ Sie geht an kein Modell (`app/speicher.py:272-276`), der Hinweis fehlt (`app/templates/konsole.html:52`) | S | nein |
| **Betroffene und Entscheidungen** |||||||
| B24 | **Auskunft und Löschung je Kunde auf Knopfdruck**, über alle Tabellen inklusive JSON-Spalten | Art. 15, 17 DSGVO | ✗ | M | ja |
| B25 | **Eine Kündigung durch den Agent wird bestätigt:** Wirksamkeitsdatum plus Weg zu einem Menschen | Art. 22 DSGVO (mit Legal klären); Art. 5(1)(a) | ◐ Kündigung zum Periodenende im Werkzeug-Ergebnis (`uc4_agent/werkzeuge.py:323-325`), kein fester Bestätigungstext | S | ja* |
| B26 | **Falls die Auto-Erstattung kommt:** Hinweis „automatisch erstattet“, Logik in einem Satz, Anfechtung über „Mit einem Menschen klären“, Obergrenze je Kunde | Art. 22(3), 13(2)(f) DSGVO (mit Legal klären) | – Option aus UC8, nicht gebaut | M | nein (erst mit der Option) |
| B27 | **Zero Data Retention bei Anthropic anfragen** und die Antwort dokumentieren | Art. 5(1)(e), 44 DSGVO | ✗ | S | nein |
| B28 | **Secret Manager mit nutzerverwalteter Replikation in der EU** | Art. 32 DSGVO (keine personenbezogenen Daten) | ✗ `--replication-policy=automatic` (`docs/deploy.md:33`) | S | nein |

**Zählung:** 28 Einträge, 19 davon vor dem Go-live (davon 3 mit „ja*“). Stand heute: 0 erfüllt, 8 teilweise, 19 fehlen, 1 nicht gebaut (B26).

## Anschauung: zwei Texte, die der Kunde sieht

Deutsch und per Du, wie der restliche Support (`app/antwort.py:24`). Beide sind Vorschläge für Legal und Produkt, nicht freigegeben.

### B01: Hinweis im Ticket-Formular

Steht über dem Knopf „Anfrage senden“, also vor der ersten Interaktion (Art. 50(5) KI-VO):

> **Unser KI-Assistent bearbeitet deine Anfrage zuerst.**
> Er sieht dafür dein Konto und deine Zahlungen ein und schreibt eine Antwort. Über Erstattungen entscheidet immer ein Mensch aus unserem Team. Wenn dir etwas an der Antwort nicht passt, kannst du jederzeit einen Menschen dazuholen.
>
> Für den Assistenten nutzen wir Claude von Anthropic. Deine Anfrage wird dafür in die USA übermittelt, auf Grundlage von EU-Standardvertragsklauseln. Anthropic verwendet sie nicht zum Training. Mehr dazu in unserer [Datenschutzerklärung, Abschnitt „Support“](#).
>
> Bitte schreib keine Gesundheitsdaten, Passwörter oder Bankdaten in die Nachricht.

Warum so:
- Der erste Satz erfüllt Art. 50(1).
- Der zweite Absatz ist die erste Ebene nach WP260, Rn. 36 (Empfänger, Drittland, Garantie). Ist Anthropic DPF-zertifiziert (B08), ändert sich die Garantie im Text.
- Der letzte Satz dient der Minimierung beim Freitext, dem größten Restrisiko (DATENMINIMIERUNG.md).

### B02: Kennzeichnung einer autonomen Antwort

Steht über jeder Antwort, die der Agent ohne menschliche Prüfung schreibt, und ersetzt „Draft. A human checks it before it is sent.“ (`app/templates/_entwurf.html:6`):

> 🤖 **Diese Antwort hat unser KI-Assistent geschrieben.** Niemand aus unserem Team hat sie vor dem Versand gelesen.
> Stimmt etwas nicht oder bist du nicht einverstanden? **[Mit einem Menschen klären]**. Dann sieht sich jemand aus dem Team deinen Fall an und meldet sich bei dir.

Hat der Agent eine Kündigung ausgeführt (B25), kommt hinzu:

> Dein Abo ist zum **14.09.2027** gekündigt. Bis dahin kannst du Pro weiter nutzen. Wolltest du nicht kündigen? **[Mit einem Menschen klären]**

Warum so:
- Der erste Satz erfüllt Art. 50(1). Die LL Art. 50 lassen die bloße Möglichkeit einer Prüfung nicht als Ausnahme gelten. Deshalb steht ausdrücklich da, dass niemand gelesen hat.
- Der Knopf ist der Weg zum Menschen. Nach Art. 22(3) wäre er Pflicht, falls Legal die Kündigung als Entscheidung einstuft. Er hilft aber auch sonst.
- Das Datum kommt aus dem Werkzeug-Ergebnis (`wirksam_zum`, `uc4_agent/werkzeuge.py:323-325`), nicht aus dem Modell. Das Beispiel zeigt das Abo-Ende von K001.

## Ausblick B13: Pseudonymisierung vor dem Modell

Nur Konzept, nicht gebaut. Grundlage: [DATENMINIMIERUNG.md](DATENMINIMIERUNG.md). Code-Belege beziehen sich auf `ai-uc-07-deployment`, Commit `75c5ea3`.

### Design

1. **Ticketkopf mit Kunden-ID statt E-Mail.** `ticket_prompt` (`uc4_agent/agent.py:181-182`) schreibt `Kunden-ID: K001` statt `Von: anna.berger@example.com`. Der Code kennt den Absender schon aus der Sitzung (`app/lauf.py:123-125`). Die Konto-Bindung prüft weiter gegen `absender_id` (`uc4_agent/werkzeuge.py:212-234`). Prompt v3, Schritt 1 und 5, sagen „Kunden-ID des Absenders“ statt „Absender-Adresse“. Das ist eine Prompt-Änderung und braucht deshalb die Messung unten.
2. **Werkzeug-Ergebnisse ohne Name und E-Mail.** `kunde_nachschlagen` (`uc4_agent/werkzeuge.py:268-270`) gibt die Felder `name` und `email` nicht ans Modell zurück. Gesucht wird nur noch per Kunden-ID. Die Suche per Namensteil entfällt, sie trifft bei Namensgleichen (K006/K007) ohnehin fremde Konten.
3. **Anrede im Code.** Agent, Haiku-Neuschreiben (`app/antwort.py:24`) und Judge sehen `{vorname}`. Eingesetzt wird der Vorname erst bei der Anzeige und beim Versand, wie heute schon in der Vorlage (`app/antwort.py:28-29`). Eine Regel ohne LLM prüft: `{vorname}` steht genau einmal und unverändert im Text. Sonst geht der Text an die Konsole.
4. **Fremde E-Mail-Adressen einheitlich ersetzen.** Vor dem Modell ersetzt der Code jede E-Mail-Adresse im Freitext durch ein Token: die des Absenders durch `<E-Mail des Absenders>`, jede andere durch `<E-Mail 2>`, `<E-Mail 3>` usw. Die Zuordnung gilt für den ganzen Lauf, also für Ticket, Werkzeug-Ergebnisse, Entwurf und Judge. Bei **T14** („kündigt das Abo auf meinem Google-Konto felix.braun@gmail.com“) sieht der Agent dann `<E-Mail 2>`. Er erkennt weiter, dass ein anderes Konto gemeint ist, und übergibt. Würde nur der Ticketkopf ersetzt, nicht aber der Text, ginge genau diese Unterscheidung verloren.
5. **Zurückübersetzen nur für Menschen.** Konsole und Kundenportal zeigen die echten Werte. Im Protokoll (Neon) liegen beide Fassungen, die pseudonyme für Prüfungen.

### Testansatz: die verschickte Anfrage abfangen, nicht die Konfiguration prüfen

Der SDK-Fund aus Schritt 1 zeigt: `setting_sources=[]` stand in der Konfiguration, trotzdem lagen Auto-Memory und Benutzerpfad in der Anfrage. Ein Test, der nur prüft, welche Parameter gesetzt sind, hätte das nicht gefunden.

- **Abfangen statt prüfen:** Die CLI im Agent SDK liest `ANTHROPIC_BASE_URL` („Override the API endpoint to route requests through a proxy or gateway“, https://code.claude.com/docs/en/env-vars). Der Test startet einen lokalen Stub-Server, der jede Anfrage speichert und feste Antworten zurückgibt (Werkzeugaufrufe aus einem aufgezeichneten Lauf). **Das kostet kein API-Geld.** Geprüft wird der rohe Request-Body jeder Anfrage, auch von Hintergrund-Aufrufen wie dem Sitzungstitel.
- **Prüfregeln:** Kein Name, keine E-Mail, keine Telefonnummer aus `kunden.json` und keine echte Adresse aus dem Ticket in irgendeinem Request. Kein Pfad mit Benutzernamen, kein Memory-Inhalt. Für jedes Goldset-Ticket einmal.
- **Gleiches für Judge und Haiku:** Auch deren Client zeigt im Test auf den Stub. Ob das Python-SDK `anthropic` die Variable ebenfalls liest, prüft der Test selbst: Er schlägt fehl, wenn kein Request am Stub ankommt.
- **Im Container laufen lassen,** nicht nur lokal, weil `HOME` und Arbeitsverzeichnis den Inhalt ändern (B20).

### Messplan: Qualität mit und ohne Pseudonymisierung

- **Zwei Arme, gleicher Tag, gleiches Modell:** frische Kontrolle auf `main` (heutiger Code) gegen den Branch mit Pseudonymisierung. 15 Goldset-Tickets × 3 Läufe je Arm. Die alten UC6-Werte (34 von 45) dienen nicht als Kontrolle, weil sich Code und Modellstand seitdem geändert haben.
- **Bewertung mit Judge j2,** wie die veröffentlichten UC4- und UC6-Werte. Bekannte Schwäche: j2 kennt das Datum „heute“ nicht und wertet korrekte Fristschlüsse teils als Spekulation (UC4, `docs/decisions.md:416`). Der Fehler trifft beide Arme gleich, der Vergleich bleibt fair. Für absolute Werte wäre j3 besser.
- **Zusätzlich ohne LLM:** `{vorname}`-Regel, T14 übergibt, keine E-Mail im Request (Stub-Test oben).
- **Kosten, erst schätzen, dann laufen:**

| Posten | Rechnung | Betrag |
|---|---|---|
| Agent-Läufe | 2 × 45 × 0,028–0,0341 USD (UC6 gemessen bzw. UC7 34,1 USD/1000) | 2,52–3,07 USD |
| Judge j2 | 90 Urteile × 0,0199 USD (UC4: 2,69 USD für 135 Urteile) | 1,79 USD |
| **Summe** | | **4,31–4,86 USD** |
| Freigabe mit Puffer (Probelauf, Wiederholungen) | | **ca. 5,20 USD** |

- **Entscheidungsregel, vorab festgelegt:** Der Branch darf höchstens 2 Läufe schlechter sein als die Kontrolle (bei n = 45 liegt das im Rauschen, UC6: „T13 ist Streuung bei identischem Input“). T14 muss in allen 3 Läufen übergeben.

### Offenes Risiko: Freitext

- **Grußzeilen:** „Viele Grüße, Anna Berger“ steht in fast jeder echten E-Mail, im Goldset in keinem Ticket. Namen aus dem eigenen Kundenstamm lassen sich ersetzen. Fremde Namen (Partner, Kinder, Mitarbeiter) erkennt keine Liste.
- **Telefonnummern, Adressen, IBAN:** per Muster ersetzbar, aber unvollständig (Schreibweisen, Leerzeichen, Ländervorwahlen).
- **Gesundheitsangaben** („war im Krankenhaus, deshalb nicht genutzt“) sind besondere Kategorien nach Art. 9 DSGVO und mit Mustern nicht zu finden. Hier hilft nur der Hinweis im Formular (B01) und die DSFA (B10).
- **Folge:** Pseudonymisierung senkt das Risiko, sie anonymisiert nicht. Die Pflichten aus B07, B08 und B10 bleiben bestehen. Messbar wird das Restrisiko erst mit echten oder realistisch nachgebauten Tickets mit Grußzeile. Das Goldset deckt das nicht ab.
