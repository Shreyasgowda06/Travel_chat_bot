# Implementation Plan — TravelWith AI Chatbot

## Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI (Python 3.11+) |
| AI model | `gemini-2.5-flash-lite` via `google-generativeai` Python SDK |
| API key management | `python-dotenv` — loaded from `.env` in project root |
| Frontend | Vanilla JS — `code.html` used **as-is** (no redesign) |
| Markdown rendering | `marked.js` via CDN, injected into `code.html` |
| Static file serving | FastAPI `StaticFiles` or inline HTML response at `/` |
| Transport | HTTP/1.1 JSON — POST endpoints `/chat` and `/vision` |

---

## Project Structure

```
project-root/
├── .env                  # GEMINI_API_KEY=your_key_here
├── main.py               # FastAPI application entry point
├── routers/
│   ├── chat.py           # /chat POST endpoint
│   └── vision.py         # /vision POST endpoint
├── services/
│   └── gemini.py         # Gemini SDK wrapper, retry logic, error handling
├── code.html             # Stitch UI export (modified in-place for JS wiring)
└── requirements.txt
```

---

## Components — Build Order

### Step 1 — Project Scaffolding
Set up the Python virtual environment, install dependencies, create the `.env` file template, and verify `GEMINI_API_KEY` loads correctly at startup. Fail fast with a clear error if the key is missing.

**`requirements.txt`:**
```
fastapi
uvicorn[standard]
google-generativeai
python-dotenv
python-multipart
```

---

### Step 2 — Gemini Service Layer (`services/gemini.py`)
Centralised wrapper around the `google-generativeai` SDK. Responsibilities:

- Initialise the client using `genai.configure(api_key=os.getenv("GEMINI_API_KEY"))`
- Define the **system instruction** (travel-expert persona — helpful, not paranoid)
- Expose two functions:
  - `generate_chat_response(history: list[dict]) -> str` — text-only chat
  - `generate_vision_response(prompt: str, image_bytes: bytes, mime_type: str) -> str` — multimodal
- Implement retry logic:
  - Catch `google.api_core.exceptions.ResourceExhausted` (429) → sleep 2 seconds → retry once → on second failure return friendly busy message
  - Catch `google.api_core.exceptions.PermissionDenied` and other `GoogleAPIError` subtypes → return the actual `exception.message` string (never swallow as busy)
  - Catch all other exceptions → log to stderr → return "Something went wrong, please retry."

**System Instruction (travel expert, not paranoid):**
```
You are TravelWith AI, a knowledgeable and friendly travel assistant. 
You help users with destination discovery, itinerary planning, budget estimation, 
visa and documentation requirements, transport options, accommodation, local food, 
and cultural experiences.

Answer general travel questions confidently. Add brief disclaimers only where 
genuinely appropriate (e.g. visa rules change — verify with the official embassy). 
Do NOT refuse routine travel questions.

Refuse only: requests clearly unrelated to travel, harmful or dangerous instructions, 
and requests for personalised medical or legal advice. 
For borderline questions, answer the travel-relevant part and note any limitations.
```

---

### Step 3 — Chat Endpoint (`routers/chat.py`)

```
POST /chat
Content-Type: application/json

Request:  { "messages": [{"role": "user"|"model", "parts": ["..."]}] }
Response: { "reply": "..." }
```

- Accepts the full conversation history from the frontend on every request (stateless backend)
- Passes history to `generate_chat_response()`
- Returns `{"reply": response_text}`

---

### Step 4 — Vision Endpoint (`routers/vision.py`)

```
POST /vision
Content-Type: multipart/form-data

Fields:
  prompt: str
  image: File (JPEG / PNG / WEBP / PDF)

Response: { "reply": "..." }
```

- Reads `image` bytes and detects MIME type from the uploaded file's content-type header
- Passes `(prompt, image_bytes, mime_type)` to `generate_vision_response()`
- Returns `{"reply": response_text}`

---

### Step 5 — FastAPI App Entry Point (`main.py`)

- Load `.env` on startup via `load_dotenv()`
- Mount routers at `/chat` and `/vision`
- Serve `code.html` at `GET /` as a plain HTML response
- Run on `host="0.0.0.0"`, `port=8000`

---

### Step 6 — Frontend Wiring (`code.html` modifications)

The HTML file is used as-is visually. The following JS additions are made inside a `<script>` tag at the bottom of `<body>`:

#### 6a — Remove demo/placeholder content
Strip any hardcoded sample messages, fake conversation history, or demo reply text from the HTML and JS before wiring live API calls.

#### 6b — Add `marked.js` via CDN
```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
```
All bot bubble content must be set via `bubble.innerHTML = marked.parse(replyText)` — never `textContent`.

#### 6c — Empty-send guard
```javascript
const input = document.querySelector('input[type="text"]');
const sendBtn = document.querySelector('[data-icon="send"]').parentElement;

function updateSendState() {
  sendBtn.disabled = input.value.trim().length === 0;
}
input.addEventListener('input', updateSendState);
updateSendState(); // initial state on load
```

#### 6d — Chat message rendering
- Maintain a `conversationHistory` array in JS (format: `[{role, parts: [text]}]`)
- On send: append user message, POST full history to `/chat`, append model reply
- Render user bubbles right-aligned (Sky Blue), bot bubbles left-aligned (white card)
- Show a typing indicator (animated dots) while awaiting response

#### 6e — Image upload wiring
- The image-upload button triggers `<input type="file" accept="image/*,.pdf">`
- On file select, store the file reference; on send, POST to `/vision` as `multipart/form-data` with `prompt` + `image`
- After vision response, clear the staged file

#### 6f — Error display
- On any fetch error or non-200 response, render the error text inside a bot bubble styled with the `error` color token (`#ba1a1a` text, `error-container` background)

---

### Step 7 — End-to-End Testing Checklist

- [ ] Empty input → Send button is visually disabled; no network request fires
- [ ] Text message → bot replies with formatted Markdown (bold, lists render correctly)
- [ ] Image upload (travel photo) → bot describes or advises based on image
- [ ] Image upload (non-travel image) → bot redirects politely
- [ ] Simulate 429 → friendly retry message appears after ~2 seconds
- [ ] Invalid API key → distinct error message appears in chat (not generic busy)
- [ ] Conversation history → bot references earlier messages correctly in multi-turn chat

---

## Free Tier Constraints (gemini-2.5-flash-lite)

| Limit | Value |
|---|---|
| Requests per minute (RPM) | 15 |
| Requests per day (RPD) | 1,000 |
| Context window | 1M tokens |
| Multimodal support | ✅ Yes |

The single 2-second retry on 429 is calibrated for the 15 RPM free-tier limit. No further rate-limiting is implemented client-side in v1.
