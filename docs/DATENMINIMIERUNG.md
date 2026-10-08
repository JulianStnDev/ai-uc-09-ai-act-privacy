# Datenminimierung vor dem Modell

Stand 2026-10-08. Nur Analyse, am UC7-Code ist nichts geändert. Zeilenangaben beziehen sich auf `ai-uc-07-deployment` (Commit `75c5ea3`). Feldkürzel wie in [DATENFLUSS.md](DATENFLUSS.md).

## Was der Agent tun muss

Laut System-Prompt v3 (`uc4_agent/agent.py:84-102`) hat der Agent fünf Aufgaben:

1. Den Absender finden.
2. Regeln aus der Hilfe holen.
3. Vor einer Erstattung die Zahlungen prüfen.
4. Empfehlen, kündigen oder übergeben.
5. Einen deutschen Entwurf „per Du“ schreiben.

Die endgültige Antwort schreibt Haiku „mit Anrede mit Vornamen“ (`app/antwort.py:24`). Wer der Absender ist, weiß der Code schon vor dem Modell: `absender_id` kommt aus der Sitzung, und die Konto-Bindung prüft jeden Werkzeugaufruf dagegen (`uc4_agent/werkzeuge.py:143`, `:212-234`).

## Feld für Feld

| Feld | Wofür das Modell es nutzt | Nötig? | Vor dem Modell ersetzbar durch | Mögliche Folge für die Qualität |
|---|---|---|---|---|
| **E-Mail im Ticketkopf** (`Von: …`, `uc4_agent/agent.py:182`) | Nur als Suchschlüssel für `kunde_nachschlagen` | nein | `Kunden-ID: K001` | Prompt v3, Schritt 1 und 5 sprechen von der „Absender-Adresse“ und müssten umformuliert werden. Der Hinweis-Pfad „E-Mail statt Kunden-ID“ (`uc4_agent/werkzeuge.py:203-210`, in v3 viermal nötig) fällt weg. Das ist eher ein Gewinn. |
| **E-Mail im Werkzeug-Ergebnis** (`kunde_nachschlagen`) | Abgleich mit Adressen im Freitext (T14) | nein | weglassen oder Token `E-Mail-1` | Neutral, solange Adressen im Freitext **konsistent** ersetzt werden (siehe Freitext). |
| **Name** im Werkzeug-Ergebnis | Anrede im Entwurf; Namenssuche bei `kunde_nachschlagen` | nein | Platzhalter `{vorname}`, den der Code nach dem Modell einsetzt | Das Modell muss den Platzhalter unverändert lassen. Risiko: „Hallo Kunde“ oder ein entstellter Platzhalter, prüfbar per Regel ohne LLM. Die Namenssuche entfällt. Bei Namensgleichen (K006/K007 Felix Braun, T07) schützt die Konto-Bindung ohnehin. |
| **Vorname in Entwurf und Antwort** | Anrede | nein | `{vorname}` | wie oben. Judge und Neuschreiben sehen dann ebenfalls den Platzhalter, eingesetzt wird erst vor der Anzeige. |
| **Kunden-ID** | Schlüssel für alle Werkzeuge | ja | ist schon das Pseudonym | Keine. Achtung: Pseudonymisierte Daten bleiben personenbezogen (Art. 4 Nr. 5, ErwG 26 DSGVO), solange jemand die Zuordnung hat. Der DPA mit Anthropic bleibt nötig. |
| **Kontodaten** (Login, Plattform, Abo-Stufe, Anbieter, Status, Periode) | Kündigen nur bei Stripe, Store-Hinweis, Fristen, Login-Probleme (T07) | ja | – | Ohne sie fallen Store-Fälle (T06, T10, T11) und Kündigungen falsch aus. |
| **Kunde seit** | Keine Regel nutzt das Feld | nein | weglassen | Keine erwartet, nicht gemessen. |
| **Zahlungen** (Datum, Betrag, Beschreibung, Anbieter) | Erstattungsregel: Frist, Tarif, Doppelbuchung (`uc4_agent/werkzeuge.py:64-93`) | ja | – | Kürzen statt ersetzen: `zahlungen_ansehen` liefert die ganze Historie (`uc4_agent/werkzeuge.py:272-275`). Ein Zeitfenster, z. B. 13 Monate, deckt Jahresabo und Doppelbuchung ab. Folge: Ältere Zahlungen fehlen, wenn ein Kunde nach ihnen fragt. Dann muss der Fall übergeben werden. |
| **Zahlungs-IDs** | Empfehlung braucht die konkrete Zahlung | ja | sind interne IDs | Keine. |
| **Freitext** | Das Anliegen selbst | ja | nur teilweise: erkennbare Muster (E-Mail, Telefon, IBAN, Kartennummer, Namen aus dem eigenen Kundenstamm) durch **konsistente** Token ersetzen | Das größte Restrisiko. Inhalt ist frei: Unterschriften mit vollem Namen, Adressen, Gesundheitsangaben („war im Krankenhaus“). Ersetzt man eine fremde Adresse nur im Kopf, aber nicht im Text, kann der Agent bei T14 nicht mehr erkennen, dass ein anderes Konto gemeint ist. Mit einem konsistenten Token (`E-Mail-2` ≠ Absender) bleibt das erkennbar. Musterersetzung übersieht freie Formulierungen. |
| **Begründung für den Kunden** (Konsole) | Geht in die Antwort | ja | – | Schreibt ein Mensch. Ein Hinweis in der Konsole („keine Namen, keine Gesundheitsangaben“) wäre organisatorisch. |
| **Interne Notiz** | – | geht schon heute an kein Modell (`app/speicher.py:272-276`) | – | – |

## Was das für T01 heißt

Gezählt in [evals/t01_anfragen.md](../evals/t01_anfragen.md), letzter Agent-Turn (64 markierte Fundstellen):

| Gruppe | Fundstellen | Mit Pseudonymisierung |
|---|---|---|
| E-Mail (3), Name und Vorname (5) | 8 | entfallen |
| Login-Methode (1), Kunde seit (1, als Datum gezählt) | 2 | entfallen |
| Kunden-ID (12), Zahlungs-IDs (15) | 27 | bleiben, sind interne Pseudonyme |
| Beträge (12), Daten (14 ohne „Kunde seit“), Abo-Stufe (1) | 27 | bleiben, sind der Inhalt des Falls |
| Freitext | ganzer Block | bleibt; T01 enthält keinen Namen und keine Adresse |

Bei T01 kommt danach **kein direkter Identifikator mehr bei Anthropic an**. Was bleibt, ist ein pseudonymer Fall: K001 mit fünf Zahlungen und einem Ticket. Wer die Zuordnung K001 → Anna Berger nicht hat, kann ihn keiner Person zuordnen, solange der Freitext nichts verrät.

## Wie oft der Freitext etwas verrät

Im Goldset (15 Tickets, `uc4_agent/evals/aufgaben.json`) enthält nur **T14** eine E-Mail-Adresse im Text. In keinem Ticket steht ein Name. Echte E-Mails haben fast immer eine Grußzeile mit Namen. Das Goldset bildet das nicht ab. Wie oft echte Tickets Namen, Adressen, Telefonnummern oder Gesundheitsangaben enthalten: **unbekannt**. Messbar erst an echten oder realistisch nachgebauten Tickets.

## Wirkung auf Judge und Neuschreiben

- **Judge** (`app/pruefung.py:170-174`): Er prüft, ob Aussagen durch die Trajektorie gedeckt sind. Das bleibt gleich, solange Trajektorie und Text **mit denselben** Platzhaltern kommen. Der Judge muss also den Text vor dem Einsetzen des Namens sehen.
- **Haiku-Neuschreiben** (`app/antwort.py:17-25`): Die Regel „Anrede mit Vornamen“ wird zu „Anrede mit `{vorname}`“. Das Einsetzen übernimmt der Code, wie heute schon in der Vorlage (`app/antwort.py:28-29`).

## Was sich nicht durch eine ID ersetzen lässt

Beträge, Daten, Tarife und das Anliegen selbst. Das ist der Gegenstand der Aufgabe. Pseudonymisierung senkt also das Risiko, dass ein Datensatz bei Anthropic einer Person zugeordnet wird. Sie ändert aber nichts daran, dass personenbezogene Daten in die USA gehen. Für die Rechtsgrundlage des Transfers bleibt es bei SCC (siehe [DATENFLUSS.md](DATENFLUSS.md), Anbieter).

## Wie man die Qualitätsfolgen messen würde (nicht ausgeführt)

> Ersetzt durch den Messplan im [Backlog, Ausblick B13](BACKLOG.md#ausblick-b13-pseudonymisierung-vor-dem-modell): frische Kontrolle auf `main` gegen den Branch, Judge j2, ca. 5,20 USD. Die Schätzung unten (nur der Branch, Judge u2) bleibt als erster Stand stehen.

Goldset mit pseudonymisiertem Prompt neu laufen lassen, 15 Tickets × 3 Läufe, Judge u2 auf allen Entwürfen.

Schätzung nach der Regel „erst schätzen, dann laufen“:

| Posten | Rechnung | Betrag |
|---|---|---|
| Agent | 45 × 0,0341 USD (UC7, 34,1 USD je 1000 Anfragen) | 1,53 USD |
| Judge | 45 × 0,024 USD (UC7, T01-Urteil 0,023838 USD, gerundet) | 1,08 USD |
| **Summe** | | **rund 2,61 USD** |

Vergleich gegen UC6 „nachher“. Zusätzlich eine Regel ohne LLM: Platzhalter `{vorname}` kommt genau einmal vor und ist unverändert.
