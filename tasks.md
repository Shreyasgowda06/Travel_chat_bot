# Build Tasks — TravelWith AI Chatbot

> Execute these tasks in order. Each task is a discrete, testable unit. Do not proceed to the next task until the current one is verified working.

---

**Task 1 — Scaffold project and install dependencies**
Create the project folder structure (`main.py`, `routers/`, `services/`, `code.html`), create `requirements.txt` with `fastapi`, `uvicorn[standard]`, `google-generativeai`, `python-dotenv`, and `python-multipart`, then run `pip install -r requirements.txt` and confirm no errors.

---

**Task 2 — Set up `.env` file and verify API key loads**
Create a `.env` file in the project root with `GEMINI_API_KEY=<student inserts key here>`, then in `main.py` call `load_dotenv()` at startup and assert that `os.getenv("GEMINI_API_KEY")` is not None — raise a clear `RuntimeError("GEMINI_API_KEY not set in .env")` if it is missing, so students know immediately when their key is misconfigured.

---

**Task 3 — Build the Gemini service layer with system instruction**
Create `services/gemini.py` that configures the `google-generativeai` client, defines the travel-expert system instruction (helpful, not paranoid — answers general travel questions, adds disclaimers only where relevant, refuses only off-topic or harmful requests), and exposes `generate_chat_response(history)` and `generate_vision_response(prompt, image_bytes, mime_type)` functions.

---

**Task 4 — Implement 429 retry logic in the Gemini service**
Inside the Gemini service functions, wrap every API call in a try/except that catches `google.api_core.exceptions.ResourceExhausted`; on first catch, sleep 2 seconds and retry once; if the retry also raises `ResourceExhausted`, return the string `"I'm a little busy right now — please try again in a moment."` to the caller without raising.

---

**Task 5 — Implement distinct 403 / GoogleAPIError handling**
In the same try/except blocks, add a separate `except google.api_core.exceptions.PermissionDenied` clause (and a broader `except google.api_core.exceptions.GoogleAPIError` clause below it) that returns the actual `str(exception)` message to the caller — for example `"API key is invalid or has no permissions for this project"` — so this error is never silently swallowed into the generic busy message and students can immediately diagnose a bad key.

---

**Task 6 — Build the `/chat` POST endpoint**
Create `routers/chat.py` with a `POST /chat` route that accepts `{"messages": [...]}` as a JSON body (full conversation history from the frontend), passes it to `generate_chat_response()`, and returns `{"reply": response_text}`; register this router in `main.py`.

---

**Task 7 — Build the `/vision` POST endpoint**
Create `routers/vision.py` with a `POST /vision` route that accepts `multipart/form-data` with a `prompt` text field and an `image` file upload, reads the image bytes and MIME type, passes them to `generate_vision_response()`, and returns `{"reply": response_text}`; register this router in `main.py`.

---

**Task 8 — Serve `code.html` at `GET /` and run on port 8000**
In `main.py`, add a `GET /` route that reads `code.html` from disk and returns it as an `HTMLResponse`; configure Uvicorn to run on `host="0.0.0.0"` and `port=8000`; verify the UI loads in the browser at `http://localhost:8000`.

---

**Task 9 — Strip all demo data and placeholder content from `code.html`**
Open `code.html` and remove any hardcoded sample chat messages, fake bot replies, mock conversation history, and placeholder response strings from both the HTML markup and any inline `<script>` blocks, so the chat area is empty on load and shows only real Gemini responses.

---

**Task 10 — Add `marked.js` and wire Markdown rendering into bot bubbles**
Add `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` to the `<head>` of `code.html`; update the bot bubble creation function so that every bot message is rendered with `bubble.innerHTML = marked.parse(replyText)` instead of `textContent` — verify by sending a question that returns a bulleted list and confirming the bullets render as HTML, not raw `*` characters.

---

**Task 11 — Implement the empty-send guard on the Send button**
In `code.html`'s inline script, add an `input` event listener on the text field that sets `sendButton.disabled = true` whenever `input.value.trim().length === 0` and `false` otherwise; call the same check on page load so the button starts disabled; verify that clicking Send with an empty field is impossible and no network request fires.

---

**Task 12 — Wire the chat input to `/chat` with full conversation history**
Implement the `sendMessage()` function in `code.html` that: appends the user's text to a `conversationHistory` array in `{role: "user", parts: [text]}` format, POSTs the full array to `/chat`, awaits the reply, appends `{role: "model", parts: [reply]}` to history, and renders both the user bubble (right-aligned, Sky Blue) and bot bubble (left-aligned, white card with Markdown via `marked.parse()`); show a typing indicator while the request is in flight.

---

**Task 13 — Wire the image-upload button to `/vision`**
Add a hidden `<input type="file" accept="image/*,.pdf">` triggered by the existing upload icon button; when a file is selected, store it as `stagedFile`; on Send, if `stagedFile` is set, POST to `/vision` as `multipart/form-data` with the `prompt` text and `image` file instead of posting to `/chat`; clear `stagedFile` and show a file-name preview badge after selection so the user knows a file is attached.

---

**Task 14 — Test all error paths and do a full end-to-end smoke test**
Verify each of the following manually: (a) empty input → Send button is disabled, no request fires; (b) valid travel question → Markdown renders correctly in the bubble; (c) travel image upload → bot responds with image-contextual advice; (d) non-travel image → bot redirects politely; (e) set a bad API key in `.env` → the chat shows the actual PermissionDenied error message, not a generic busy message; (f) multi-turn conversation → bot references earlier context correctly.
