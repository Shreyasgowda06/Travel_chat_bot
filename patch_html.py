import re

with open('code.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add marked.js to head
if 'marked.min.js' not in content:
    content = content.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>\n</head>')

# Make main scrollable and empty
main_match = re.search(r'<main[^>]*>.*?</main>', content, flags=re.DOTALL)
if main_match:
    main_tag = re.search(r'<main[^>]*>', main_match.group(0)).group(0)
    # add overflow-y-auto, change justify-end to justify-start
    main_tag = main_tag.replace('justify-end', 'justify-start').replace('flex-col', 'flex-col overflow-y-auto')
    content = content[:main_match.start()] + main_tag + '</main>' + content[main_match.end():]

# Ensure the sendBtn has an id or is identifiable. It has data-icon="send".
# Ensure mic button has data-icon="mic".

# Add the script
script_code = """
<script>
    const input = document.querySelector('input[type="text"]');
    const sendBtn = document.querySelector('[data-icon="send"]').parentElement;
    const mainContainer = document.querySelector('main');
    
    // Change mic to attach_file for upload
    const micIcon = document.querySelector('[data-icon="mic"]');
    if (micIcon) {
        micIcon.innerText = 'attach_file';
        micIcon.setAttribute('data-icon', 'attach_file');
    }
    const uploadBtn = micIcon ? micIcon.parentElement : null;
    
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*,.pdf';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);
    
    let stagedFile = null;
    let conversationHistory = [];
    
    const inputWrapper = input.parentElement;
    const fileBadge = document.createElement('div');
    fileBadge.className = 'absolute -top-8 left-4 bg-surface-variant text-on-surface-variant text-xs px-2 py-1 rounded-md hidden shadow-sm cursor-pointer border border-outline-variant/30';
    inputWrapper.parentElement.appendChild(fileBadge);
    
    if (uploadBtn) {
        uploadBtn.addEventListener('click', () => fileInput.click());
    }
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            stagedFile = e.target.files[0];
            fileBadge.innerText = stagedFile.name + " (Click to remove)";
            fileBadge.style.display = 'block';
        }
        updateSendState();
    });
    
    fileBadge.addEventListener('click', () => {
        stagedFile = null;
        fileInput.value = '';
        fileBadge.style.display = 'none';
        updateSendState();
    });

    function updateSendState() {
        sendBtn.disabled = input.value.trim().length === 0 && !stagedFile;
        sendBtn.style.opacity = sendBtn.disabled ? '0.5' : '1';
    }
    input.addEventListener('input', updateSendState);
    updateSendState();
    
    function appendBubble(role, text, isError=false) {
        const bubble = document.createElement('div');
        bubble.className = "p-4 rounded-2xl shadow-sm max-w-[85%] animate-[slideUp_0.3s_ease-out] ";
        
        if (role === 'user') {
            bubble.className += "bg-primary text-on-primary self-end ml-auto rounded-br-sm";
            bubble.innerText = text;
        } else {
            if (isError) {
                bubble.className += "bg-error-container text-error self-start mr-auto rounded-bl-sm";
                bubble.innerText = text; // Don't parse markdown for errors
            } else {
                bubble.className += "glass-panel text-on-surface self-start mr-auto rounded-bl-sm border border-surface-variant/50 prose prose-sm max-w-none prose-headings:text-on-surface prose-a:text-primary";
                bubble.innerHTML = marked.parse(text);
            }
        }
        
        const row = document.createElement('div');
        row.className = "w-full flex mb-4";
        row.appendChild(bubble);
        mainContainer.appendChild(row);
        
        mainContainer.scrollTo({ top: mainContainer.scrollHeight, behavior: 'smooth' });
        return bubble;
    }
    
    function appendTypingIndicator() {
        const bubble = document.createElement('div');
        bubble.className = "glass-panel text-on-surface p-4 rounded-2xl shadow-sm max-w-[85%] self-start mr-auto rounded-bl-sm border border-surface-variant/50 mb-4 animate-[slideUp_0.3s_ease-out]";
        bubble.innerHTML = '<div class="flex gap-1 items-center h-6"><div class="w-2 h-2 bg-on-surface-variant rounded-full animate-bounce"></div><div class="w-2 h-2 bg-on-surface-variant rounded-full animate-bounce" style="animation-delay: 0.2s"></div><div class="w-2 h-2 bg-on-surface-variant rounded-full animate-bounce" style="animation-delay: 0.4s"></div></div>';
        
        const row = document.createElement('div');
        row.className = "w-full flex mb-4 typing-row";
        row.appendChild(bubble);
        mainContainer.appendChild(row);
        mainContainer.scrollTo({ top: mainContainer.scrollHeight, behavior: 'smooth' });
        return row;
    }

    async function sendMessage() {
        if (sendBtn.disabled) return;
        
        const text = input.value.trim();
        const file = stagedFile;
        
        input.value = '';
        stagedFile = null;
        fileInput.value = '';
        fileBadge.style.display = 'none';
        updateSendState();
        
        if (text || file) {
            let userText = text;
            if (file) {
                userText = `[Attached File: ${file.name}] ` + text;
            }
            appendBubble('user', userText);
            
            if (!file) {
                conversationHistory.push({role: "user", parts: [text]});
            }
        }
        
        const typingRow = appendTypingIndicator();
        
        try {
            let res;
            if (file) {
                const formData = new FormData();
                formData.append('prompt', text || 'Describe this file');
                formData.append('image', file);
                
                res = await fetch('/vision', {
                    method: 'POST',
                    body: formData
                });
            } else {
                res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({messages: conversationHistory})
                });
            }
            
            const data = await res.json();
            typingRow.remove();
            
            if (!res.ok) {
                throw new Error(data.reply || data.detail || "Server error");
            }
            
            appendBubble('model', data.reply);
            
            if (!file) {
                conversationHistory.push({role: "model", parts: [data.reply]});
            }
        } catch (err) {
            typingRow.remove();
            appendBubble('model', err.message, true);
        }
    }
    
    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

</script>
</body>
"""

content = content.replace('</body>', script_code)

with open('code.html', 'w', encoding='utf-8') as f:
    f.write(content)
