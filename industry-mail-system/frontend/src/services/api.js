import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = {
    // Topics
    getTopics: async () => {
        const response = await axios.get(`${API_BASE_URL}/topics/`)
        return response.data
    },

    createTopic: async (topicData) => {
        const response = await axios.post(`${API_BASE_URL}/topics/`, topicData)
        return response.data
    },

    // Users
    getUsers: async () => {
        const response = await axios.get(`${API_BASE_URL}/users/`)
        return response.data
    },

    createUser: async (userData) => {
        const response = await axios.post(`${API_BASE_URL}/users/`, userData)
        return response.data
    },

    // Subscriptions
    getSubscriptions: async () => {
        const response = await axios.get(`${API_BASE_URL}/subscriptions/`)
        return response.data
    },

    getUserSubscriptions: async (userId) => {
        const response = await axios.get(`${API_BASE_URL}/subscriptions/user/${userId}`)
        return response.data
    },

    createSubscription: async (subscriptionData) => {
        const response = await axios.post(`${API_BASE_URL}/subscriptions/`, subscriptionData)
        return response.data
    },

    updateSubscription: async (subscriptionId, updateData) => {
        const response = await axios.put(`${API_BASE_URL}/subscriptions/${subscriptionId}`, updateData)
        return response.data
    },

    deleteSubscription: async (subscriptionId) => {
        const response = await axios.delete(`${API_BASE_URL}/subscriptions/${subscriptionId}`)
        return response.data
    },

    // News
    fetchNews: async (topic, days = 1) => {
        const response = await axios.get(`${API_BASE_URL}/news/fetch`, {
            params: { topic, days, limit: 10 }
        })
        return response.data
    },

    sendNewsletter: async (topicId, days) => {
        const response = await axios.post(`${API_BASE_URL}/news/send-newsletter`, {
            topic_id: topicId,
            days: days
        })
        return response.data
    }

}

export default api
