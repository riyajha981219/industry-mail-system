import { useState } from 'react'
import './TopicCard.css'
import api from '../services/api'

const TopicCard = ({ topic, onSubscribe, isSubscribed = false }) => {
    const [sending, setSending] = useState(false)

    const handleSendNow = async (e, days) => {
        e.stopPropagation()
        if (!confirm(`Send newsletter for "${topic.name}" now?`)) return
        try {
            setSending(true)
            const res = await api.sendNewsletter(topic.id, days)
            alert(res.message || 'Scheduled newsletter send')
        } catch (err) {
            alert(err.response?.data?.detail || 'Failed to trigger newsletter')
        } finally {
            setSending(false)
        }
    }

    return (
        <div className="topic-card">
            <h3>{topic.name}</h3>
            <p className="description">{topic.description}</p>
            <div className="keywords">
                {topic.keywords.split(',').map((keyword, idx) => (
                    <span key={idx} className="keyword-tag">{keyword.trim()}</span>
                ))}
            </div>
            <div className="topic-actions">
                {isSubscribed ? (
                    <button className="btn" disabled>Subscribed!</button>
                ) : (
                    <button
                        className="btn btn-primary"
                        onClick={() => onSubscribe(topic)}
                    >
                        Subscribe
                    </button>
                )}

                <button
                    className="btn btn-secondary"
                    onClick={(e) => handleSendNow(e, 1)}
                    disabled={sending}
                >
                    {sending ? 'Sending…' : 'Send Now (1d)'}
                </button>

                <button
                    className="btn"
                    onClick={(e) => handleSendNow(e, 7)}
                    disabled={sending}
                >
                    {sending ? 'Sending…' : 'Send Now (7d)'}
                </button>
            </div>
        </div>
    )
}

export default TopicCard
