// ── DOM References ────────────────────────────────────────────
const messagesEl = document.getElementById('messages');
const inputEl    = document.getElementById('userInput');

// ── Init ──────────────────────────────────────────────────────
window.addEventListener('load', () => {
    sendToBot('hello');
});

// ── Key Handler ───────────────────────────────────────────────
function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

// ── Send user message ─────────────────────────────────────────
function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;
    appendUserMessage(text);
    inputEl.value = '';
    sendToBot(text);
}

// ── Quick button shortcut ─────────────────────────────────────
function sendQuick(text) {
    appendUserMessage(text);
    sendToBot(text);
}

// ── Append user bubble ────────────────────────────────────────
function appendUserMessage(text) {
    const msgEl = document.createElement('div');
    msgEl.className = 'msg msg-user';
    msgEl.innerHTML = `<div class="bubble bubble-user">${escapeHTML(text)}</div>`;
    messagesEl.appendChild(msgEl);
    scrollToBottom();
}

// ── Show typing indicator ─────────────────────────────────────
function showTyping() {
    const el = document.createElement('div');
    el.className = 'msg msg-bot';
    el.id = 'typing-msg';
    el.innerHTML = `
        <div class="bot-label">Chef Bot</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>`;
    messagesEl.appendChild(el);
    scrollToBottom();
}

function removeTyping() {
    const el = document.getElementById('typing-msg');
    if (el) el.remove();
}

// ── Fetch from Flask ──────────────────────────────────────────
async function sendToBot(text) {
    showTyping();
    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await resp.json();
        removeTyping();
        renderBotResponse(data);
    } catch (err) {
        removeTyping();
        appendBotText("Hmm, something went wrong in the kitchen! 🔥 Please try again.");
    }
}

// ── Render bot responses ──────────────────────────────────────
function renderBotResponse(data) {
    switch (data.type) {
        case 'greeting':
            appendBotText(data.message);
            break;

        case 'recipe':
            appendBotText("Here's a recipe for you! ✨");
            appendRecipeCard(data.recipe);
            break;

        case 'suggestions':
            appendBotText(data.message);
            appendSuggestions(data.suggestions);
            break;

        case 'list':
            appendBotText(data.message);
            appendList(data.items);
            break;

        case 'fallback':
            appendBotText(data.message);
            break;

        default:
            appendBotText(data.message || "Sorry, I didn't understand that.");
    }
    scrollToBottom();
}

// ── Plain text bubble ─────────────────────────────────────────
function appendBotText(text) {
    const msgEl = document.createElement('div');
    msgEl.className = 'msg msg-bot';
    msgEl.innerHTML = `
        <div class="bot-label">Chef Bot</div>
        <div class="bubble bubble-bot">${renderMarkdownLight(text)}</div>`;
    messagesEl.appendChild(msgEl);
}

// ── Recipe card ───────────────────────────────────────────────
function appendRecipeCard(r) {
    const ingredientsHTML = r.ingredients
        .map(i => `<li>${escapeHTML(i)}</li>`)
        .join('');

    const stepsHTML = r.steps
        .map(s => `<li>${escapeHTML(s)}</li>`)
        .join('');

    const msgEl = document.createElement('div');
    msgEl.className = 'msg msg-bot';
    msgEl.innerHTML = `
        <div class="bot-label">Chef Bot</div>
        <div class="recipe-card">
            <div class="recipe-header">
                <span class="recipe-emoji">${r.emoji}</span>
                <div class="recipe-name">${escapeHTML(r.name)}</div>
                <div class="recipe-meta">
                    <span class="meta-tag meta-time">⏱ ${escapeHTML(r.time)}</span>
                    <span class="meta-tag meta-diff">${escapeHTML(r.difficulty)}</span>
                </div>
            </div>
            <div class="recipe-body">
                <div class="section-title">Ingredients</div>
                <ul class="ingredients-list">${ingredientsHTML}</ul>
                <div class="section-title">Method</div>
                <ol class="steps-list">${stepsHTML}</ol>
                <div class="chef-tip">${escapeHTML(r.tips)}</div>
            </div>
        </div>`;
    messagesEl.appendChild(msgEl);
}

// ── Suggestion chips ──────────────────────────────────────────
function appendSuggestions(suggestions) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg msg-bot';

    const itemsHTML = suggestions.map(s => `
        <div class="suggestion-item" onclick="sendQuick('I want ${escapeHTML(s.name)}')">
            <div class="suggestion-emoji">${s.emoji}</div>
            <div class="suggestion-info">
                <strong>${escapeHTML(s.name)}</strong>
                <span>⏱ ${escapeHTML(s.time)}</span>
            </div>
        </div>`).join('');

    wrapper.innerHTML = `
        <div class="bot-label">Chef Bot</div>
        <div class="suggestions-wrap">${itemsHTML}</div>`;
    messagesEl.appendChild(wrapper);
}

// ── Recipe list ───────────────────────────────────────────────
function appendList(items) {
    const wrapper = document.createElement('div');
    wrapper.className = 'msg msg-bot';

    const itemsHTML = items.map(i => `
        <div class="list-item">${renderMarkdownLight(i)}</div>`).join('');

    wrapper.innerHTML = `
        <div class="bot-label">Chef Bot</div>
        <div class="list-wrap">${itemsHTML}</div>`;
    messagesEl.appendChild(wrapper);
}

// ── Clear chat ────────────────────────────────────────────────
function clearChat() {
    messagesEl.innerHTML = '';
    sendToBot('hello');
}

// ── Helpers ───────────────────────────────────────────────────
function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHTML(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// Simple **bold** markdown support
function renderMarkdownLight(text) {
    return escapeHTML(text)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}
