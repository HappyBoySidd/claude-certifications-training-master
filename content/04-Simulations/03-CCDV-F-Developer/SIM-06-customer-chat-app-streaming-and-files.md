# CCDV-F SIM-06 — Customer Chat App: Streaming, Errors and Files

**Primary domains:** 2 Applications and Integration (with touches of 5 and 7) · **Decisions:** 10 ·
**Time:** 20 min

## Scene (original, written from the official objectives)

You're the developer on a travel-insurance company's claims chat. Customers open it on the website,
describe what went wrong, upload **photos** of damaged luggage and **PDF receipts**, and can ask
Claude to draft a claim letter they then send. The answer has to feel live, the claims system reads
a fixed set of fields from each finished chat, and legal says customer data must be processed in the
US. Launch is in two weeks, and the first test day went badly.


---

## The decisions (answer these before you open the key)

1. Testers stare at a blank chat bubble for several seconds before anything appears
2. The front-end team wants the browser to call the Claude API directly, "to save a hop"
3. How to send a customer's photo of a torn suitcase
4. A customer refers back to the same 20-page PDF receipt pack across many turns, and re-sending it each time is slow
5. The long "draft my claim letter" request fails with an HTTP timeout on the non-streaming call
6. Halfway through a streamed answer, an `overloaded_error` event arrives after the HTTP 200
7. On the test day, every call starts failing with a 429 that has **no** `retry-after` header
8. Each chat gets slower and more expensive the longer it runs
9. The claims system needs policy number, incident date, item list and amount from each finished chat
10. Legal: customer data must be processed in the US

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | Testers stare at a blank chat bubble for several seconds before anything appears | **Stream the response** (`stream: true`, server-sent events) so text shows up as it's generated | Switch to a bigger model; move chat to the Batches API; raise `max_tokens` | D2 Claude API Mechanics (streaming) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 2 | The front-end team wants the browser to call the Claude API directly, "to save a hop" | **Keep the API key on your server.** The backend calls Claude, streams the reply, and relays it to the browser | Ship the key in the web app but obfuscate it; one shared key in a public config file; let each customer paste their own key | D2 Claude Application Design; D7 Identity, Secrets, and Key Management | [Lesson 2, section 5.2](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md), [Lesson 6, section 7.5](../../02-Lessons/03-CCDV-F-Developer/L06-security-and-safety.md) |
| 3 | How to send a customer's photo of a torn suitcase | An **image content block** (base64, URL or a Files API `file_id`) placed **before** the text of the question | Describe the photo yourself and send only the text; send the file name; put the image after a long block of instructions | D2 Claude API Mechanics (vision) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 4 | A customer refers back to the same 20-page PDF receipt pack across many turns, and re-sending it each time is slow | **Upload it once with the Files API and reference it by `file_id`** in later turns | Paste the PDF's text into every message; ask the customer to re-upload each turn; summarize it once and throw the original away | D2 Claude API Mechanics (data access patterns) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 5 | The long "draft my claim letter" request fails with an HTTP timeout on the non-streaming call | **Stream it** (or use the SDK's streaming helper that returns the final message), since long outputs need streaming to avoid HTTP timeouts | Retry the same call; lower `max_tokens` until it fits and truncate letters; move it to a batch the customer checks tomorrow | D2 Claude API Mechanics (streaming); D5 Technical Fundamentals | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 2, section 5.2](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 6 | Halfway through a streamed answer, an `overloaded_error` event arrives after the HTTP 200 | **Treat it as transient**: retry with backoff and jitter, tell the customer you're retrying, and never show the half answer as final | Assume a 200 means success and show the partial text; retry every error the same way forever; switch the chat to batch | D2 Claude API Mechanics; D4 Debugging and Error Handling | [Lesson 1, section 2.4](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 7, section 4.1](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |
| 7 | On the test day, every call starts failing with a 429 that has **no** `retry-after` header | **That's the spend cap, not a per-minute limit.** Retrying won't help: raise the limit and alert the team | Back off and retry for an hour; rotate to another key; lower `max_tokens` | D2 Software Engineering Foundations (errors) | [Lesson 1, section 2.4](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 8 | Each chat gets slower and more expensive the longer it runs | **The Messages API is stateless**, so every turn resends the history. Cache the stable prefix (system prompt, policy text) and summarize or trim old turns | Assume the API stores the chat for you; drop the system prompt after turn one; switch to a smaller model with no eval | D2 Claude API Mechanics; D5 Cost and Token Management | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 9 | The claims system needs policy number, incident date, item list and amount from each finished chat | **Structured outputs** with a JSON schema: required fields, `null` allowed when the customer didn't say, then **check the meaning in code** (the amount matches the receipts) | "Please reply in JSON" in the prompt; prefill `{`; accept anything that parses | D2 Claude Application Design (schema design) | [Lesson 1, section 2.5](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 4, section 6.5](../../02-Lessons/03-CCDV-F-Developer/L04-prompt-and-context-engineering.md) |
| 10 | Legal: customer data must be processed in the US | **Read it as an infrastructure requirement** and set the data-residency option (`inference_geo` on the Claude API, or a regional endpoint on a cloud platform). Check which models support it and the price change | Put "keep data in the US" in the system prompt; strip names from messages and call it done; ignore it because the servers "are probably in the US" | D2 Understanding Requirements (infrastructure requirements) | [Lesson 1, section 2.1](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |

**Scoring:** 8 or more is a pass. Decisions 1 and 7 are the heart of the scenario: *a person is
waiting, so stream it*, and *read the error before you retry: temporary errors get backoff, a spend
cap or a bad request doesn't*.

Sources (Tier 1): [CCDV-F exam guide, Domain 2](https://anthropic-partners.skilljar.com/page/partner-certifications),
streaming,
vision,
working with messages,
rate limits,
structured outputs,
prompt caching,
pricing (data residency).
Files API: [platform.claude.com Files API docs](https://platform.claude.com/docs/en/build-with-claude/files)
(not saved locally; check the current page).

</details>