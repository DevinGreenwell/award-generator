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
    const printBtn = document.getElementById('printBtn');
    const clearSessionBtn = document.getElementById('clearSessionBtn');
    const newSessionBtn = document.getElementById('newSessionBtn');
    const saveSessionBtn = document.getElementById('saveSessionBtn');
    const loadSessionBtn = document.getElementById('loadSessionBtn');
    const sessionIdInput = document.getElementById('sessionIdInput');
    const sessionNameInput = document.getElementById('sessionNameInput');
    const awardContent = document.getElementById('awardContent');
    const uploadBtn = document.getElementById('uploadBtn');
    const fileInput = document.getElementById('fileInput');
    
    // Awardee info fields
    const awardeeName = document.getElementById('awardeeName');
    const awardeeRank = document.getElementById('awardeeRank');
    const awardeeUnit = document.getElementById('awardeeUnit');
    const dateRangeStart = document.getElementById('dateRangeStart');
    const dateRangeEnd = document.getElementById('dateRangeEnd');
    const operationalDevice = document.getElementById('operationalDevice');
    
    // Message template
    const messageTpl = document.getElementById('messageTpl');
    const awardTpl = document.getElementById('awardTpl');
    const finalAwardTpl = document.getElementById('finalAwardTpl');
    
    // Session ID and workflow state
    let sessionId = '';
    let sessionName = '';
    let workflowState = 'input'; // States: input, recommendation, improvement, finalized
    let currentAward = '';
    
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
    
    // File upload event listeners
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileUpload);
    
    generateBtn.addEventListener('click', generateRecommendation);
    refreshBtn.addEventListener('click', refreshRecommendation);
    improveBtn.addEventListener('click', improveRecommendation);
    finalizeBtn.addEventListener('click', finalizeAward);
    exportBtn.addEventListener('click', exportRecommendation);
    printBtn.addEventListener('click', printRecommendation);
    
    // Session management event listeners
    if (clearSessionBtn) {
        clearSessionBtn.addEventListener('click', clearSession);
    }
    if (newSessionBtn) {
        newSessionBtn.addEventListener('click', newSession);
    }
    if (saveSessionBtn) {
        saveSessionBtn.addEventListener('click', saveSession);
    }
    if (loadSessionBtn) {
        loadSessionBtn.addEventListener('click', loadSession);
    }
    
    // Functions
    function initChat() {
        // Clear chat
        chatMessages.innerHTML = '';
        
        // Reset workflow state
        workflowState = 'input';
        updateWorkflowUI();
        
        // Add welcome message
        addMessage({
            role: 'assistant',
            content: 'Welcome to the Coast Guard Award Writing Tool! Please enter the accomplishments you would like to include in the award recommendation. When you\'re done, click "Generate Recommendation".',
            timestamp: new Date().toISOString()
        });
        
        // Reset award content
        awardContent.innerHTML = '<div class="placeholder-text"><p>Enter accomplishments in the chat and click "Generate Recommendation" when ready.</p></div>';
        
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
    
    function handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        // Check file type
        const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
            alert('Please upload a PDF or Word document');
            fileInput.value = '';
            return;
        }
        
        // Check file size (max 10MB)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            alert('File size must be less than 10MB');
            fileInput.value = '';
            return;
        }
        
        // Show uploading message
        const uploadMsg = {
            role: 'user',
            content: `📎 Uploading ${file.name}...`,
            timestamp: new Date().toISOString(),
            isFileUpload: true
        };
        addMessage(uploadMsg);
        
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        
        // Upload file
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add success message with extracted content
                addMessage({
                    role: 'assistant',
                    content: data.message,
                    timestamp: new Date().toISOString()
                });
                
                // If content was extracted, add it to the conversation
                if (data.extracted_text) {
                    // Send the extracted text as a message
                    userInput.value = data.extracted_text;
                    sendMessage();
                }
            } else {
                addMessage({
                    role: 'assistant',
                    content: `Error: ${data.error}`,
                    timestamp: new Date().toISOString()
                });
            }
            
            // Clear file input
            fileInput.value = '';
        })
        .catch(error => {
            console.error('Upload error:', error);
            addMessage({
                role: 'assistant',
                content: 'Error uploading file. Please try again.',
                timestamp: new Date().toISOString()
            });
            fileInput.value = '';
        });
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
                message,
                workflow_state: workflowState
            })
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
        
        // Add file upload class if applicable
        if (msg.isFileUpload) {
            messageDiv.classList.add('file-upload');
        }
        
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
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>Generating recommendation...</p></div>';
        
        // Request recommendation from server
        fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                session_id: sessionId,
                session_name: sessionNameInput.value,
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
            displayAward(data.award, data.explanation, data.improvements);
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
        })
        .catch(error => {
            console.error('Error generating recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>Error generating recommendation. Please try again.</p></div>';
        });
    }
    
    function refreshRecommendation() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>Refreshing recommendation...</p></div>';
        
        // Request a fresh recommendation from server
        fetch('/api/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                session_id: sessionId,
                session_name: sessionNameInput.value,
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
            displayAward(data.award, data.explanation, data.improvements);
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
        })
        .catch(error => {
            console.error('Error refreshing recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>Error refreshing recommendation. Please try again.</p></div>';
        });
    }
    
    function improveRecommendation() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>Improving recommendation...</p></div>';
        
        // Request improved recommendation from server
        fetch('/api/improve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                session_id: sessionId,
                award: currentAward,
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
            displayAward(data.award, data.explanation, data.improvements);
            currentAward = data.award;
            
            // Update workflow state
            workflowState = 'improvement';
            updateWorkflowUI();
            
            // Add system message to chat
            addMessage({
                role: 'assistant',
                content: 'I\'ve improved the recommendation based on the information provided. You can continue to improve it, refresh for a new recommendation, or finalize it to generate the award citation.',
                timestamp: new Date().toISOString()
            });
        })
        .catch(error => {
            console.error('Error improving recommendation:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>Error improving recommendation. Please try again.</p></div>';
        });
    }
    
    function finalizeAward() {
        // Get awardee info
        const awardeeInfo = {
            name: awardeeName.value,
            rank: awardeeRank.value,
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
        };
        
        // Show loading state
        awardContent.innerHTML = '<div class="placeholder-text"><p>Generating final award citation...</p></div>';
        
        // Request finalized award from server
        fetch('/api/finalize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                session_id: sessionId,
                award: currentAward,
                awardee_info: awardeeInfo
            })
        })
        .then(response => response.json())
        .then(data => {
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
        })
        .catch(error => {
            console.error('Error finalizing award:', error);
            awardContent.innerHTML = '<div class="placeholder-text"><p>Error generating final award citation. Please try again.</p></div>';
        });
    }
    
    function displayAward(award, explanation, improvements) {
        // Clone template
        const awardNode = awardTpl.content.cloneNode(true);
        const titleEl = awardNode.querySelector('.award-title');
        const explanationEl = awardNode.querySelector('.award-explanation');
        const improvementsEl = awardNode.querySelector('.improvement-suggestions');
        
        // Set content
        titleEl.textContent = award;
        explanationEl.innerHTML = explanation;
        
        // Add improvement suggestions if available
        if (improvements && improvements.length > 0) {
            let improvementHtml = '<h4>Ways to Improve This Recommendation:</h4><ul>';
            improvements.forEach(improvement => {
                improvementHtml += `<li>${improvement}</li>`;
            });
            improvementHtml += '</ul>';
            improvementsEl.innerHTML = improvementHtml;
        } else {
            improvementsEl.style.display = 'none';
        }
        
        // Clear and add to award content
        awardContent.innerHTML = '';
        awardContent.appendChild(awardNode);
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
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
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
    
    function clearSession() {
        if (confirm('Clear all current data? This will reset the conversation and recommendations.')) {
            fetch('/api/session/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reset local state
                    sessionId = '';
                    sessionName = '';
                    workflowState = 'input';
                    currentAward = '';
                    
                    // Clear form fields
                    awardeeName.value = '';
                    awardeeRank.value = '';
                    if (awardeeUnit) awardeeUnit.value = '';
                    dateRangeStart.value = '';
                    dateRangeEnd.value = '';
                    if (operationalDevice) operationalDevice.checked = false;
                    
                    // Reinitialize chat
                    initChat();
                    
                    // Show success message
                    addMessage({
                        role: 'assistant',
                        content: 'Session cleared successfully. You can start fresh with new achievements.',
                        timestamp: new Date().toISOString()
                    });
                } else {
                    alert('Error clearing session. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error clearing session:', error);
                alert('Error clearing session. Please try again.');
            });
        }
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
            unit: awardeeUnit.value,
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice.checked
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
                }
                
                // Show recommendation or finalized award if available
                if (data.finalized_award) {
                    displayFinalAward(data.finalized_award.award, data.finalized_award.citation);
                    workflowState = 'finalized';
                } else if (data.recommendation) {
                    displayAward(data.recommendation.award, data.recommendation.explanation, data.recommendation.improvements);
                    currentAward = data.recommendation.award;
                    workflowState = 'recommendation';
                } else {
                    awardContent.innerHTML = '<div class="placeholder-text"><p>Enter accomplishments in the chat and click "Generate Recommendation" when ready.</p></div>';
                    workflowState = 'input';
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
