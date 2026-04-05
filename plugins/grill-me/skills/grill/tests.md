# Tests: grill

## Scenarios

### Scenario 1: architectural decision
**Input context:** User presents a plan: "I want to migrate our monolith to microservices over the next quarter. Each team owns one service. We'll use REST between services."
**Invoke:** `/grill`
**Expected format:** Questions grouped under domain headings (e.g., `### Operational Complexity`, `### Data Consistency`). 2–3 questions per group. No recommendations or answers — only questions.

### Scenario 2: product feature idea
**Input context:** User proposes: "Add an AI-powered auto-reply feature to our customer support inbox that responds to tickets without human review."
**Invoke:** `/grill`
**Expected format:** Domain-grouped questions. No advocacy for or against the idea. Ends when user signals stop.

### Scenario 3: stop signal triggers synthesis
**Input context:** After a grilling session, user says "ok that's enough, summarize".
**Invoke:** (continuation of grilling session)
**Expected format:** `### Core Tensions Surfaced` section with 1–2 paragraphs. Summarizes the most important unresolved questions and tradeoffs. Does NOT give a recommendation.

### Scenario 4: already-decided plan
**Input context:** User says "We've already decided to use PostgreSQL, I just want you to grill the schema design."
**Invoke:** `/grill`
**Expected format:** Questions focus only on schema design — does not re-open the database choice. Respects the stated constraint.

## Rubric

1. **Questions only, no recommendations** — the skill stays Socratic throughout. No "you should", "I recommend", or implied answers.
   - Pass: every sentence is a question or a domain heading
   - Fail: any sentence that recommends, advises, or advocates
2. **Domain grouping** — questions are organized under named domain headings with 2–3 questions each.
   - Pass: `### Data Consistency\n1. How will you handle...\n2. What happens when...`
   - Fail: flat list of questions with no grouping, or single-question groups
3. **Distinctness of domains** — at least 3 different concern areas are surfaced.
   - Pass: Operational, Data, Team, User Impact, Cost — distinct angles
   - Fail: all questions are about the same narrow concern
4. **Synthesis after stop** — on stop signal, produces `### Core Tensions Surfaced` section with no recommendation.
   - Pass: "The central unresolved question is whether X or Y..." (identifies tension, doesn't resolve it)
   - Fail: "You should choose X" or no synthesis produced
5. **Constraint respect** — does not re-open decisions the user has declared closed.
   - Pass: focuses on schema when DB is declared fixed
   - Fail: "But are you sure PostgreSQL is right?"

## Golden Set

### Golden 1 — microservices plan
**Input:** "I want to migrate our monolith to microservices. Each team owns one service. We'll use REST."
**Ideal output:**
```
### Deployment & Operations
1. How will you handle a failure in Service A that cascades to Services B and C?
2. Who owns the deploy pipeline for each service — the team, or a central platform team?

### Data Ownership
1. Which service owns the user record, and how do others access it?
2. If two services need the same data, will you duplicate it or introduce a shared service?

### Migration Path
1. Which service do you carve out first, and what's the rollback plan if it goes wrong?
2. How do you handle the period when part of the system is a monolith and part is microservices?
```
