class ChatbotUI {
    constructor() {
        this.apiUrl = 'http://localhost:8000/api/v1';
        this.wsUrl = 'ws://localhost:8000/api/v1/chat';
        this.sessionId = null;
        this.ws = null;
        
        // Elementos del DOM
        this.userRoleSelect = document.getElementById('userRole');
        this.startSessionBtn = document.getElementById('startSession');
        this.messageInput = document.getElementById('messageInput');
        this.sendMessageBtn = document.getElementById('sendMessage');
        this.chatMessages = document.getElementById('chatMessages');
        this.contextDisplay = document.getElementById('contextDisplay');
        this.completionBars = document.getElementById('completionBars');
        
        // Bind de eventos
        this.startSessionBtn.addEventListener('click', () => this.startSession());
        this.sendMessageBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }
    
    async startSession() {
        try {
            const response = await fetch(`${this.apiUrl}/sessions`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_role: this.userRoleSelect.value
                })
            });
            
            if (!response.ok) throw new Error('Error al crear sesión');
            
            const data = await response.json();
            this.sessionId = data.session_id;
            
            // Iniciar WebSocket
            this.connectWebSocket();
            
            // Actualizar UI
            this.startSessionBtn.disabled = true;
            this.messageInput.disabled = false;
            this.sendMessageBtn.disabled = false;
            
            this.addMessage('Sistema', '¡Bienvenido! ¿En qué puedo ayudarte?', 'bot');
        } catch (error) {
            console.error('Error:', error);
            alert('Error al iniciar sesión');
        }
    }
    
    connectWebSocket() {
        this.ws = new WebSocket(`${this.wsUrl}/${this.sessionId}`);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.type === 'message') {
                this.addMessage('Bot', data.data.response, 'bot');
                this.updateContext(data.data.context);
                this.updateCompletionStatus(data.data.context.completion_status);
            } else if (data.type === 'error') {
                this.addMessage('Error', data.data.error, 'error');
            }
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket cerrado');
            this.sessionId = null;
            this.startSessionBtn.disabled = false;
            this.messageInput.disabled = true;
            this.sendMessageBtn.disabled = true;
        };
    }
    
    async sendMessage() {
        const text = this.messageInput.value.trim();
        if (!text || !this.ws) return;
        
        this.addMessage('Tú', text, 'user');
        this.messageInput.value = '';
        
        this.ws.send(JSON.stringify({
            text,
            timestamp: new Date().toISOString()
        }));
    }
    
    addMessage(sender, text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = `
            <strong>${sender}:</strong>
            <p>${text}</p>
        `;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    updateContext(context) {
        this.contextDisplay.textContent = JSON.stringify(context, null, 2);
    }
    
    updateCompletionStatus(completion) {
        this.completionBars.innerHTML = '';
        
        for (const [category, percentage] of Object.entries(completion)) {
            const barDiv = document.createElement('div');
            barDiv.className = 'progress-bar';
            barDiv.innerHTML = `
                <div class="progress-bar-fill" style="width: ${percentage * 100}%"></div>
                <div class="progress-label">${category}: ${Math.round(percentage * 100)}%</div>
            `;
            this.completionBars.appendChild(barDiv);
        }
    }
}

// Inicializar la UI cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new ChatbotUI();
}); 