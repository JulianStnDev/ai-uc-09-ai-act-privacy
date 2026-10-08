🇩🇪 [Deutsche Version](README_DE.md)

# UC9: AI Act & Data Protection for the Support Agent

> A decision and obligations memo, not product code. The question: what would have to hold if real customer tickets went into the UC7 support agent tomorrow? Step 1 is a data flow inventory taken from the code, step 2 the AI Act classification, step 3 the GDPR review and an obligations backlog. Not legal advice. Every claim is backed by a file and line or by a vendor primary source. Cost: 0 USD, no API calls.

## Problem
The UC7 agent runs on Cloud Run and handles support tickets. In the demo the customers are fictional. With real customers, names, e-mail addresses, payments and free text would pass through eleven stations, three of them at Anthropic. Before the system can be classified under the AI Act or GDPR obligations can be set up, one thing has to be clear: which personal data ends up where, for how long, and on what contractual basis.

## Step 1: Data Flow Inventory

**5 of 11 stations without an EU location commitment.**
The app and the database run in Frankfurt (Cloud Run `europe-west3`, Neon `aws-eu-central-1`). Anthropic stores API data in the US and offers no EU option. Haiku 4.5, which runs the agent and the rewrite, cannot be pinned to a region at all. Cloud Logging keeps request logs with IP address, user agent and full URL in a bucket at location "global". The recorded T01 case is a complete customer record, and it sits in the public GitHub repo.

| Station | Personal data | Location | Retention |
|---|---|---|---|
| Browser | customer ID, free text; the pages show everything | user's device | cookies 7 / 60 days |
| Cloud Run | everything, in memory and in run files | Frankfurt | until the instance ends |
| Neon | everything except IP | Frankfurt | **no deletion in the code** |
| Anthropic agent, judge, rewrite | e-mail, name, account, payments, free text, draft | stored in the US | up to 30 days, up to 2 years if flagged |
| Cloud Logging | IP, user agent, URL with run ID and link code | "global" | 30 days |
| Console, operations page | name, e-mail, ticket, draft, internal note | from Neon | as Neon |
| Replay | the full T01 case | public Git repo, every visitor | unlimited |
| Personal links | link code, linked to the visitor's free text | Neon, logs, cookie | row stays |

The full table with code references, vendor sources and open points is in [docs/DATENFLUSS.md](docs/DATENFLUSS.md). The three requests to Anthropic for T01 are reproduced word for word, with every personal field marked: [evals/t01_anfragen.md](evals/t01_anfragen.md).

**Pseudonymisation would remove all 8 direct identifiers from the T01 agent request.**
The agent needs the customer ID, the account data and the payments. It does not need the e-mail address, because the code already knows the sender. It does not need the name either: the name is only used for the greeting, and a placeholder can do that job. Amounts, dates and the free text itself cannot be replaced. In the gold set only T14 has an e-mail address in the text, and no ticket has a name. Real e-mails usually end with a signature, which the gold set does not cover. This is analysis only, nothing was changed: [docs/DATENMINIMIERUNG.md](docs/DATENMINIMIERUNG.md).

## Step 2: AI Act Classification

**Limited risk: no prohibited practice, not high-risk, Art. 50 applies since 2 Aug 2026.**
FocusFlow builds the agent and uses it itself, so it is **provider and deployer** at the same time (Art. 3(3), 3(11); the Commission's Art. 50 guidelines name this exact case). Anthropic is the provider of the general-purpose model. None of the Art. 5 prohibitions applies. Customer service, refunds and cancellations are not listed in Annex III. It would become high-risk if the agent scored payment behaviour for credit decisions (5(b)), evaluated support staff individually (4(b)) or analysed emotions in voice support (1(c)).

What applies now:
- **Art. 50(1):** customers must be told they are dealing with AI. The Commission's guidelines name helpdesk chatbots explicitly. Today the portal even says "A human checks it before it is sent", but for drafts without a recommendation no human does.
- **Art. 50(2):** machine-readable marking of AI text. The grace period until 2 Dec 2026 only covers systems placed on the market before 2 Aug 2026.
- **Art. 4:** AI literacy measures, as amended by the Digital Omnibus (Regulation (EU) 2026/1744, in force since 27 Jul 2026, checked in EUR-Lex): no "sufficient level" any more, but the obligation stays. High-risk obligations moved to 2 Dec 2027 (Annex III) and 2 Aug 2028 (Annex I).

Details: [docs/AI_ACT.md](docs/AI_ACT.md).

## Step 3: GDPR Review and Obligations Backlog

- **Legal basis:** ticket handling Art. 6(1)(b), judge sampling and logs Art. 6(1)(f). Whether using an LLM is "necessary" for (b) is marked "clarify with Legal".
- **DPIA needed:** the German DSK list names "Kundensupport mittels künstlicher Intelligenz" (item 11).
- **Transfer to Anthropic:** SCC module 2/3 plus a transfer impact assessment, unless Anthropic is DPF-certified (not checked).
- **Retention:** the code deletes nothing today. Accounting records 8 years, business letters 6 years (HGB §257, checked); everything else needs a set period.
- **Art. 22:** the automatic refund option from UC8 is a decision based solely on automated processing; whether a purely favourable decision is covered is open. Two findings exist even without that option: refusals of refund requests reach the customer without a human, and the agent executes cancellations itself.

**28 obligations, 19 before go-live, 0 fulfilled today.** Every entry has a requirement in product language, the legal basis, today's status in UC7 with file and line, effort and priority: [docs/BACKLOG.md](docs/BACKLOG.md). Two of them come with the exact customer-facing text (ticket form notice, label on an autonomous reply).

## Findings That Were Not in the Code
- **The Agent SDK adds context of its own.** In a local run, the bundled CLI put two things into the support agent's request: the developer's auto-memory and the machine's user path. This happened even with `setting_sources=[]`. According to Anthropic, the CLI also writes plaintext transcripts (kept 30 days by default) and creates session titles with an extra model call. Whether the same happens in the container is open.
- **Link codes end up in the logs.** The code of a personal link is part of the URL, so Cloud Run logs it together with the IP address (4 entries in the last 30 days).
- **Anthropic's sources contradict each other on retention.** The Privacy Center says inputs and outputs are deleted "within 30 days". The API docs say content is "not retained by default". The plan assumes up to 30 days.

## Vendors (primary sources, 2026-10-08)

| | DPA | Role | Transfer basis | Location |
|---|---|---|---|---|
| Anthropic | yes, part of the Commercial Terms | processor | SCC module 2/3; DPF not mentioned | stored in the US, inference "global" or "us" |
| Google Cloud | yes, CDPA | processor | SCC unless an alternative solution applies; Google LLC DPF-certified | selected region for listed services; logs and secrets "global" |
| Neon (Databricks) | yes, via platform terms | not stated explicitly on neon.com | open | one region per project; backups 30 days |

## Cost & Latency
- Cost per 1000 requests: does not apply to this step (0 USD, no API calls). The agent being analysed costs 34.1 USD per 1000 requests (UC7).
- p95 latency: 39.7 s per agent run (UC7, unchanged).
- Quality metric: 5 of 11 stations without an EU location commitment. The last T01 agent request has 64 personal-data hits, 8 of them direct identifiers. Obligations backlog: 28 entries, 19 before go-live, 0 fulfilled today.

## Next Steps
- Take the "clarify with Legal" points to Legal (listed at the end of AI_ACT.md and DSGVO.md).
- Close the open research points: Anthropic's DPF status and subprocessors, the retention contradiction, the Neon DPA, the SDK in the container.
- Build the go-live entries of the backlog, starting with the AI notices (B01-B03) and the SDK settings (B20).

Details (German): [AI Act](docs/AI_ACT.md) · [GDPR](docs/DSGVO.md) · [Backlog](docs/BACKLOG.md) · [Data flow](docs/DATENFLUSS.md) · [Data minimisation](docs/DATENMINIMIERUNG.md) · [T01 requests](evals/t01_anfragen.md) · [Decisions](docs/decisions.md)
