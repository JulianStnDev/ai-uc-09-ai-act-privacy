# DSGVO-Prüfung des UC7-Support-Agents

Stand 2026-10-08. **Keine Rechtsberatung.** Grundlage ist die Inventur in [DATENFLUSS.md](DATENFLUSS.md). Wo die Auslegung offen ist, steht **„mit Legal klären“**. Code-Belege beziehen sich auf `ai-uc-07-deployment`, Commit `75c5ea3`.

## Quellen

| Kürzel | Dokument | Fundstelle |
|---|---|---|
| DSGVO | VO (EU) 2016/679 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:32016R0679 |
| SCC | Durchführungsbeschluss (EU) 2021/914, ABl. L 199/31 vom 7.6.2021 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:32021D0914 |
| DPF | Angemessenheitsbeschluss (EU) 2023/1795, ABl. L 231/118 vom 20.9.2023 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:32023D1795 |
| EDPB 2/2019 | Leitlinien zu Art. 6(1)(b), Version 2.0, 8.10.2019 | https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines-art_6-1-b-adopted_after_public_consultation_en.pdf |
| EDPB 1/2024 | Leitlinien zu Art. 6(1)(f), Version 1.0 (Konsultationsfassung), 8.10.2024 | https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202401_legitimateinterest_en.pdf |
| EDPB 01/2020 | Empfehlungen zu ergänzenden Maßnahmen, Version 2.0, 18.6.2021 | https://www.edpb.europa.eu/system/files/2021-06/edpb_recommendations_202001vo.2.0_supplementarymeasurestransferstools_en.pdf |
| EDPB DPF-Note | Information Note zum DPF, Juli 2023 | https://www.edpb.europa.eu/system/files/2023-07/edpb_informationnoteadequacydecisionus_en.pdf |
| WP260 | Leitlinien Transparenz, rev.01, 11.4.2018 | https://ec.europa.eu/newsroom/article29/redirection/document/51025 |
| WP251 | Leitlinien automatisierte Entscheidungen, rev.01, 6.2.2018 | https://ec.europa.eu/newsroom/article29/redirection/document/49826 |
| WP248 | Leitlinien DSFA, rev.01, 4.10.2017 (DE) | https://www.datenschutzkonferenz-online.de/media/wp/20171004_wp248_rev01.pdf |
| DSK Muss-Liste | DSFA-Liste, Version 1.1, 17.10.2018 | https://www.datenschutzkonferenz-online.de/media/ah/20181017_ah_DSK_DSFA_Muss-Liste_Version_1.1_Deutsch.pdf |
| DSK OH KI | Orientierungshilfe KI und Datenschutz, Version 1.0, 6.5.2024 | https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf |
| EuGH SCHUFA | C-634/21, Urteil vom 7.12.2023 | https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:62021CJ0634 |
| EuG Latombe | T-553/23, Urteil vom 3.9.2025, Pressemitteilung 106/25; Rechtsmittel C-703/25 P | https://curia.europa.eu/site/upload/docs/application/pdf/2025-09/cp250106de.pdf |
| HGB, AO | § 257 HGB, § 147 AO | https://www.gesetze-im-internet.de/hgb/__257.html, https://www.gesetze-im-internet.de/ao_1977/__147.html |

Selbst am Original geprüft: § 257 Abs. 4 HGB (10 / 8 / 6 Jahre) und Nr. 11 der DSK-Muss-Liste. Die übrigen Zitate stammen aus Recherche-Abrufen derselben Quellen.

## 1. Rechtsgrundlage je Verarbeitung

FocusFlow ist Verantwortlicher. Anthropic, Google Cloud und Neon sind Auftragsverarbeiter (siehe DATENFLUSS.md, Anbieter). Bei Neon steht das auf neon.com nicht ausdrücklich, daher B07. Die Weitergabe an einen Auftragsverarbeiter braucht keine eigene Rechtsgrundlage, wohl aber einen Vertrag nach Art. 28 und für die USA Kapitel V (siehe 3).

| # | Verarbeitung | Rechtsgrundlage (Einschätzung) | Begründung, Quelle |
|---|---|---|---|
| V1 | Ticket annehmen, Konto und Zahlungen nachschlagen, Antwort entwerfen (Agent) | Art. 6(1)(b) | EDPB 2/2019, Example 3: Problem eines Kunden beheben „can be based on Article 6(1)(b)“, Rn. 38 „correcting errors“. **Mit Legal klären:** Ist der Einsatz eines LLM „objektiv erforderlich“ (Rn. 25: „If there are realistic, less intrusive alternatives, the processing is not ‘necessary’“)? Wenn nicht: Art. 6(1)(f) mit Abwägung. Kein Primärtext entscheidet das. |
| V2 | Alle Zahlungen des Kunden ins Modell (`uc4_agent/werkzeuge.py:272-275`) | wie V1, aber nur das Nötige | Art. 5(1)(c). Für die Erstattungsregel reichen die letzten 13 Monate (DATENMINIMIERUNG.md). Ältere Zahlungen sind „useful but not objectively necessary“ (Rn. 25). |
| V3 | Abo kündigen auf Wunsch (`uc4_agent/werkzeuge.py:311-328`) | Art. 6(1)(b) | Erfüllung des Kündigungswunsches. Art. 22 siehe 6. |
| V4 | Erstattungsempfehlung, Entscheidung in der Konsole | Art. 6(1)(b) | Vertragsabwicklung. Buchhaltung danach Art. 6(1)(c) (EDPB 2/2019, Example 4). |
| V5 | Endgültige Antwort durch Haiku | Art. 6(1)(b) | wie V1 |
| V6 | Judge-Stichprobe 20 % (`app/pruefung.py:26`, `:135-137`) | **Art. 6(1)(f)** | Qualitätssicherung ist Serviceverbesserung. EDPB 2/2019, Rn. 49: (b) ist dafür „generally“ nicht geeignet, Rn. 48: berechtigtes Interesse kommt in Betracht. Dreistufentest nach EDPB 1/2024: Interesse (fehlerhafte Antworten finden), Erforderlichkeit (Stichprobe statt alles, pseudonymisierbar), Abwägung (gleicher Auftragsverarbeiter, kein neuer Empfänger). Dokumentieren. |
| V7 | Protokoll in Neon (`app/speicher.py:17-76`) | während des Falls (b); Belegteile (c); Rest bis Fristende (f), danach löschen | EDPB 2/2019, Rn. 41: nach Vertragsende nicht auf eine neue Grundlage „umschwenken“. Rn. 43: Aufbewahrungsgrund „at the outset“ festlegen. Siehe 4. |
| V8 | Request-Logs mit IP, User-Agent, URL (Cloud Run) | Art. 6(1)(f) | Betrieb und Sicherheit, EDPB 1/2024, Rn. 126 („may, in principle, be based on Article 6(1)(f)“). Frist festlegen. Link-Codes gehören nicht hinein (Art. 5(1)(c)). |
| V9 | Betriebsseite: Kosten, Dauer, Titel aus Freitext, Name (`app/templates/betrieb.html:73`) | Art. 6(1)(f) | Kennzahlen ja. Name und Freitext-Titel sind dafür nicht nötig (Art. 5(1)(c)). |
| V10 | Replay eines echten Falls an jeden Besucher (`app/main.py:64`, `:364-394`) | **keine** | Mit echten Kundendaten gibt es keine Rechtsgrundlage für eine Veröffentlichung. Nur synthetische Fälle verwenden. |
| V11 | Interne Notiz der Konsole (`app/speicher.py:67`) | Art. 6(1)(b)/(f) | Geht an kein Modell (`app/speicher.py:272-276`). Inhalt ist frei, deshalb Hinweis an Mitarbeiter: keine sensiblen Angaben. |
| V12 | Telemetrie und Transkripte der Agent-SDK-CLI im Container | keine eigene; abschalten | Laut Anthropic enthalten die Metriken keine Prompts. Transkripte enthalten aber den ganzen Fall und sind nicht nötig (Art. 5(1)(c)). |

## 2. Informationspflichten (Art. 13): was in die Datenschutzerklärung muss

Daten werden beim Kunden erhoben (Ticket) bzw. liegen aus dem Vertrag vor, also gilt Art. 13. Nach WP260, Rn. 36 gehört in die **erste Ebene**, was „the most impact on the data subject and processing which could surprise them“ hat. Ein KI-Agent, der Konto und Zahlungen liest und Daten in die USA sendet, gehört dazu. Deshalb steht ein Kurzhinweis direkt am Formular (BACKLOG B01), die Details stehen in der Datenschutzerklärung.

Abschnitt „Support-Anfragen und KI-Assistent“ der Datenschutzerklärung:

| Pflichtangabe | Inhalt für FocusFlow | Norm |
|---|---|---|
| Verantwortlicher, ggf. DSB | Name, Anschrift, Kontakt | 13(1)(a), (b) |
| Zwecke und Rechtsgrundlagen | Anfrage bearbeiten (V1-V5, Art. 6(1)(b)); Qualitätsstichprobe (V6, Art. 6(1)(f)); Betrieb und Sicherheit, Logs (V8, Art. 6(1)(f)); Aufbewahrung von Belegen (Art. 6(1)(c)) | 13(1)(c) |
| Berechtigte Interessen | Qualität der KI-Antworten prüfen; Sicherheit und Stabilität des Dienstes | 13(1)(d) |
| Empfänger | **benannt** (WP260: „generally … the named recipients“): Anthropic PBC (KI-Modell), Google Cloud (Hosting, Logs), Neon / Databricks (Datenbank) | 13(1)(e) |
| Drittland | USA (Anthropic, Speicherung). Verarbeitung „in the US, Europe, Asia and Australia“ möglich (Anthropic Privacy Center). Garantie: Standardvertragsklauseln nach Art. 46(2)(c), Hinweis, wo eine Kopie erhältlich ist. Logs am Ort „global“ (Google). | 13(1)(f) |
| Speicherdauer | konkrete Fristen je Datenart (siehe 4). Nicht „solange erforderlich“ (WP260: „not sufficient … to generically state …“) | 13(2)(a) |
| Rechte, Beschwerde | Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch (gegen V6, V8), Datenübertragbarkeit, Beschwerde bei der Aufsicht | 13(2)(b), (d) |
| Pflicht zur Bereitstellung | Für die Bearbeitung nötig sind Kunden-ID und Anliegen. Ohne diese Angaben ist keine Bearbeitung möglich. | 13(2)(e) |
| Automatisierte Entscheidung | **mit Legal klären** (siehe 6). Falls Art. 22: Bestehen, Logik („rationale … or the criteria“, WP251), Tragweite. Falls nicht: als gute Praxis trotzdem (WP251: „good practice to provide the above information“). Logik in einem Satz, z. B. „Eine Doppelbuchung erkennt ein festes Programm, wenn zwei Zahlungen am selben Tag mit gleichem Betrag und gleicher Beschreibung vorliegen“ (`uc4_agent/werkzeuge.py:69-76`). | 13(2)(f) |
| KI-Einsatz und Training | Hinweis, dass Anthropic Eingaben nicht für Training verwendet (Commercial Terms: „may not train models on Customer Content“). DSK OH KI, Nr. 1.9: Anwendungen ohne Trainingsnutzung sind „vorzugswürdig“. | Transparenz (Art. 5(1)(a), 12) |

**Stand UC7: fehlt.** Es gibt keine Datenschutzerklärung und keinen Hinweis am Formular, nur den Demo-Fuß (`app/templates/base.html:42`, `app/templates/anliegen.html:36-41`).

## 3. Drittlandtransfer zu Anthropic

**Ausgangslage** (DATENFLUSS.md, Anbieter):
- Anthropic speichert in den USA und verarbeitet ggf. auch in Asien und Australien.
- DPA mit SCC Modul 2 und 3.
- Das DPF wird in den Anthropic-Quellen nicht genannt.
- Eine EU-Option gibt es nicht. Haiku 4.5 lehnt `inference_geo` ab.

**Prüfweg:**

1. **DPF-Zertifizierung prüfen.** Der Angemessenheitsbeschluss gilt nur für Organisationen auf der „Data Privacy Framework List“ (Art. 1 DPF-Beschluss). Die Liste führt das US-Handelsministerium (https://www.dataprivacyframework.gov/s/participant-search). Ob Anthropic darauf steht: **offen, nicht geprüft.**
   - **Ist Anthropic gelistet:** Art. 45 trägt. Laut EDPB 01/2020, Rn. 19 sind dann „no further steps“ nötig.
   - **Restrisiko:** Das EuG hat das DPF am 3.9.2025 bestätigt (T-553/23). Das Rechtsmittel C-703/25 P ist anhängig, Stand nicht verifiziert.
2. **Sonst SCC (Art. 46(2)(c), Beschluss 2021/914).** Modul 2 (FocusFlow → Anthropic) und Modul 3 (Anthropic → Unterauftragsverarbeiter) sind im Anthropic-DPA enthalten.
3. **Transfer Impact Assessment (TIA).** Klausel 14(d) SCC: Die Parteien dokumentieren die Beurteilung und legen sie der Aufsicht auf Anfrage vor. Die sechs Schritte stehen in EDPB 01/2020.
   - **Erleichterung:** Laut EDPB DPF-Note gelten die US-Garantien aus dem DPF-Verfahren „to all data transferred to the US, regardless of the transfer tool used“. Die Bewertung der Kommission kann in die TIA einfließen.
4. **Ergänzende Maßnahmen** (EDPB 01/2020, Schritt 4):
   - Pseudonymisierung vor dem Modell (DATENMINIMIERUNG.md). Sie nimmt alle direkten Identifikatoren aus der T01-Anfrage.
   - Zahlungen auf ein Zeitfenster begrenzen.
   - Zero Data Retention anfragen. Ob ZDR für ein Pay-as-you-go-Konto erhältlich ist: offen.
5. **Unterauftragsverarbeiter.** Die Liste von Anthropic (trust.anthropic.com) ist noch nicht gelesen (offen aus Schritt 1). Sie gehört zur TIA.

**Auch Google und Neon:**
- Cloud-Logging-Buckets am Ort „global“ und Secret Manager „across multiple regions globally“ können Drittländer berühren. Für Google gelten CDPA und SCC.
- Für Neon / Databricks: Transfergrundlage offen (Databricks-DPA auswerten).

**Mit Legal klären:** Reicht die TIA mit Verweis auf die DPF-Bewertung, wenn Anthropic nicht gelistet ist? Welche ergänzenden Maßnahmen sind verhältnismäßig?

## 4. Löschfristen

Heute löscht der UC7-Code nichts (`app/speicher.py`, kein `DELETE` außer `pruefungen`; Rolle `uc7_app` ohne `DELETE`, `docs/deploy.md:47-48`). Art. 5(1)(e) verlangt eine Begrenzung. Art. 17(3)(b) erlaubt das Aufbewahren für gesetzliche Pflichten.

**Gesetzliche Fristen** (§ 257 Abs. 4 HGB, § 147 Abs. 3 AO, am Original geprüft):
- Buchungsbelege **8 Jahre**, nicht mehr 10.
- Empfangene und abgesandte Handelsbriefe **6 Jahre**.
- Beginn mit Schluss des Kalenderjahres.
- Handelsbriefe sind „nur Schriftstücke, die ein Handelsgeschäft betreffen“ (§ 257 Abs. 2 HGB).

**Vorschlag**, jede Zahl ist eine Annahme und **mit Legal klären**:

| Daten | Ort | Vorschlag | Begründung |
|---|---|---|---|
| Ticket, Agent-Protokoll (`laeufe.text`, `ereignisse`, `ergebnis`), Prüfungen | Neon | 90 Tage nach Abschluss des Falls löschen oder anonymisieren | Rückfragen und Beschwerden; Annahme, keine Primärquelle |
| Ticket und Antwort zu Erstattung oder Kündigung | Neon | 6 Jahre, **falls Handelsbrief** | Ob Support-Korrespondenz Handelsbrief ist: **offen**, keine Primärquelle |
| Erstattungsentscheidung als Buchungsgrundlage | Buchhaltung, nicht Neon | 8 Jahre | § 257 Abs. 4 HGB. Der Beleg gehört ins Buchhaltungssystem, nicht ins Agent-Protokoll. |
| Interne Notiz | Neon | mit dem Fall | – |
| Request-Logs mit IP | Cloud Logging | kürzer als die heutigen 30 Tage, z. B. 7 Tage; regionaler Bucket | Annahme; keine Primärquelle für eine konkrete Frist |
| Eingaben und Ausgaben bei Anthropic | Anthropic | bis 30 Tage (nicht steuerbar), bei Markierung bis 2 Jahre; ZDR prüfen | Anthropic Privacy Center |
| CLI-Transkripte, Laufdateien | Container | nicht schreiben | nicht nötig |
| Link-Codes (Demo) | Neon | 60 Tage nach Ablauf löschen | Annahme |
| Replay | Git, Image | nur synthetisch, dann keine Frist nötig | – |

## 5. Datenschutz-Folgenabschätzung (Art. 35): ja, nach unserer Einschätzung nötig

- **DSK Muss-Liste, Nr. 11** (am Original geprüft): „Einsatz von künstlicher Intelligenz zur Verarbeitung personenbezogener Daten zur Steuerung der Interaktion mit den Betroffenen oder zur Bewertung persönlicher Aspekte der betroffenen Person“. Typisches Einsatzfeld: **„Kundensupport mittels künstlicher Intelligenz“**. Beispiel: „Ein Unternehmen setzt ein System ein, welches mit Kunden durch Konversation interagiert und für deren Beratung personenbezogene Daten durch eine künstliche Intelligenz verarbeitet werden“. Das beschreibt den Agent fast wörtlich.
- **WP248, Kriterien:**
  - „Innovative Nutzung … neuer technologischer … Lösungen“ (LLM): erfüllt.
  - „Automatisierte Entscheidungsfindung mit Rechtswirkung oder ähnlich bedeutsamer Wirkung“: möglich (Kündigung, autonome Ablehnung, Option Auto-Erstattung, siehe 6).
  - Daten zu finanziellen Verhältnissen: teilweise (Zahlungen).
  - Faustregel: „Erfüllt ein Verarbeitungsvorgang zwei dieser Kriterien, muss … in den meisten Fällen“ eine DSFA erfolgen.
- **DSK OH KI, Nr. 2.3:** „Beim Einsatz von KI-Anwendungen wird dies vielfach der Fall sein.“

**Ergebnis:** Die DSFA ist vor dem Go-live durchzuführen (Art. 35(1): „vorab“). Die Inventur liefert Teil (a) von Art. 35(7) (systematische Beschreibung). Diese Prüfung und der Backlog liefern Ansätze für (b) bis (d).

**Mit Legal klären:** Ändert die menschliche Freigabe bei Erstattungen etwas an Nr. 11? Der Wortlaut „Kundensupport mittels KI“ und das Beispiel sprechen dagegen.

## 6. Art. 22 und die UC8-Option „Doppelbuchung automatisch erstatten“

**Die Option:** UC8, `docs/decisions.md`, 2026-10-08, vorgeschlagen, nicht entschieden. Doppelbuchungen bis 10 EUR werden ohne Freigabe erstattet, darüber entscheidet ein Mensch. Die Regel prüft der Code (`uc4_agent/werkzeuge.py:69-76`), der Agent wählt die Zahlung aus.

**Prüfung nach EuGH SCHUFA, Rn. 43:** drei kumulative Voraussetzungen.

| Voraussetzung | Bei der Option | Einschätzung |
|---|---|---|
| „Entscheidung“ (weiter Begriff, Rn. 45-46) | Erstattung ja oder nein | erfüllt |
| „ausschließlich auf einer automatisierten Verarbeitung“ | Agent (LLM) wählt, Code prüft, niemand sieht es vorher. Auch regelbasierte Entscheidungen zählen (WP251: „by technological means without human involvement“). | erfüllt |
| „rechtliche Wirkung“ oder „in ähnlicher Weise erheblich“ | Erstattung = Leistung im Vertrag, wirkt auf die finanziellen Verhältnisse (WP251) | **mit Legal klären** |

**Kern der Frage:** Die Entscheidung ist **ausschließlich begünstigend**. Wer die Voraussetzung nicht erfüllt oder über 10 EUR liegt, kommt zum Menschen.
- Eine Primäraussage, dass begünstigende Entscheidungen nicht unter Art. 22 fallen, gibt es nicht. Weder WP251 noch der EuGH äußern sich dazu.
- **Indiz dagegen:** Der deutsche Gesetzgeber hat für Versicherungen eine ausdrückliche Ausnahme geschaffen, wenn „dem Begehren der betroffenen Person stattgegeben wurde“ (§ 37 Abs. 1 Nr. 1 BDSG). Das spricht dafür, dass ohne eine solche Norm Art. 22 grundsätzlich greift. Für FocusFlow gilt § 37 nicht.

**Wenn Art. 22 greift:**
- **Ausnahme Art. 22(2)(a) (Vertrag):** möglich. Die Notwendigkeit ist aber streng (WP251: „If other effective and less intrusive means … exist, then it would not be ‘necessary’“). Die menschliche Freigabe gibt es ja. Das Argument für die Option wäre Geschwindigkeit, nicht Notwendigkeit. **Mit Legal klären.**
- **Pflichten nach Art. 22(3):** Recht auf Eingreifen einer Person, Darlegung des eigenen Standpunkts, Anfechtung.
- **Informationspflicht nach Art. 13(2)(f):** über die Logik.
- **Art. 22(4):** Es fließen keine besonderen Kategorien ein. Gesundheitsangaben im Freitext dürfen die Entscheidung nicht tragen, die Regel nutzt nur Zahlungsdaten.
- **Keine Scheinbeteiligung** (WP251, DSK OH KI Nr. 1.6: „lediglich formelle Beteiligung … nicht ausreichend“): Ein Mensch, der Auto-Erstattungen nur „abnickt“, nimmt sie nicht aus Art. 22 heraus.

**Zwei Funde, die schon heute ohne die Option bestehen:**

1. **Autonome Ablehnungen.** Fragt ein Kunde nach Geld zurück und die Regel sagt nein, schreibt der Agent die Ablehnung in den Entwurf. Der Kunde sieht sie ohne Mensch, z. B. Monatsabo T15 (`uc4_agent/werkzeuge.py:82-84`, `app/main.py:212-214`). Eine Ablehnung ist **belastend**. Ob die Mitteilung einer feststehenden Regel eine „Entscheidung“ nach Art. 22 ist: **mit Legal klären.** Nach dem weiten Begriff (SCHUFA, Rn. 45-46) ist das nicht ausgeschlossen. Vorsichtiger Weg: Ablehnungen von Geldwünschen immer über die Konsole (BACKLOG B05).
2. **Kündigung durch den Agent** (`uc4_agent/werkzeuge.py:311-328`). WP251 nennt „cancellation of a contract“ als Beispiel für Rechtswirkung. Hier setzt der Agent aber die eigene Kündigungserklärung des Kunden um. **Mit Legal klären,** ob das eine Entscheidung von FocusFlow ist. In jedem Fall sinnvoll: Bestätigung mit Wirksamkeitsdatum und ein Weg zum Menschen (BACKLOG B25).

## 7. Weitere Pflichten aus der Inventur

- **Art. 28 AVV:** DPAs von Anthropic (in den Commercial Terms), Google (CDPA) und Neon / Databricks (Platform Terms, MCSA) ablegen. Prüfen, ob sie Art. 28(3)(a)-(h) abdecken. Bei Modul 2/3 decken die SCC Art. 28(3)-(4) ab (Art. 1(2) SCC-Beschluss).
- **Art. 30 Verzeichnis:** V1-V12 mit Zwecken, Kategorien, Empfängern „einschließlich Empfänger in Drittländern“ und Löschfristen.
- **Art. 15-17 Betroffenenrechte:** Auskunft und Löschung je Kunde über alle Tabellen. Heute gibt es keine Funktion dafür. Die Daten liegen in JSON-Spalten verteilt (`laeufe.ereignisse`).
- **Art. 25, 32:** Konto aus dem Login statt Auswahlliste (`app/templates/anliegen.html:26`). Laufdateien und CLI-Transkripte nicht schreiben.

## Mit Legal klären

1. Ist ein LLM für die Ticketbearbeitung „erforderlich“ nach Art. 6(1)(b), oder braucht es Art. 6(1)(f)?
2. Ist Anthropic DPF-zertifiziert? Reicht sonst die TIA mit Verweis auf die DPF-Bewertung?
3. Ist Support-Korrespondenz zu Erstattung oder Kündigung ein Handelsbrief (6 Jahre)?
4. Konkrete Löschfristen (90 Tage Protokoll, 7 Tage IP-Logs sind Annahmen).
5. Art. 22: Fällt eine ausschließlich begünstigende Auto-Erstattung darunter? Trägt Art. 22(2)(a)?
6. Art. 22: Sind autonome Ablehnungen und die vom Agent ausgeführte Kündigung „Entscheidungen“?
7. DSFA: Ändert die menschliche Freigabe etwas an DSK Nr. 11? (Die Vorlage geht von nein aus.)
