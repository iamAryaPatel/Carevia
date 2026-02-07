# Carevia - Job Aggregator Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Carevia is a modern job aggregator platform that collects and displays job listings from multiple sources including Remotive and Adzuna. Built with FastAPI backend and React frontend, it provides a seamless experience for job seekers.

## ✨ Features

- 🔄 **Automated Job Aggregation**: Fetches jobs from multiple sources every 12 hours
- 🔍 **Advanced Search & Filtering**: Search by title, company, location, source, and category
- 📄 **Pagination Support**: Efficient browsing of large job datasets
- 🏥 **Health Monitoring**: Built-in health check endpoints
- 🐳 **Docker Support**: Easy deployment with Docker and Docker Compose
- 📊 **RESTful API**: Well-documented API with OpenAPI/Swagger
- 🔒 **Production-Ready**: Security headers, error handling, and logging

## 🏗️ Architecture

```
carevia/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── config.py           # Configuration management
│   │   ├── database.py         # MongoDB connection
│   │   ├── main.py             # FastAPI application
│   │   ├── models/             # Pydantic models
│   │   ├── routes/             # API routes
│   │   ├── services/           # Job aggregation services
│   │   ├── middleware/         # Error handling & logging
│   │   └── scheduler.py        # Background job scheduler
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/frontend/ # React frontend
│   ├── src/
│   │   ├── pages/Jobs.tsx      # Main jobs page
│   │   └── config.ts           # Frontend configuration
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ and Node.js 20+ (for local development)
- MongoDB Atlas account (or local MongoDB instance)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd carevia
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your MongoDB URI
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/v1/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend/frontend
npm install
cp .env.example .env
# Edit .env with your API URL
npm run dev
```

## 📝 Environment Variables

### Backend (.env)

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=<appname>
ENVIRONMENT=development
API_VERSION=v1
ALLOWED_ORIGINS=http://localhost:5173
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
LOG_LEVEL=INFO
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Key Endpoints

- `GET /api/v1/jobs` - Get paginated job listings
- `GET /api/v1/jobs/fetch` - Manually trigger job fetch
- `GET /api/v1/jobs/sources` - Get available job sources
- `GET /health` - Health check endpoint
- `GET /ready` - Readiness check endpoint

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

## 🚢 Deployment

### Deploy to Railway/Render/Heroku

1. Set environment variables in your platform's dashboard
2. Connect your GitHub repository
3. Deploy!

### Deploy with Docker

```bash
docker-compose -f docker-compose.yml up -d
```

For detailed deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 🔧 Configuration

- **Job Fetch Interval**: Modify `hours=12` in `backend/app/scheduler.py`
- **CORS Origins**: Update `ALLOWED_ORIGINS` in `.env`
- **Pagination**: Default page size is 20, max 100

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Remotive](https://remotive.com/) - Remote job listings
- [Adzuna](https://www.adzuna.com/) - Job search API
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend library

## 📧 Support

For support, email your-email@example.com or open an issue on GitHub.

---

Made with ❤️ by Arya Patel
