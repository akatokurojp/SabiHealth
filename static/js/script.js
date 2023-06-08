const chatLog = document.getElementById('chat-log');
const userQueryInput = document.getElementById('user-query');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendUserQuery);

function sendUserQuery() {
    const userQuery = userQueryInput.value;
    if (userQuery.trim() !== '') {
        appendUserMessage(userQuery);
        userQueryInput.value = '';

        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_query: userQuery })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.bot_response;
            appendBotMessage(botResponse);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function appendUserMessage(message) {
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user-message';
    userMessageElement.textContent = 'User: ' + message;
    chatLog.appendChild(userMessageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}

function appendBotMessage(message) {
    const botMessageElement = document.createElement('div');
    botMessageElement.className = 'message bot-message';
    botMessageElement.textContent = 'Bot: ' + message;
    chatLog.appendChild(botMessageElement);
    chatLog.scrollTop = chatLog.scrollHeight;
}
