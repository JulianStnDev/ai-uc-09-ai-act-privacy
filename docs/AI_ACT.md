# AI-Act-Einstufung des UC7-Support-Agents

Stand 2026-10-08. **Keine Rechtsberatung.** Das ist eine Einschätzung aus Gesetzestext und Kommissionsleitlinien als Grundlage für das Gespräch mit Legal. Wo die Auslegung unklar ist, steht **„mit Legal klären“**, entschieden wird dort nichts.

Code-Belege beziehen sich auf `ai-uc-07-deployment`, Commit `75c5ea3`. Szenario wie in [DATENFLUSS.md](DATENFLUSS.md): Ab morgen gehen echte Kundentickets hinein.

## Quellen

| Kürzel | Dokument | Fundstelle |
|---|---|---|
| KI-VO | Verordnung (EU) 2024/1689, CELEX 32024R1689 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689 |
| Omnibus | Verordnung (EU) 2026/1744 vom 8.7.2026 (Digital Omnibus on AI), ABl. L 2026/1744 vom 24.7.2026, CELEX 32026R1744 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202601744 |
| LL Verbote | Leitlinien der Kommission zu verbotenen Praktiken, C(2025) 5052 final, 29.7.2025 | https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF |
| LL Definition | Leitlinien der Kommission zur Definition eines KI-Systems, C(2025) 5053 final, 29.7.2025 | https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-01/guide-definition_en.pdf |
| LL Art. 50 | Leitlinien der Kommission zu den Transparenzpflichten nach Art. 50, C(2026) 5054 final, 20.7.2026 | https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf |
| Entwurf LL Hochrisiko | Entwurf der Leitlinien zu Art. 6, 19.5.2026, **nicht final** | https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems; Service Desk: https://ai-act-service-desk.ec.europa.eu/en/essential-services |
| Q&A KI-Kompetenz | Kommission, AI Literacy Q&A, aktualisiert 27.7.2026 | https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers |

Selbst in EUR-Lex geprüft: Titel, Datum und Amtsblatt des Omnibus, Inkrafttreten „on the third day following that of its publication“ (24.7.2026 + 3 = **27.7.2026**), neuer Art. 4, neue Fristen für Hochrisiko (2.12.2027 / 2.8.2028) und Art. 111(4). Die übrigen Zitate stammen aus Recherche-Abrufen derselben Quellen und sollten vor einer Übernahme am Original gegengelesen werden.

## Das System in einem Absatz

Der Agent bekommt ein Kundenticket und schlägt das Konto und die Zahlungen des Absenders nach. Er liest die Hilfeartikel. Er kann eine Erstattung **empfehlen** (ein Mensch entscheidet), ein Web-Abo auf ausdrücklichen Wunsch **selbst kündigen** und an einen Menschen übergeben. Zum Schluss schreibt er einen Antwortentwurf (`uc4_agent/agent.py:84-102`, `uc4_agent/werkzeuge.py:300-367`). Ohne Empfehlung und ohne Geldzusage sieht der Kunde den Entwurf **direkt** (`app/main.py:212-214`). Nach einer Entscheidung formuliert Haiku die endgültige Antwort (`app/main.py:168-184`). Gebaut auf Claude (Anthropic, Modell mit allgemeinem Verwendungszweck).

## 1. Ist das ein KI-System?

**Ja.** Art. 3(1) KI-VO: ein maschinengestütztes System, das „infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions“. Der Agent erzeugt Inhalte (Entwürfe), Empfehlungen (Erstattung) und Entscheidungen (Kündigung, Übergabe) aus dem Ticket. Die LL Definition sind nicht bindend und ändern daran nichts.

## 2. Rolle von FocusFlow: Anbieter und Betreiber

**Beides.**

- **Anbieter (Provider), Art. 3(3):** wer „develops an AI system … and places it on the market or puts the AI system into service under its own name or trademark, whether for payment or free of charge“.
- **Inbetriebnahme, Art. 3(11):** „the supply of an AI system for first use directly to the deployer or **for own use** in the Union for its intended purpose“.
- **Betreiber (Deployer), Art. 3(4):** wer ein KI-System „under its authority“ verwendet.
- **Die Kommission sagt es für genau diesen Fall:** LL Art. 50, Rn. 11: „a company … that has developed an interactive AI system (e.g. chatbot) in-house and puts it into service in the Union for its own use and under its name or trademark“ ist Anbieter. Rn. 15: „it will qualify as both a provider and a deployer“. Ebenso LL Verbote, Rn. 13: Art. 3(11) erfasst „in-house development and deployment“.
- **FocusFlow entwickelt das System:** System-Prompt, Werkzeuge, Konto-Bindung, Freigabe-Logik (`uc4_agent/agent.py:185-210`, `uc4_agent/werkzeuge.py`, `app/`). Das Modell kommt von Anthropic. **Anthropic ist Anbieter des KI-Modells mit allgemeinem Verwendungszweck** (Kapitel V KI-VO). Diese Pflichten liegen bei Anthropic, nicht bei FocusFlow.

## 3. Verbotene Praktiken (Art. 5): keine einschlägig

| Art. 5(1) | Inhalt | Beim Agent |
|---|---|---|
| (a) | manipulative oder täuschende Techniken mit erheblichem Schaden | nein. Siehe Grenze unten. |
| (b) | Ausnutzung von Schwächen (Alter, Behinderung, soziale oder wirtschaftliche Lage) | nein |
| (ba), (bb) | neu durch den Omnibus, ab 2.12.2026: nicht einvernehmliche intime Darstellungen, Missbrauchsdarstellungen von Kindern | nein, der Agent erzeugt nur Text |
| (c) | Social Scoring | nein |
| (d) | Straftatenprognose allein aus Profiling | nein |
| (e) | ungezieltes Auslesen von Gesichtsbildern | nein |
| (f) | Emotionserkennung am Arbeitsplatz und in Bildung | nein |
| (g) | biometrische Kategorisierung nach sensiblen Merkmalen | nein |
| (h) | biometrische Echtzeit-Fernidentifizierung zur Strafverfolgung | nein |

**Grenze:** Nach LL Verbote, Rn. 127-128 gilt (a) nicht für „lawful persuasion practices“ innerhalb von Transparenz und Autonomie. Würde der Agent künftig Kündigungen mit Druck oder Täuschung abwenden sollen („Halteangebote“), ist (a)/(b) neu zu prüfen, zusammen mit dem Lauterkeitsrecht (RL 2005/29/EG). Heute kündigt er auf Wunsch, ohne Gegenangebot (`uc4_agent/agent.py:89`).

## 4. Hohes Risiko (Art. 6): nein

**Art. 6(1), Produkte nach Anhang I:** Der Agent ist weder Sicherheitsbauteil noch Produkt nach Anhang I. Der Omnibus stellt in Art. 6(1a) zusätzlich klar, dass Funktionen „solely used for non-safety related aspects of user assistance … service efficiency“ keine Sicherheitsbauteile sind.

**Art. 6(2), Anhang III:** Kundenservice, Erstattungen und Abo-Kündigungen stehen in keiner Nummer. Die Bereiche einzeln:

| Anhang III | Bereich | Beim Agent |
|---|---|---|
| 1 | Biometrie (inkl. Emotionserkennung) | nein, nur Text |
| 2 | kritische Infrastruktur | nein |
| 3 | Bildung | nein |
| 4 | Beschäftigung, Personalmanagement | nein. Die Konsole zeigt eine Bestätigungsquote über alle Entscheidungen, nicht je Mitarbeiter (`app/speicher.py:370-375`). |
| 5(a) | Zugang zu öffentlichen Leistungen, durch oder für Behörden | nein, privates Unternehmen |
| 5(b) | Kreditwürdigkeit, Kredit-Score | nein. Zahlungen dienen nur der Erstattungsregel (`uc4_agent/werkzeuge.py:64-93`). Der Entwurf der LL Hochrisiko nennt ausdrücklich „AI systems intended for customer support related to the assessment of their creditworthiness should not be classified as high-risk under point 5(b)“ (Service Desk, Entwurf). |
| 5(c) | Risiko und Preis bei Lebens- und Krankenversicherung | nein |
| 5(d) | Notrufe | nein |
| 6-8 | Strafverfolgung, Migration, Justiz, Wahlen | nein |

Weil das System unter keine Nummer von Anhang III fällt, braucht es **keine Ausnahmeprüfung nach Art. 6(3)**. Damit entfallen auch die Dokumentation nach Art. 6(4) und die Registrierung nach Art. 49(2). Die endgültigen Leitlinien der Kommission nach Art. 6(5) gibt es noch nicht, nur den Entwurf vom 19.5.2026.

### Wann es hochriskant würde

| Änderung am Einsatz | Anhang III | Folge |
|---|---|---|
| Der Agent bewertet Zahlungsverhalten, um über Ratenzahlung, „Kauf auf Rechnung“ oder Kreditrahmen zu entscheiden | 5(b) Kreditwürdigkeit | Hochrisiko. Ausnahme in 5(b) nur für Betrugserkennung. |
| Die Konsole wertet Entscheidungen **je Mitarbeiter** aus (Bestätigungsquote, Tempo) oder verteilt Tickets nach Verhalten | 4(b) Leistungsbewertung, Aufgabenzuteilung | Hochrisiko. FocusFlow wäre dann auch Betreiber gegenüber eigenen Beschäftigten. |
| Sprachsupport mit Stimmungsanalyse | 1(c) Emotionserkennung (biometrisch) | Hochrisiko, zusätzlich Art. 50(3). Textbasierte Stimmung ist nicht biometrisch. |
| Einsatz für eine Krankenkasse oder Lebensversicherung (Tarif, Risiko) | 5(c) | Hochrisiko |
| Einsatz im Auftrag einer Behörde für Leistungsansprüche | 5(a) | Hochrisiko |

Für jede dieser Änderungen gilt Art. 25(1)(c): Wer den Zweck so ändert, dass das System hochriskant wird, ist Anbieter eines Hochrisikosystems. Die Pflichten dafür gelten nach dem Omnibus ab dem **2.12.2027** (Anhang III), vorher nicht.

## 5. Transparenz (Art. 50): betroffen, und zwar jetzt

### Art. 50(1): Hinweis, dass man mit KI interagiert. Gilt, seit 2.8.2026.

- **Wortlaut:** Anbieter sorgen dafür, dass Personen „informed that they are interacting with an AI system, unless this is obvious“.
- **Kundensupport ist genannt:** LL Art. 50 zählt „chatbots/conversational agents in various contexts (e.g. public service, customer support, complaints management …)“ dazu. Die Ausnahme „obvious“ greift ausdrücklich nicht bei „AI chatbots embedded in online platforms or assistance support tools (helpdesks) whereby users directly interact and receive AI outputs … they may perceive as human-generated“.
- **Prüfmöglichkeit reicht nicht:** „the mere possibility for humans to intervene or review the AI system’s outputs should not be used to circumvent the application“ (LL Art. 50).
- **Zeitpunkt:** „at the latest at the time of the first interaction“ (Art. 50(5)), also im Ticket-Formular.
- **Ab wann:** Art. 50(1) gilt seit dem allgemeinen Geltungsbeginn 2.8.2026 (Art. 113). LL Art. 50, Rn. 153: Die Disclosure „must be ensured as of 2 August 2026“. Die Übergangsfrist bis 2.12.2026 betrifft nur Art. 50(2).

**Stand UC7: fehlt, und eine Aussage ist irreführend.**

| Kundensicht | Wer schreibt | Was der Kunde liest | Beleg |
|---|---|---|---|
| Entwurf ohne Empfehlung | Agent, **niemand prüft** | „Draft. A human checks it before it is sent.“ | `app/templates/_entwurf.html:6`, `app/main.py:212-214` |
| Antwort nach Entscheidung | Haiku, nach menschlicher Entscheidung über den Betrag | „Decided by support … This reply is based on the decision“. Dass der Text von einer KI stammt, steht nicht da. | `app/templates/_entwurf.html:22-27` |
| Zwischenbescheid | feste Vorlage, keine KI | unkritisch | `app/antwort.py:32-38` |
| Absender aller Nachrichten | – | „FocusFlow Support“ | `app/templates/_entwurf.html:4` |

Für die Demo gilt die „obvious“-Ausnahme: Die Startseite sagt „An AI agent in customer support“ (`app/templates/start.html:6`), der Fuß nennt das Modell (`app/templates/base.html:42`). Im Kundenportal eines echten Kunden gäbe es weder Startseite noch Fuß.

**Mit Legal klären:** Ist ein asynchrones Ticketportal (Anfrage rein, Antwort raus) eine „Interaktion“ im Sinne von Art. 50(1)? Die Leitlinien nennen „complaints management“ und Helpdesks, das spricht dafür. Die Vorlage plant deshalb den Hinweis ein.

### Art. 50(2): maschinenlesbare Kennzeichnung von KI-Text. Gilt für UC7 ohne Übergangsfrist.

- **Wortlaut:** Anbieter von KI-Systemen, die „synthetic … text content“ erzeugen, sorgen dafür, dass die Ausgaben „marked in a machine-readable format and detectable as artificially generated“ sind.
- **Übergangsfrist nur für ältere Systeme:** Neuer Art. 111(4) (Omnibus): Systeme, die vor dem 2.8.2026 in Verkehr gebracht wurden, müssen das bis 2.12.2026 umsetzen. UC7 ging am 28.9.2026 online, ein echter Go-live käme noch später. **Die Übergangsfrist greift also nicht.**
- **Stütze auf den Modellanbieter erlaubt:** Laut LL Art. 50 dürfen Anbieter „rely on the marking solution implemented by an upstream model provider“. Ob Anthropic API-Text markiert: **offen**, nicht in einer Anthropic-Quelle gefunden.
- **Mit Legal klären:**
  - Wie wird eine kurze Support-Antwort in Portal oder E-Mail sinnvoll maschinenlesbar markiert (z. B. Metadaten im HTML bzw. E-Mail-Header)?
  - Greift die Ausnahme „assistive function for standard editing“ für die Haiku-Antwort nach einer Entscheidung? Eher nicht, Haiku formuliert den ganzen Text neu.
  - Orientierung: Verhaltenskodex zu KI-generierten Inhalten, Endfassung 10.6.2026 (https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content).

### Art. 50(3) und (4): nicht einschlägig

- **(3):** Es gibt keine Emotionserkennung und keine biometrische Kategorisierung.
- **(4):** Deepfakes erzeugt der Agent nicht. Texte, die „published with the purpose of informing the public on matters of public interest“ sind, auch nicht. LL Art. 50 nennen „private, interpersonal correspondence (for professional purposes)“ als nicht veröffentlicht.

## 6. KI-Kompetenz (Art. 4): gilt, in der Fassung des Omnibus

- **Neuer Art. 4(1):** „Providers and deployers of AI systems shall take measures to support the development of AI literacy of their staff and other persons dealing with the operation and use of AI systems on their behalf … This obligation does not require providers or deployers to guarantee any specific level of AI literacy of any individual.“ In EUR-Lex geprüft.
- **Früher:** „ensure, to their best extent, a sufficient level“. Das „ausreichende Niveau“ ist weggefallen, die **Pflicht zu Maßnahmen bleibt**.
- **Neuer Art. 4(2):** Kommission und Mitgliedstaaten unterstützen, besonders KMU.
- **Aufsicht:** Laut Q&A der Kommission überwachen die nationalen Marktüberwachungsbehörden ab 2.8.2026. Die Pflicht selbst gilt seit 2.2.2025 (Kapitel I).

**Für FocusFlow heißt das:**
- Die Mitarbeiter in der Konsole kennen die Grenzen des Agents: Er empfiehlt nur, kündigt selbst und kann Ursachen erfinden. Sie kennen den Automation Bias.
- Die Entwickler kennen die Konfiguration und ihre Grenzen (siehe SDK-Fund in DATENFLUSS.md).
- **Stand UC7: teilweise.** Die Konsole zeigt Regelprüfung und Warnungen gegen Automation Bias (`app/main.py:594-610`, aus UC6). Schulung und Nachweis fehlen. Ein Nachweis ist nicht vorgeschrieben, aber nützlich.

## 7. Geltungsdaten

| Was | Ursprünglich (Art. 113 KI-VO) | Nach dem Omnibus | Für den Agent |
|---|---|---|---|
| Kapitel I, II (Art. 4, Art. 5) | 2.2.2025 | unverändert; Art. 4 neu gefasst | gilt |
| neue Verbote Art. 5(1)(ba), (bb) | – | 2.12.2026 | nicht einschlägig |
| Kapitel V (Modelle mit allgemeinem Verwendungszweck) u. a. | 2.8.2025 | unverändert | Pflichten von Anthropic |
| Allgemeiner Geltungsbeginn, darunter Art. 50 | 2.8.2026 | unverändert | **Art. 50(1) gilt seit 2.8.2026** |
| Art. 50(2) für Systeme, die **vor** dem 2.8.2026 in Verkehr gebracht wurden | 2.8.2026 | 2.12.2026 (Art. 111(4)) | greift nicht, UC7 ist jünger |
| Hochrisiko nach Anhang III (Kap. III Abschn. 1-3) | 2.8.2026 | **2.12.2027** | nur bei Zweckänderung, siehe 4 |
| Hochrisiko nach Anhang I (Art. 6(1)) | 2.8.2027 | **2.8.2028** | nein |
| Omnibus in Kraft | – | **27.7.2026** (ABl. 24.7.2026, Art. 3 Omnibus) | – |

## 8. Ergebnis

**Begrenztes Risiko mit Transparenzpflichten.** FocusFlow ist Anbieter und Betreiber. Keine Verbote, kein Hochrisiko. Pflichten heute:

1. **Art. 50(1):** KI-Hinweis spätestens bei der ersten Interaktion.
2. **Art. 50(2):** maschinenlesbare Kennzeichnung der KI-Texte.
3. **Art. 4:** Maßnahmen zur KI-Kompetenz.

Die Umsetzung steht in [BACKLOG.md](BACKLOG.md).

## Mit Legal klären

1. Ist ein asynchrones Ticketportal eine Interaktion nach Art. 50(1)? (Die Vorlage geht von ja aus.)
2. Wie wird Art. 50(2) bei kurzen Support-Texten umgesetzt? Markiert Anthropic? Greift die Ausnahme „standard editing“ für die Haiku-Antwort?
3. Ist UC7 als öffentliche Portfolio-Demo bereits „in Betrieb genommen“, mit Art. 50(2) seit 28.9.2026? Oder erst der echte Go-live?
4. Einordnung, sobald die endgültigen Leitlinien nach Art. 6(5) erscheinen. Bisher gibt es nur den Entwurf.
