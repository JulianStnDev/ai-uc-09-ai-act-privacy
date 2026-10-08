🇩🇪 [Deutsche Version](README_DE.md)

# UC9: AI Act & Data Protection for the Support Agent

> A decision and obligations memo, not product code. The question: what would have to hold if real customer tickets went into the UC7 support agent tomorrow? Step 1 is a data flow inventory taken from the code. Every claim is backed by a file and line or by a vendor primary source. Cost: 0 USD, no API calls.

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
- Quality metric: 5 of 11 stations without an EU location commitment. The last T01 agent request has 64 personal-data hits, 8 of them direct identifiers.

## Next Steps
- Close the open points: Anthropic's subprocessors, the retention contradiction, the Neon DPA, and what the SDK does in the container.
- Classify the agent under the AI Act, then write the obligations memo.

Details (German): [Data flow](docs/DATENFLUSS.md) · [Data minimisation](docs/DATENMINIMIERUNG.md) · [T01 requests](evals/t01_anfragen.md) · [Decisions](docs/decisions.md)
