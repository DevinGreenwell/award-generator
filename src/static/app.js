// Main JavaScript for Coast Guard Award Writing Tool

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const generateBtn = document.getElementById('generateBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const improveBtn = document.getElementById('improveBtn');
    const finalizeBtn = document.getElementById('finalizeBtn');
    const exportBtn = document.getElementById('exportBtn');
    const clearSessionBtn = document.getElementById('clearSessionBtn');
    const printBtn = document.getElementById('printBtn');
    const newSessionBtn = document.getElementById('newSessionBtn');
    const saveSessionBtn = document.getElementById('saveSessionBtn');
    const loadSessionBtn = document.getElementById('loadSessionBtn');
    const sessionIdInput = document.getElementById('sessionIdInput');
    const sessionNameInput = document.getElementById('sessionNameInput');
    const awardContent = document.getElementById('awardContent');
    
    // Awardee info fields
    const awardeeName = document.getElementById('awardeeName');
    const awardeeRank = document.getElementById('awardeeRank');
    const dateRangeStart = document.getElementById('dateRangeStart');
    const dateRangeEnd = document.getElementById('dateRangeEnd');
    
    // Message template
    const messageTpl = document.getElementById('messageTpl');
    const awardTpl = document.getElementById('awardTpl');
    const finalAwardTpl = document.getElementById('finalAwardTpl');
    
    // Session ID and workflow state
    let sessionId = '';
    let sessionName = '';
    let workflowState = 'input'; // States: input, recommendation, improvement, finalized
    let currentAward = '';
    let achievementsAdded = false;
    
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
    refreshBtn.addEventListener('click', refreshRecommendation);
    improveBtn.addEventListener('click', improveRecommendation);
    finalizeBtn.addEventListener('click', finalizeAward);
    exportBtn.addEventListener('click', exportRecommendation);
    printBtn.addEventListener('click', printRecommendation);
    clearSessionBtn.addEventListener('click', clearSession);
    
    newSessionBtn.addEventListener('click', newSession);
    saveSessionBtn.addEventListener('click', saveSession);
    loadSessionBtn.addEventListener('click', loadSession);
    
    // Functions
    function clearSession() {
    if (confirm('Clear the current session? This will remove all messages and start fresh.')) {
        // Clear session storage
        sessionStorage.removeItem('coastGuardAwardSession');
        
        // Clear server-side session data
        fetch('/api/session/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reset the UI
                chatMessages.innerHTML = '';
                awardContent.innerHTML = '<div class="placeholder-text"><p>📝 <strong>How to use:</strong> First describe your achievements in the chat above, then click "Generate Recommendation"</p></div>';
                
                // Reset form fields
                awardeeName.value = '';
                awardeeRank.value = '';
                dateRangeStart.value = '';
                dateRangeEnd.value = '';
                userInput.value = '';
                
                // Reset state variables
                sessionId = '';
                sessionName = '';
                workflowState = 'input';
                currentAward = '';
                achievementsAdded = false;
                
                // Update UI
                updateWorkflowUI();
                
                // Add welcome message
                addMessage({
                    role: 'assistant',
                    content: 'Session cleared! Welcome to the Coast Guard Award Writing Tool! Please enter the accomplishments you would like to include in the award recommendation.',
                    timestamp: new Date().toISOString()
                });
                
                console.log('Session cleared successfully');
            } else {
                throw new Error(data.error || 'Failed to clear session');
            }
        })
        .catch(error => {
            console.error('Error clearing session:', error);
            // Still clear the frontend even if backend fails
            initChat();
        });
    }
}
    function initChat() {
        // Clear chat
        chatMessages.innerHTML = '';
        
        // Reset workflow state
        workflowState = 'input';
        achievementsAdded = false;
        updateWorkflowUI();
        
        // Add welcome message
        addMessage({
            role: 'assistant',
            content: 'Welcome to the Coast Guard Award Writing Tool! Please enter the accomplishments you would like to include in the award recommendation. When you\'re done, click "Generate Recommendation".',
            timestamp: new Date().toISOString()
        });
        
        // Reset award content
        awardContent.innerHTML = '<div class="placeholder-text"><p>📝 <strong>How to use:</strong> First describe your achievements in the chat above, then click "Generate Recommendation"</p></div>';
        
        // Get session from server
        fetch('/api/session')
            .then(response => response.json())
            .then(data => {
                sessionId = data.session_id;
                sessionName = data.session_name || '';
                
                // Update session name input
                if (sessionName) {
                    sessionNameInput.value = sessionName;
                } else {
                    sessionNameInput.value = 'Unnamed Session';
                }
                
                // Update awardee info if available
                if (data.awardee_info) {
                    awardeeName.value = data.awardee_info.name || '';
                    awardeeRank.value = data.awardee_info.rank || '';
                    dateRangeStart.value = data.awardee_info.date_start || '';
                    dateRangeEnd.value = data.awardee_info.date_end || '';
                }
                
                // If there are messages, add them to the chat
                if (data.messages && data.messages.length > 0) {
                    chatMessages.innerHTML = ''; // Clear welcome message
                    data.messages.forEach(msg => addMessage(msg));
                    achievementsAdded = true;
                    updateWorkflowUI();
                }
                
                // If there's a recommendation, show it
                if (data.recommendation) {
                    displayAward(data.recommendation.award, data.recommendation.explanation, data.recommendation.improvements);
                    currentAward = data.recommendation.award;
                    workflowState = 'recommendation';
                    updateWorkflowUI();
                }
                
                // If there's a finalized award, show it
                if (data.finalized_award) {
                    displayFinalAward(data.finalized_award.award, data.finalized_award.citation);
                    workflowState = 'finalized';
                    updateWorkflowUI();
                }
            })
            .catch(error => console.error('Error fetching session:', error));
    }
    
    function updateWorkflowUI() {
        // Update generate button based on achievements
        if (achievementsAdded) {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Recommendation';
            generateBtn.style.opacity = '1';
        } else {
            generateBtn.disabled = true;
            generateBtn.textContent = 'Add Achievements First';
            generateBtn.style.opacity = '0.6';
        }
        
        // Update UI based on current workflow state
        switch(workflowState) {
            case 'input':
                generateBtn.style.display = 'block';
                refreshBtn.style.display = 'none';
                improveBtn.style.display = 'none';
                finalizeBtn.style.display = 'none';
                break;
            case 'recommendation':
                generateBtn.style.display = 'none';
                refreshBtn.style.display = 'block';
                improveBtn.style.display = 'block';
                finalizeBtn.style.display = 'block';
                break;
            case 'improvement':
                generateBtn.style.display = 'none';
                refreshBtn.style.display = 'block';
                improveBtn.style.display = 'block';
                finalizeBtn.style.display = 'block';
                break;
            case 'finalized':
                generateBtn.style.display = 'none';
                refreshBtn.style.display = 'block'; // Allow refreshing even after finalization
                improveBtn.style.display = 'none';
                finalizeBtn.style.display = 'none';
                break;
        }
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
            body: JSON.stringify({ 
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add assistant message to chat
                addMessage({
                    role: 'assistant',
                    content: data.response,
                    timestamp: new Date().toISOString()
                });
                
                // Mark achievements as added
                achievementsAdded = true;
                updateWorkflowUI();
                
                console.log(`Total messages: ${data.message_count || 'unknown'}`);
            } else {
                throw new Error(data.error || 'Unknown error');
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
    
    function displayMessage(message, type = 'info') {
        addMessage({
            role: 'assistant',
            content: `<div class="message-${type}">${message}</div>`,
            timestamp: new Date().toISOString()
        });
    }
    
    function generateRecommendation() {
        if (!achievementsAdded) {
            displayMessage('Please add some achievements first by describing them in the chat above.', 'error');
            return;
        }
        
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>🔄 Generating recommendation...</p></div>';
        
        // Request recommendation from server
        fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                awardee_info: awardeeInfo
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to generate recommendation');
                });
            }
            return response.json();
        })
        .then(data => {
            
            if (data.success) {
                displayAward(data.award, data.explanation, data.scores);
                currentAward = data.award;
                
                // Update workflow state
                workflowState = 'recommendation';
                updateWorkflowUI();
                
                // Add system message to chat
                addMessage({
                    role: 'assistant',
                    content: `Based on the information provided, I recommend a <strong>${data.award}</strong>. You can refresh this recommendation, improve it, or finalize it to generate the award citation.`,
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error generating recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>❌ Error generating recommendation. Please try again.</p></div>';
            displayMessage(error.message || 'Error generating recommendation. Please try again.', 'error');
        });
    }
    
    function refreshRecommendation() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>🔄 Refreshing recommendation...</p></div>';
        
        // Just call the regular recommend endpoint - it re-analyzes everything
        fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                awardee_info: awardeeInfo
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to refresh recommendation');
                });
            }
            return response.json();
        })
        .then(data => {
            
            if (data.success) {
                displayAward(data.award, data.explanation, data.scores);
                currentAward = data.award;
                
                // Update workflow state to recommendation (even if we were in finalized state)
                workflowState = 'recommendation';
                updateWorkflowUI();
                
                // Add system message to chat
                addMessage({
                    role: 'assistant',
                    content: `I've refreshed the recommendation. Now recommending a <strong>${data.award}</strong>. You can refresh again, improve it, or finalize it to generate the award citation.`,
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error refreshing recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>❌ Error refreshing recommendation. Please try again.</p></div>';
            displayMessage(error.message || 'Error refreshing recommendation. Please try again.', 'error');
        });
    }
    
    function improveRecommendation() {
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>🔄 Improving recommendation...</p></div>';
        
        // Request improved recommendation from server
        fetch('/api/improve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                current_award: currentAward
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to improve recommendation');
                });
            }
            return response.json();
        })
        .then(data => {
            
            if (data.success) {
                // Display improvement suggestions
                displayImprovements(data.suggestions, data.current_award);
                
                // Update workflow state
                workflowState = 'improvement';
                updateWorkflowUI();
                
                // Add system message to chat
                addMessage({
                    role: 'assistant',
                    content: 'I\'ve analyzed your achievements and provided improvement suggestions. You can add more details based on these suggestions and then refresh the recommendation.',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error improving recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>❌ Error improving recommendation. Please try again.</p></div>';
            displayMessage(error.message || 'Error improving recommendation. Please try again.', 'error');
        });
    }
    
    function finalizeAward() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>🔄 Generating final award citation...</p></div>';
        
        // Request finalized award from server
        fetch('/api/finalize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                award: currentAward,
                awardee_info: awardeeInfo
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to finalize award');
                });
            }
            return response.json();
        })
        .then(data => {
            
            if (data.success) {
                displayFinalAward(data.award, data.citation);
                
                // Update workflow state
                workflowState = 'finalized';
                updateWorkflowUI();
                
                // Add system message to chat
                addMessage({
                    role: 'assistant',
                    content: 'I\'ve generated the final award citation. You can export or print it using the buttons below. If you\'d like to make changes, you can click "Refresh Recommendation" to start over.',
                    timestamp: new Date().toISOString()
                });
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error finalizing award:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>❌ Error generating final award citation. Please try again.</p></div>';
            displayMessage(error.message || 'Error finalizing award. Please try again.', 'error');
        });
    }
    
    function displayAward(award, explanation, scores) {
        // Clone template
        const awardNode = awardTpl.content.cloneNode(true);
        const titleEl = awardNode.querySelector('.award-title');
        const explanationEl = awardNode.querySelector('.award-explanation');
        const scoresEl = awardNode.querySelector('.award-scores');
        
        // Set content
        titleEl.textContent = award;
        explanationEl.innerHTML = explanation;
        
        // Add scores if available
        if (scores) {
            let scoresHtml = '<h4>Scoring Breakdown:</h4><div class="scores-grid">';
            for (const [criterion, score] of Object.entries(scores)) {
                if (criterion !== 'total_weighted') {
                    scoresHtml += `<div class="score-item"><span class="criterion">${criterion}:</span> <span class="score">${score}/5</span></div>`;
                }
            }
            scoresHtml += `<div class="score-total"><strong>Total Weighted Score: ${scores.total_weighted || 0}</strong></div>`;
            scoresHtml += '</div>';
            scoresEl.innerHTML = scoresHtml;
        } else {
            scoresEl.style.display = 'none';
        }
        
        // Clear and add to award content
        awardContent.innerHTML = '';
        awardContent.appendChild(awardNode);
    }
    
    function displayImprovements(suggestions, award) {
        let html = `<div class="improvement-suggestions">`;
        html += `<h3>Current Recommendation: ${award}</h3>`;
        html += `<h4>💡 Ways to Improve This Recommendation:</h4>`;
        html += `<ul>`;
        suggestions.forEach(suggestion => {
            html += `<li>${suggestion}</li>`;
        });
        html += `</ul>`;
        html += `<p><strong>Next steps:</strong> Add more details based on these suggestions in the chat above, then click "Refresh Recommendation" to see if you can get a higher award.</p>`;
        html += `</div>`;
        
        awardContent.innerHTML = html;
    }
    
    function displayFinalAward(award, citation) {
        // Clone template
        const awardNode = finalAwardTpl.content.cloneNode(true);
        const titleEl = awardNode.querySelector('.award-title');
        const citationEl = awardNode.querySelector('.award-citation');
        
        // Set content
        titleEl.textContent = award;
        citationEl.innerHTML = citation;
        
        // Clear and add to award content
        awardContent.innerHTML = '';
        awardContent.appendChild(awardNode);
    }
    
    function exportRecommendation() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value
        };
        
        fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
            // Create a blob with the data
            let content = '';
            
            if (workflowState === 'finalized' && data.citation) {
                content = `AWARD CITATION: ${data.award}\n\n`;
                content += `AWARDEE: ${awardeeInfo.rank} ${awardeeInfo.name}\n`;
                content += `DATE RANGE: ${formatDate(awardeeInfo.date_start)} to ${formatDate(awardeeInfo.date_end)}\n\n`;
                content += `${data.citation.replace(/<[^>]*>/g, '')}\n\n`;
            } else {
                content = `AWARD RECOMMENDATION: ${data.award}\n\n`;
                content += `AWARDEE: ${awardeeInfo.rank} ${awardeeInfo.name}\n`;
                content += `DATE RANGE: ${formatDate(awardeeInfo.date_start)} to ${formatDate(awardeeInfo.date_end)}\n\n`;
                content += `${data.explanation.replace(/<[^>]*>/g, '')}\n\n`;
            }
            
            content += `Generated: ${new Date().toLocaleString()}\n`;
            content += `Session: ${sessionNameInput.value || 'Unnamed Session'}`;
            
            const blob = new Blob([content], { type: 'text/plain' });
            
            // Create download link
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${sessionNameInput.value || 'award'}-${new Date().toISOString().slice(0,10)}.txt`;
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
    
    function formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
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
        // Get session name from input
        const name = sessionNameInput.value.trim() || 'Unnamed Session';
        
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value
        };
        
        fetch('/api/session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                session_id: sessionId,
                session_name: name,
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Session "${name}" saved successfully!`);
            sessionId = data.session_id;
            
            // Also save to session storage as backup
            sessionStorage.setItem('coastGuardAwardSession', JSON.stringify({
                id: data.session_id,
                name: name
            }));
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
                // Update session ID and name
                sessionId = data.session_id;
                sessionName = data.session_name || 'Unnamed Session';
                sessionNameInput.value = sessionName;
                
                // Update awardee info if available
                if (data.awardee_info) {
                    awardeeName.value = data.awardee_info.name || '';
                    awardeeRank.value = data.awardee_info.rank || '';
                    dateRangeStart.value = data.awardee_info.date_start || '';
                    dateRangeEnd.value = data.awardee_info.date_end || '';
                }
                
                // Clear chat
                chatMessages.innerHTML = '';
                
                // Add messages
                if (data.messages && data.messages.length > 0) {
                    data.messages.forEach(msg => addMessage(msg));
                    achievementsAdded = true;
                }
                
                // Show recommendation or finalized award if available
                if (data.finalized_award) {
                    displayFinalAward(data.finalized_award.award, data.finalized_award.citation);
                    workflowState = 'finalized';
                } else if (data.recommendation) {
                    displayAward(data.recommendation.award, data.recommendation.explanation, data.recommendation.scores);
                    currentAward = data.recommendation.award;
                    workflowState = 'recommendation';
                } else {
                    awardContent.innerHTML = '<div class="placeholder-text"><p>📝 <strong>How to use:</strong> First describe your achievements in the chat above, then click "Generate Recommendation"</p></div>';
                    workflowState = 'input';
                    achievementsAdded = false;
                }
                
                updateWorkflowUI();
                alert(`Session "${sessionName}" loaded successfully!`);
            })
            .catch(error => {
                console.error('Error loading session:', error);
                alert('Error loading session. Please check the session ID and try again.');
            });
    }
    
    // Check for saved session in storage
    const savedSession = sessionStorage.getItem('coastGuardAwardSession');
    if (savedSession) {
        try {
            const session = JSON.parse(savedSession);
            sessionIdInput.value = session.id;
            // Optionally auto-load the session
            // loadSession();
        } catch (e) {
            console.error('Error parsing saved session:', e);
        }
    }
});