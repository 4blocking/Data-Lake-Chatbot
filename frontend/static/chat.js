document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chat-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    let isAIThinking = false;

    messageInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        sendButton.disabled = this.value.trim() === '' || isAIThinking;
    });

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const avatar = document.createElement('div');
        avatar.className = isUser ? 'avatar user-avatar' : 'avatar bot-avatar';
        avatar.textContent = isUser ? 'You' : 'AI';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);

        if (isUser) {
            contentDiv.textContent = content;
        }

        scrollToBottom();
        return contentDiv;
    }

    function showThinkingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';

    const avatar = document.createElement('div');
    avatar.className = 'avatar bot-avatar';
    avatar.textContent = 'DL';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';

    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'thinking-indicator';

    const spinner = document.createElement('div');
    spinner.className = 'spinner';

    const text = document.createElement('div');
    text.className = 'thinking-text';
    text.textContent = 'AI is thinking...';

    thinkingDiv.appendChild(spinner);
    thinkingDiv.appendChild(text);
    contentDiv.appendChild(thinkingDiv);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    scrollToBottom();
    return messageDiv;
}


    async function getAIResponse(userMessage) {
        const token = localStorage.getItem('access_token');
        if (!token) throw new Error("Not authenticated");

        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ query: userMessage })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to fetch response.");
        }

        const data = await response.json();
        return data.response;
    }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (message === '' || isAIThinking) return;


            hasSentFirstMessage = true;

            addMessage(message, true);
            messageInput.value = '';
            messageInput.style.height = 'auto';
            sendButton.disabled = true;
            isAIThinking = true;

            const thinkingIndicator = showThinkingIndicator();

            try {
                const aiResponse = await getAIResponse(message);
                const aiMessageElement = addMessage('', false);
                thinkingIndicator.remove();

                let formatted = '';

                if (typeof aiResponse === 'object' && Array.isArray(aiResponse.sources)) {
                    if (aiResponse.sources.length === 0) {
                        formatted = `
                            <div class="response-card">No data sources found for your query.Try rephrasing or asking about a different domain</div>
                        `;
                    } else {
                        formatted = `
                            <div class="response-card">
                                ${aiResponse.sources.map(src => `
                                    <div class="entry">
                                        <div class="path">Path: ${src.path}</div>
                                        <div class="reason">Reason: ${src.reason}</div>
                                    </div>
                                `).join('')}
                            </div>
                        `;
                    }
                } else {
                    formatted = `<div class="response-card">${aiResponse}</div>`;
                }

                aiMessageElement.innerHTML = formatted;
            } catch (error) {
                console.error('AI error:', error);
                const aiMessageElement = addMessage("Error: " + error.message, false);
                thinkingIndicator.remove();
            } finally {
                isAIThinking = false;
                sendButton.disabled = messageInput.value.trim() === '';
            }
        }


    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    let hasSentFirstMessage = false;

    async function loadChatHistory() {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        try {
            const response = await fetch("/api/history", {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error("Failed to fetch history");

            const data = await response.json();

            for (const item of data.history) {
                const userMsg = item.message || item.message_text;
                const responseText = item.response || item.response_text;

                // Add user message
                addMessage(userMsg, true);

                // Format LLM response
                let formatted = '';
                try {
                    const parsed = typeof responseText === 'string' ? JSON.parse(responseText) : responseText;

                    if (parsed.sources && Array.isArray(parsed.sources)) {
                        if (parsed.sources.length === 0) {
                            formatted = `
                            <div class="response-card">No data sources found for your query.Try rephrasing or asking about a different domain</div>
                        `;
                        } else {
                            formatted = `
                                <div class="response-card">
                                    ${parsed.sources.map(src => `
                                        <div class="entry">
                                            <div class="path">Path: ${src.path}</div>
                                            <div class="reason">Reason: ${src.reason}</div>
                                        </div>
                                    `).join('')}
                                </div>
                            `;
                        }
                    } else {
                        formatted = `<div class="response-card">${responseText}</div>`;
                    }
                } catch (e) {
                    formatted = `<div class="response-card">${responseText}</div>`;
                }

                const aiMessageElement = addMessage('', false);
                aiMessageElement.innerHTML = formatted;
            }
        } catch (err) {
            console.error("Failed to load chat history:", err);
        }
    }


    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    if (!hasSentFirstMessage) {
        loadChatHistory();
    }
    scrollToBottom();
    document.getElementById('logout-button').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    });
});
