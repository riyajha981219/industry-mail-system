# Industry Mailer System

A full-stack web application that delivers curated industry news newsletters to subscribers. Built with FastAPI (backend) and React (frontend), this system fetches top news articles from NewsAPI and sends formatted emails to users based on their industry interests.

## 🚀 Features

- **Industry Topic Subscriptions**: Users can subscribe to multiple industry topics
- **Flexible Scheduling**: Choose newsletter frequency (daily, weekly, or monthly)
- **News Aggregation**: Fetches top 10 articles from NewsAPI for selected topics
- **Beautiful Email Templates**: HTML-formatted newsletters with images and descriptions
- **Real-time Dashboard**: Preview news articles before subscribing
- **RESTful API**: Clean, well-documented API endpoints
- **Responsive UI**: Modern React interface that works on all devices

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- NewsAPI Key (get free at [newsapi.org](https://newsapi.org))
- Gmail account for sending emails (or other SMTP service)

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation
- **HTTPX**: Async HTTP client for API calls
- **SMTP**: Email delivery

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **CSS3**: Styling

## 📁 Project Structure

```
industry-mail-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── users.py
│   │   │       ├── topics.py
│   │   │       ├── subscriptions.py
│   │   │       └── news.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── topic.py
│   │   │   └── subscription.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── news_service.py
│   │   │   └── email_service.py
│   │   ├── main.py
│   │   ├── config.py
│   │   └── database.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚦 Getting Started

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   NEWS_API_KEY=your_newsapi_key_here
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   EMAIL_FROM=your_email@gmail.com
   ```

   > **Note**: For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   Backend will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## 📝 API Endpoints

### Topics
- `GET /api/topics/` - List all topics
- `POST /api/topics/` - Create new topic
- `GET /api/topics/{id}` - Get topic by ID
- `PUT /api/topics/{id}` - Update topic
- `DELETE /api/topics/{id}` - Delete topic

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Subscriptions
- `GET /api/subscriptions/` - List all subscriptions
- `POST /api/subscriptions/` - Create subscription
- `GET /api/subscriptions/user/{user_id}` - Get user's subscriptions
- `PUT /api/subscriptions/{id}` - Update subscription
- `DELETE /api/subscriptions/{id}` - Delete subscription

### News
- `GET /api/news/fetch` - Fetch news articles
  - Query params: `topic`, `days` (1, 7, or 30), `limit`
- `POST /api/news/send-newsletter` - Send newsletter to subscribers
  - Body: `{"topic_id": 1, "days": 7}`

## 💡 Usage

### Creating Topics

Use the API to create industry topics:

```bash
curl -X POST http://localhost:8000/api/topics/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "description": "Latest tech news and innovations",
    "keywords": "technology,AI,software,hardware"
  }'
```

Or use the interactive API docs at `http://localhost:8000/docs`

### Subscribing to Topics

1. Visit `http://localhost:5173/subscribe`
2. Browse available topics
3. Click "Subscribe" on your preferred topic
4. Fill in your email and select frequency
5. Submit the form

### Viewing News

1. Visit `http://localhost:5173/dashboard`
2. Enter an industry keyword (e.g., "technology", "healthcare")
3. Select time period (1, 7, or 30 days)
4. Click "Search News" to preview articles

## 📧 Email Configuration

### Gmail Setup

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the generated password
3. Use this password in your `.env` file as `SMTP_PASSWORD`

### Other SMTP Services

Modify the `SMTP_HOST` and `SMTP_PORT` in your `.env`:

```env
# For Outlook
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587

# For SendGrid
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
```

## 🔧 Environment Variables

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./industry_mailer.db` |
| `NEWS_API_KEY` | NewsAPI.org API key | `abc123...` |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | Email account username | `you@gmail.com` |
| `SMTP_PASSWORD` | Email account password | `your_app_password` |
| `EMAIL_FROM` | Sender email address | `you@gmail.com` |
| `SECRET_KEY` | JWT secret key | `random-secret-key` |

### Frontend (.env.local) - Optional

```env
VITE_API_URL=http://localhost:8000/api
```

## 🧪 Testing the System

1. **Create a topic**:
   ```bash
   curl -X POST http://localhost:8000/api/topics/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Tech","description":"Technology news","keywords":"technology,AI,software"}'
   ```

2. **Test news fetching**:
   ```bash
   curl "http://localhost:8000/api/news/fetch?topic=technology&days=1&limit=10"
   ```

3. **Create a subscription and test email**:
   - Use the web interface at `http://localhost:5173/subscribe`
   - Or use API directly via `/docs`

## 🚀 Deployment

### Backend Deployment (Heroku/Railway/Render)

1. Update `DATABASE_URL` to use PostgreSQL
2. Set environment variables in hosting platform
3. Deploy using Git or Docker

### Frontend Deployment (Vercel/Netlify)

1. Build the frontend:
   ```bash
   npm run build
   ```
2. Deploy the `dist` folder
3. Set `VITE_API_URL` to your backend URL

## 📊 Database Schema

### Users
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `full_name`: String
- `is_active`: Boolean
- `created_at`: DateTime

### Topics
- `id`: Integer (Primary Key)
- `name`: String (Unique)
- `description`: Text
- `keywords`: String (comma-separated)
- `is_active`: Boolean
- `created_at`: DateTime

### Subscriptions
- `id`: Integer (Primary Key)
- `user_id`: Foreign Key → Users
- `topic_id`: Foreign Key → Topics
- `frequency`: Enum ('1', '7', '30')
- `last_sent_at`: DateTime
- `created_at`: DateTime

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**:
```bash
uvicorn app.main:app --reload --port 8001
```

**Database errors**:
```bash
# Delete the database and restart
rm industry_mailer.db
uvicorn app.main:app --reload
```

### Frontend Issues

**Port already in use**:
Edit `vite.config.js` and change the port:
```js
server: { port: 3000 }
```

**API connection errors**:
Check that backend is running and CORS is properly configured.

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the console logs for errors

## 🎯 Future Enhancements

- [ ] User authentication and login
- [ ] Subscription management dashboard
- [ ] Email template customization
- [ ] Analytics and tracking
- [ ] Scheduled newsletter automation
- [ ] Multiple language support
- [ ] Social media sharing
- [ ] Mobile app

---

Built with ❤️ using FastAPI and React
