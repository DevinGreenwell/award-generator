/**
 * API communication module for Coast Guard Award Generator
 */

const API = {
    /**
     * Base configuration for API calls
     */
    config: {
        headers: {
            'Content-Type': 'application/json'
        }
    },

    /**
     * Handle API errors consistently
     */
    handleError: function(error, context) {
        console.error(`API Error in ${context}:`, error);
        throw new Error(`Failed to ${context}. Please try again.`);
    },

    /**
     * Make a POST request to the API
     */
    post: async function(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: this.config.headers,
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    },

    /**
     * Make a GET request to the API
     */
    get: async function(endpoint) {
        try {
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: this.config.headers
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    },

    // Specific API methods

    /**
     * Send a chat message
     */
    sendMessage: async function(message) {
        return this.post('/api/chat', { message });
    },

    /**
     * Generate award recommendation
     */
    generateRecommendation: async function(awardeeInfo) {
        return this.post('/api/recommend', { awardee_info: awardeeInfo });
    },

    /**
     * Refresh recommendation
     */
    refreshRecommendation: async function(awardeeInfo) {
        return this.post('/api/refresh', { awardee_info: awardeeInfo });
    },

    /**
     * Get improvement suggestions
     */
    getImprovements: async function(currentAward) {
        return this.post('/api/improve', { current_award: currentAward });
    },

    /**
     * Finalize award citation
     */
    finalizeAward: async function(award) {
        return this.post('/api/finalize', { award });
    },

    /**
     * Export award package
     */
    exportPackage: async function(format, awardeeInfo) {
        return this.post('/api/export', { 
            format: format,
            awardee_info: awardeeInfo 
        });
    },

    /**
     * Clear session
     */
    clearSession: async function() {
        return this.post('/api/session/clear', {});
    },

    /**
     * Get session data
     */
    getSession: async function() {
        return this.get('/api/session');
    },

    /**
     * Save session data
     */
    saveSession: async function(sessionData) {
        return this.post('/api/session', sessionData);
    }
};