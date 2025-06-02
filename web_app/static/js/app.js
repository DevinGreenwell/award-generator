// Main JavaScript for Coast Guard Award Writing Tool

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const generateBtn = document.getElementById('generateBtn');
    const exportBtn = document.getElementById('exportBtn');
    const printBtn = document.getElementById('printBtn');
    const newSessionBtn = document.getElementById('newSessionBtn');
    const saveSessionBtn = document.getElementById('saveSessionBtn');
    const loadSessionBtn = document.getElementById('loadSessionBtn');
    const sessionIdInput = document.getElementById('sessionIdInput');
    const awardContent = document.getElementById('awardContent');
    
    // Message template
    const messageTpl = document.getElementById('messageTpl');
    const awardTpl = document.getElementById('awardTpl');
    
    // Session ID
    let sessionId = '';
    
    // Initialize the chat with a welcome message
    initChat();
    
    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    generateBtn.addEventListener('click', generateRecommendation);
    exportBtn.addEventListener('click', exportRecommendation);
    printBtn.addEventListener('click', printRecommendation);
    
    newSessionBtn.addEventListener('click', newSession);
    saveSessionBtn.addEventListener('click', saveSession);
    loadSessionBtn.addEventListener('click', loadSession);
    
    // Functions
    function initChat() {
        // Clear chat
        chatMessages.innerHTML = '';
        
        // Add welcome message
        addMessage({
            role: 'assistant',
            content: 'Welcome to the Coast Guard Award Writing Tool! I\'ll help you gather information about a service member\'s accomplishments and recommend an appropriate award based on objective criteria from the Coast Guard manuals. Let\'s start by discussing the nominee\'s achievements. What would you like to tell me about them?',
            timestamp: new Date().toISOString()
        });
        
        // Reset award content
        awardContent.innerHTML = '<div class="placeholder-text"><p>Complete the chat conversation to receive an award recommendation.</p></div>';
        
        // Get session from server
        fetch('/api/session')
            .then(response => response.json())
            .then(data => {
                sessionId = data.session_id;
                
                // If there are messages, add them to the chat
                if (data.messages && data.messages.length > 0) {
                    chatMessages.innerHTML = ''; // Clear welcome message
                    data.messages.forEach(msg => addMessage(msg));
                }
                
                // If there's a recommendation, show it
                if (data.recommendation) {
                    displayAward(data.recommendation.award, data.recommendation.explanation);
                }
            })
            .catch(error => console.error('Error fetching session:', error));
    }
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage({
            role: 'user',
            content: message,
            timestamp: new Date().toISOString()
        });
        
        // Clear input
        userInput.value = '';
        
        // Send message to server
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => {
            // Add assistant message to chat
            addMessage({
                role: 'assistant',
                content: data.message,
                timestamp: new Date().toISOString()
            });
            
            // Update session ID if provided
            if (data.session_id) {
                sessionId = data.session_id;
                sessionIdInput.placeholder = `Session ID: ${sessionId.substring(0, 8)}...`;
            }
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Error sending message:', error);
            addMessage({
                role: 'assistant',
                content: 'Sorry, there was an error processing your message. Please try again.',
                timestamp: new Date().toISOString()
            });
        });
    }
    
    function addMessage(msg) {
        // Clone template
        const messageNode = messageTpl.content.cloneNode(true);
        const messageDiv = messageNode.querySelector('.message');
        const contentDiv = messageNode.querySelector('.message-content');
        const timeDiv = messageNode.querySelector('.message-time');
        
        // Add classes based on role
        messageDiv.classList.add(msg.role);
        
        // Set content
        contentDiv.innerHTML = msg.content;
        
        // Set time if available
        if (msg.timestamp) {
            const date = new Date(msg.timestamp);
            timeDiv.textContent = date.toLocaleTimeString();
        }
        
        // Add to chat
        chatMessages.appendChild(messageNode);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function generateRecommendation() {
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>Generating recommendation...</p></div>';
        
        // Request recommendation from server
        fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_id: sessionId })
        })
        .then(response => response.json())
        .then(data => {
            displayAward(data.award, data.explanation);
        })
        .catch(error => {
            console.error('Error generating recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>Error generating recommendation. Please try again.</p></div>';
        });
    }
    
    function displayAward(award, explanation) {
        // Clone template
        const awardNode = awardTpl.content.cloneNode(true);
        const titleEl = awardNode.querySelector('.award-title');
        const explanationEl = awardNode.querySelector('.award-explanation');
        
        // Set content
        titleEl.textContent = award;
        explanationEl.innerHTML = explanation;
        
        // Clear and add to award content
        awardContent.innerHTML = '';
        awardContent.appendChild(awardNode);
    }
    
    function exportRecommendation() {
        fetch('/api/export')
            .then(response => response.json())
            .then(data => {
                // Create a blob with the data
                const blob = new Blob([
                    `Award Recommendation: ${data.award}\n\n`,
                    `${data.explanation.replace(/<[^>]*>/g, '')}\n\n`,
                    `Generated: ${new Date(data.timestamp).toLocaleString()}\n`,
                    `Session ID: ${data.session_id}`
                ], { type: 'text/plain' });
                
                // Create download link
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `award-recommendation-${data.session_id.substring(0, 8)}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('Error exporting recommendation:', error);
                alert('Error exporting recommendation. Please try again.');
            });
    }
    
    function printRecommendation() {
        // Open print dialog
        window.print();
    }
    
    function newSession() {
        if (confirm('Start a new session? This will clear all current data.')) {
            // Clear session storage
            sessionStorage.removeItem('coastGuardAwardSession');
            
            // Reload page to start fresh
            window.location.reload();
        }
    }
    
    function saveSession() {
        fetch('/api/session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_id: sessionId })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Session saved! Your session ID is: ${data.session_id}`);
            sessionIdInput.value = data.session_id;
            
            // Also save to session storage as backup
            sessionStorage.setItem('coastGuardAwardSession', data.session_id);
        })
        .catch(error => {
            console.error('Error saving session:', error);
            alert('Error saving session. Please try again.');
        });
    }
    
    function loadSession() {
        const id = sessionIdInput.value.trim();
        if (!id) {
            alert('Please enter a session ID.');
            return;
        }
        
        fetch(`/api/session/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Session not found');
                }
                return response.json();
            })
            .then(data => {
                // Update session ID
                sessionId = data.session_id;
                
                // Clear chat
                chatMessages.innerHTML = '';
                
                // Add messages
                if (data.messages && data.messages.length > 0) {
                    data.messages.forEach(msg => addMessage(msg));
                }
                
                // Show recommendation if available
                if (data.recommendation) {
                    displayAward(data.recommendation.award, data.recommendation.explanation);
                } else {
                    awardContent.innerHTML = '<div class="placeholder-text"><p>Complete the chat conversation to receive an award recommendation.</p></div>';
                }
                
                alert('Session loaded successfully!');
            })
            .catch(error => {
                console.error('Error loading session:', error);
                alert('Error loading session. Please check the session ID and try again.');
            });
    }
    
    // Check for saved session in storage
    const savedSessionId = sessionStorage.getItem('coastGuardAwardSession');
    if (savedSessionId) {
        sessionIdInput.value = savedSessionId;
        // Optionally auto-load the session
        // loadSession();
    }
});
