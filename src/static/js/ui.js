/**
 * UI management module for Coast Guard Award Generator
 */

const UI = {
    /**
     * Display a message in the chat
     */
    addMessage: function(msg, chatMessages, messageTpl) {
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
    },

    /**
     * Display award recommendation
     */
    displayAward: function(award, explanation, improvements, awardContent, awardTpl) {
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
    },

    /**
     * Display final award citation
     */
    displayFinalAward: function(award, citation, awardContent, finalAwardTpl) {
        const awardNode = finalAwardTpl.content.cloneNode(true);
        const titleEl = awardNode.querySelector('.award-title');
        const citationEl = awardNode.querySelector('.award-citation');
        
        // Set content
        titleEl.textContent = award;
        citationEl.innerHTML = citation;
        
        // Clear and add to award content
        awardContent.innerHTML = '';
        awardContent.appendChild(awardNode);
    },

    /**
     * Update workflow UI based on state
     */
    updateWorkflowUI: function(state, buttons) {
        const { generateBtn, refreshBtn, improveBtn, finalizeBtn } = buttons;
        
        switch(state) {
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
                refreshBtn.style.display = 'block';
                improveBtn.style.display = 'none';
                finalizeBtn.style.display = 'none';
                break;
        }
    },

    /**
     * Show loading state
     */
    showLoading: function(element, message = 'Loading...') {
        element.innerHTML = `<div class="placeholder-text"><p>${message}</p></div>`;
    },

    /**
     * Show error message
     */
    showError: function(element, error) {
        element.innerHTML = `<div class="placeholder-text error"><p>Error: ${error}</p></div>`;
    },

    /**
     * Get awardee info from form
     */
    getAwardeeInfo: function(fields) {
        const { awardeeName, awardeeRank, awardeeUnit, dateRangeStart, dateRangeEnd, operationalDevice } = fields;
        
        return {
            name: awardeeName.value,
            rank: awardeeRank.value,
            unit: awardeeUnit ? awardeeUnit.value : '',
            date_start: dateRangeStart.value,
            date_end: dateRangeEnd.value,
            operational_device: operationalDevice ? operationalDevice.checked : false
        };
    },

    /**
     * Clear form fields
     */
    clearFormFields: function(fields) {
        Object.values(fields).forEach(field => {
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = false;
                } else if (field.value !== undefined) {
                    field.value = '';
                }
            }
        });
    },

    /**
     * Format date for display
     */
    formatDate: function(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }
};