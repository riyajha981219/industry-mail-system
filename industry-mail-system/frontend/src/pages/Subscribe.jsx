import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import TopicCard from '../components/TopicCard'
import './Subscribe.css'

const Subscribe = () => {
    const [topics, setTopics] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [formData, setFormData] = useState({
        email: '',
        fullName: '',
        selectedTopic: null,
        frequency: '1'
    })
    const [showForm, setShowForm] = useState(false)
    const [success, setSuccess] = useState('')
    const [user, setUser] = useState(null)
    const [userSubscriptions, setUserSubscriptions] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        const stored = localStorage.getItem('ims_user')
        if (stored) {
            try {
                const u = JSON.parse(stored)
                setUser(u)
                setFormData(fd => ({ ...fd, email: u.email || '', fullName: u.full_name || u.fullName || '' }))
            } catch (e) {
                // ignore parse errors
            }
        }
        fetchTopics()
    }, [])

    useEffect(() => {
        if (user?.id) fetchUserSubscriptions(user.id)
    }, [user])

    const fetchTopics = async () => {
        setLoading(true)
        try {
            const data = await api.getTopics()
            setTopics(data)
        } catch (err) {
            setError('Failed to load topics')
        } finally {
            setLoading(false)
        }
    }

    const fetchUserSubscriptions = async (userId) => {
        try {
            const subs = await api.getUserSubscriptions(userId)
            setUserSubscriptions(subs || [])
        } catch (err) {
            console.warn('Failed to load subscriptions', err)
        }
    }

    const handleTopicSelect = (topic) => {
        setFormData({ ...formData, selectedTopic: topic })
        setShowForm(true)
    }

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setSuccess('')

        try {
            let currentUser = user
            if (!currentUser) {
                currentUser = await api.createUser({
                    email: formData.email,
                    full_name: formData.fullName
                })
                setUser(currentUser)
                try { localStorage.setItem('ims_user', JSON.stringify(currentUser)) } catch (e) { }
            }

            // prevent duplicate subscriptions
            const already = userSubscriptions.find(s => s.topic_id === formData.selectedTopic.id)
            if (already) {
                alert('Already subscribed')
                return
            }

            await api.createSubscription({
                user_id: currentUser.id,
                topic_id: formData.selectedTopic.id,
                frequency: formData.frequency
            })

            setSuccess('Subscription created successfully!')
            fetchUserSubscriptions(currentUser.id)
            setTimeout(() => navigate('/dashboard'), 1500)
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create subscription')
        }
    }

    const handleSignOut = () => {
        localStorage.removeItem('ims_user')
        setUser(null)
        setFormData(fd => ({ ...fd, email: '', fullName: '' }))
        setUserSubscriptions([])
    }

    if (loading) return <div className="container"><div className="loading">Loading topics...</div></div>

    return (
        <div className="container">
            <div className="subscribe-header">
                <h1>Subscribe to Industry News</h1>
                <p>Select a topic to start receiving curated news updates</p>
                <div style={{ marginTop: 12 }}>
                    {formData.email ? (
                        <button className="btn" onClick={handleSignOut}>Sign out</button>
                    ) : (
                        <div style={{ color: '#666' }}>Enter your email when subscribing</div>
                    )}
                </div>
            </div>

            {!showForm ? (
                <div className="grid">
                    {topics.map(topic => (
                        <TopicCard
                            key={topic.id}
                            topic={topic}
                            onSubscribe={handleTopicSelect}
                            isSubscribed={!!userSubscriptions.find(s => s.topic_id === topic.id)}
                        />
                    ))}
                </div>
            ) : (
                <div className="subscription-form-container">
                    <div className="card">
                        <h2>Complete Your Subscription</h2>
                        <p className="selected-topic">Selected Topic: <strong>{formData.selectedTopic.name}</strong></p>

                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="fullName">Full Name</label>
                                <input type="text" id="fullName" name="fullName" value={formData.fullName} onChange={handleInputChange} required placeholder="Enter your full name" />
                            </div>

                            <div className="form-group">
                                <label htmlFor="email">Email Address</label>
                                <input type="email" id="email" name="email" value={formData.email} onChange={handleInputChange} required placeholder="your.email@example.com" />
                            </div>

                            <div className="form-group">
                                <label htmlFor="frequency">Newsletter Frequency</label>
                                <select id="frequency" name="frequency" value={formData.frequency} onChange={handleInputChange} required>
                                    <option value="1">Daily (Every 1 day)</option>
                                    <option value="7">Weekly (Every 7 days)</option>
                                    <option value="30">Monthly (Every 30 days)</option>
                                </select>
                            </div>

                            {error && <div className="error">{error}</div>}
                            {success && <div className="success">{success}</div>}

                            <div className="form-actions">
                                <button type="button" className="btn" onClick={() => setShowForm(false)}>Back to Topics</button>
                                <button type="submit" className="btn btn-primary">Subscribe Now</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Subscribe
