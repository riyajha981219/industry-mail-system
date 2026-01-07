import { useState } from 'react'
import api from '../services/api'
import NewsCard from '../components/NewsCard'
import './Dashboard.css'

const Dashboard = () => {
    const [searchParams, setSearchParams] = useState({
        topic: '',
        days: '1'
    })
    const [articles, setArticles] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleInputChange = (e) => {
        setSearchParams({ ...searchParams, [e.target.name]: e.target.value })
    }

    const handleSearch = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            const data = await api.fetchNews(searchParams.topic, searchParams.days)
            setArticles(data.articles)
        } catch (err) {
            setError('Failed to fetch news articles')
            setArticles([])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container">
            <div className="dashboard-header">
                <h1>News Dashboard</h1>
                <p>Search and preview news articles by industry topic</p>
            </div>

            <div className="card">
                <form onSubmit={handleSearch} className="search-form">
                    <div className="form-row">
                        <div className="form-group">
                            <label htmlFor="topic">Industry Topic</label>
                            <input
                                type="text"
                                id="topic"
                                name="topic"
                                value={searchParams.topic}
                                onChange={handleInputChange}
                                placeholder="e.g., technology, healthcare, finance"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="days">Time Period</label>
                            <select
                                id="days"
                                name="days"
                                value={searchParams.days}
                                onChange={handleInputChange}
                                required
                            >
                                <option value="1">Last 1 day</option>
                                <option value="7">Last 7 days</option>
                                <option value="30">Last 30 days</option>
                            </select>
                        </div>
                        <div className="form-group">
                        <button type="submit" className="btn btn-primary search-btn" disabled={loading}>
                            {loading ? 'Searching...' : 'Search News'}
                        </button>
                        </div>
                    </div>
                </form>

                {error && <div className="error">{error}</div>}
            </div>

            {loading && <div className="loading">Fetching latest news...</div>}

            {articles.length > 0 && (
                <div className="results-section">
                    <h2>Found {articles.length} Articles</h2>
                    <div className="grid">
                        {articles.map((article, index) => (
                            <NewsCard key={index} article={article} />
                        ))}
                    </div>
                </div>
            )}

            {!loading && articles.length === 0 && searchParams.topic && (
                <div className="no-results">
                    <h3>No articles found</h3>
                    <p>Try adjusting your search criteria or selecting a different time period</p>
                </div>
            )}
        </div>
    )
}

export default Dashboard
