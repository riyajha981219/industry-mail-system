import './NewsCard.css'

const NewsCard = ({ article }) => {
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })
    }

    return (
        <div className="news-card">
            {article.image_url && (
                <div className="news-image">
                    <img src={article.image_url} alt={article.title} />
                </div>
            )}
            <div className="news-content">
                <h3>{article.title}</h3>
                <p className="news-source">
                    {article.source} • {formatDate(article.published_at)}
                </p>
                <p className="news-description">{article.description}</p>
                <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-secondary"
                >
                    Read Full Article →
                </a>
            </div>
        </div>
    )
}

export default NewsCard
