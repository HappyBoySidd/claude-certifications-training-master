# CCDV-F SIM-02 — Document Pipeline: Batch, Streaming and Caching

**Primary domains:** 2 Applications and Integration, 5 Model Selection and Optimization ·
**Decisions:** 10 · **Time:** 20 min

## Scene (original, written from the official objectives)

You're the developer on a freight company's document team. Two jobs use Claude on the same
scanned delivery forms. The **back-office job** extracts fields from a backlog of tens of thousands
of forms for a month-end audit that nobody reads until next week. The **customer portal** lets a
driver upload a photo of one form and see a plain-English summary on screen. Both jobs send the
same three pages of extraction instructions and a JSON schema on every call, and the bill is
climbing.


---

## The decisions (answer these before you open the key)

1. How to run the month-end backlog
2. Drivers stare at a blank portal screen for many seconds
3. How to send the driver's photo
4. The same instructions and schema are paid for on every call
5. Cache reads stay near zero. The system prompt starts with today's timestamp and a request ID
6. Most forms are clean and typed; a few have long handwritten damage notes
7. Some summaries end mid-JSON and the parser crashes
8. Finance wants cost per customer
9. The portal gets HTTP 429 errors at the morning rush
10. A stream sends an `overloaded_error` event partway through

<details><summary><b>Answer key (coach key): don't open until you've finished the simulation</b></summary>

| # | Decision | Correct move | Traps to use as distractors | Objective | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | How to run the month-end backlog | **Message Batches API**: asynchronous, 50% of standard price, results within 24 hours (most finish much sooner) | Fire all requests in parallel through the realtime API; lower `max_tokens` to save money; switch to the smallest model without testing quality | D2 Claude API Mechanics (realtime vs batch) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 2 | Drivers stare at a blank portal screen for many seconds | **Stream the response** (`stream: true`, server-sent events) so text appears as it's generated | Move the portal to the Batches API; use a bigger model; raise `max_tokens` | D2 Claude API Mechanics (streaming) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 3 | How to send the driver's photo | Send it as an **image content block** (base64 or URL), placed **before** the text instructions | Run your own text description of the photo and send only that; send the file name; put the image after the long instructions | D2 Claude API Mechanics (vision) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 4 | The same instructions and schema are paid for on every call | **Prompt caching**: stable content (tools, system instructions, schema) first, a `cache_control` breakpoint at the end of it, the per-form content after | Put the form image at the top so it's "seen first"; cut the instructions in half and lose accuracy; resend the instructions in each user turn | D5 Cost and Token Management (prompt caching) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 5 | Cache reads stay near zero. The system prompt starts with today's timestamp and a request ID | **Move changing values after the breakpoint.** The cache matches the exact prefix (tools, then system, then messages), so any change early in it is a miss | Switch to the 1-hour cache duration; add more breakpoints; switch models | D5 Cost and Token Management (cache check-pointing) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 6 | Most forms are clean and typed; a few have long handwritten damage notes | **Route by difficulty**: a fast, low-cost tier for routine extraction, a stronger tier for the hard cases, confirmed with a small eval | The most capable model for everything "to be safe"; the cheapest model for everything without testing; pick by price alone | D5 Model Selection and Tradeoffs | [Lesson 2, section 5.3](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 7 | Some summaries end mid-JSON and the parser crashes | **Check `stop_reason`.** On `max_tokens`, raise the budget or split the work; never treat truncated output as complete | Parse whatever came back; retry the identical request; add "be brief" to the prompt | D2 Claude API Mechanics; D5 LLM Fundamentals (tokens) | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 8 | Finance wants cost per customer | **Record the `usage` block** from each response (input, output, cache write and cache read tokens); use token counting to estimate big documents before sending | Estimate from character counts; wait for the monthly invoice; count only output tokens | D5 Cost and Token Management (usage tracking) | [Lesson 2, section 5.4](../../02-Lessons/03-CCDV-F-Developer/L02-model-selection-and-optimization.md) |
| 9 | The portal gets HTTP 429 errors at the morning rush | **Honor the `retry-after` header**, back off with jitter, queue requests, and ramp traffic up gradually | Retry immediately in a tight loop; rotate to another API key to dodge the limit; fail the request straight away | D2 Software Engineering Foundations; D5 Technical Fundamentals | [Lesson 1, section 2.4](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md) |
| 10 | A stream sends an `overloaded_error` event partway through | **Treat it as transient**: retry with backoff, show a friendly "try again" message, and never present the partial text as the final summary. Don't retry 400 invalid-request errors unchanged. | Show the partial summary as final; retry every error type the same way forever; move the whole portal to batch | D2 Claude API Mechanics; D4 Debugging and Error Handling | [Lesson 1, section 2.3](../../02-Lessons/03-CCDV-F-Developer/L01-applications-and-integration.md), [Lesson 7, section 4.1](../../02-Lessons/03-CCDV-F-Developer/L07-claude-code-eval-and-debugging.md) |

**Scoring:** 8 or more is a pass. Decisions 1 and 4 are the heart of the scenario: *match the API
to who is waiting (batch when nobody is, streaming when a person is)*, and *cache the stable
prefix, put what changes last*.

Sources: batch processing,
prompt caching,
streaming,
vision,
rate limits.

</details>