# Product Requirements Document — TravelWith AI Chatbot

## Vision

TravelWith AI is a conversational travel assistant that helps users discover destinations, plan itineraries, estimate budgets, and navigate travel logistics — all through a friendly, expert chat interface. The product wraps the Gemini `gemini-2.5-flash-lite` model in a polished, mobile-first UI exported from Google Stitch, delivering a Wanderlust-branded experience that feels native, fast, and trustworthy.

---

## Target User

- Leisure and adventure travelers aged 22–45 planning domestic or international trips
- Students and young professionals seeking budget-conscious travel advice
- First-time international travelers who need visa, documentation, and logistics guidance
- Users who want AI-assisted planning without switching between multiple apps or tabs

---

## Must-Have Features

### 1. Domain-Specialised Chat (`/chat`)
- Accepts a user text message and returns a Gemini-powered response scoped to travel and tourism
- Maintains conversational context across multiple turns within a session
- System instruction establishes the bot as a **helpful travel expert** — it answers general travel questions (best seasons to visit, packing tips, visa overviews, currency advice, common cultural norms) with appropriate disclaimers where relevant
- Refuses only: requests that are clearly off-topic (medical diagnoses, legal advice, coding help), genuinely harmful asks, or requests for prescription-level personalised advice
- **Does NOT over-refuse**: common travel knowledge, popular itineraries, general health-and-safety tips for travellers, and well-established practices must be answered

### 2. Image Upload & Vision Analysis (`/vision`)
- User can attach a photo (destination shot, boarding pass, itinerary screenshot, visa document, travel map) alongside a text prompt
- Backend sends image + prompt to Gemini multimodal endpoint
- Bot verifies the image is travel-related before answering; if off-topic (e.g. code screenshot, medical report), it returns a polite redirect message
- Supported formats: JPEG, PNG, WEBP, PDF (first page)

### 3. Empty-Send Guard (Frontend)
- The Send button is **disabled** whenever the input field is empty or contains only whitespace
- Activates instantly as the user types any non-whitespace character
- Prevents accidental empty POST requests to the backend

### 4. Markdown Rendering
- Gemini natively outputs Markdown (`**bold**`, `*italic*`, `- lists`, `## headers`)
- All bot message bubbles must render this as formatted HTML — raw `**` and `*` symbols must never appear to the end user
- Implemented via `marked.js` loaded from CDN

### 5. Rate Limit Handling (429)
- On HTTP 429, backend retries once after a 2-second backoff
- If the second attempt also fails, returns a friendly user-facing message: _"I'm a little busy right now — please try again in a moment."_

### 6. Auth / Permission Error Handling (403 / GoogleAPIError)
- Distinctly caught and surfaced to the chat as the actual error message (e.g. _"API key is invalid or has no permissions for this project"_)
- Must NOT be swallowed into the generic busy/retry message — this distinction is critical for debugging during development

### 7. Environment-Based API Key
- `GEMINI_API_KEY` loaded from a `.env` file in the project root using `python-dotenv`
- Never hard-coded in source files

---

## Non-Goals

- No user authentication or persistent account system (v1)
- No real-time flight or hotel price lookups via third-party APIs
- No booking or transaction capability
- No dark mode toggle (system follows Stitch light-mode design)
- No multi-language localisation (English only, v1)
- No conversation history persisted across browser sessions

---

## Success Criteria

| Metric | Target |
|---|---|
| Chat response latency (p90) | < 4 seconds on gemini-2.5-flash-lite free tier |
| Empty-send guard | 100% — zero empty POSTs reach the backend |
| Markdown rendering | All `**bold**` and `*italic*` render as HTML; no raw symbols visible |
| 429 retry success rate | ≥ 80% of rate-limit hits resolved by the single retry |
| 403 errors surfaced | 100% — never swallowed as generic busy message |
| Off-topic image detection | Bot redirects for non-travel images in > 90% of test cases |
| Domain refusal rate | Bot answers legitimate travel questions; refuses < 5% of valid travel queries |
