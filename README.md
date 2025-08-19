# LaudatorAI

**LaudatorAI** is your AI advocate in the job market, inspired by the ancient *laudator* — one who praises and elevates others' achievements. This platform automates the tailoring of resumes and the crafting of cover letters to match specific job postings, ensuring your applications stand out with precision and polish.

## 🚀 Features

- **Smart Job Description Extraction**: Automatically extract and normalize job descriptions from any job posting URL
- **AI-Powered Resume Tailoring**: Use advanced AI to tailor your resume for specific job requirements
- **Cover Letter Generation**: Generate compelling, personalized cover letters
- **Professional Output**: Get polished DOCX and PDF files ready for your job applications
- **Modern Web Interface**: Beautiful, responsive UI built with Next.js and Tailwind CSS

## 🏗️ Architecture

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI (Python 3.11+), SQLAlchemy, Celery
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **File Storage**: MinIO/S3
- **Web Scraping**: Playwright + Readability
- **LLM Integration**: Pluggable (OpenAI/Ollama/HuggingFace)
- **Document Processing**: python-docx + weasyprint

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (for local development)
- PostgreSQL
- Redis

## 🚀 Deployment

LaudatorAI is configured for deployment on modern cloud platforms:

- **Backend**: Deployed on Railway with PostgreSQL and Redis
- **Frontend**: Deployed on Vercel with automatic CI/CD

### Quick Deployment Steps

1. **Backend (Railway)**:
   - Connect your GitHub repository to Railway
   - Add PostgreSQL and Redis services
   - Configure environment variables
   - Deploy automatically on push to main

2. **Frontend (Vercel)**:
   - Connect your GitHub repository to Vercel
   - Configure environment variables
   - Deploy automatically on push to main

3. **Integration**:
   - Update CORS settings
   - Test API connectivity
   - Configure custom domains (optional)

## 🛠️ Local Development

### Option 1: Docker Compose (Recommended for Local)

1. Clone the repository:
```bash
git clone https://github.com/caprolt/LaudatorAI.git
cd LaudatorAI
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MinIO Console: http://localhost:9001

### Option 2: Local Development Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Access the application at http://localhost:3000

## 📁 Project Structure

```
LaudatorAI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend Docker image
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utility functions
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend Docker image
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD workflows
├── docker-compose.yml     # Local development setup
└── README.md             # This file
```

## 🧪 Development

### Code Quality

#### Backend
```bash
cd backend
# Format code
black app/
# Sort imports
isort app/
# Type checking
mypy app/
# Run tests
pytest tests/
```

#### Frontend
```bash
cd frontend
# Lint code
npm run lint
# Type checking
npm run type-check
# Build
npm run build
```

### Running Tests

The project includes comprehensive test suites for both backend and frontend:

- **Backend**: pytest with async support
- **Frontend**: Jest and React Testing Library
- **E2E**: Playwright (coming soon)

### CI/CD

The project uses GitHub Actions for continuous integration:

- Automated testing on push/PR
- Code quality checks (linting, type checking)
- Build verification
- Docker image building

## 📚 API Documentation

Once the backend is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=LaudatorAI

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=laudatorai

# Redis
REDIS_URL=redis://localhost:6379/0

# File Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=laudatorai

# LLM
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Production Deployment

The project includes Docker configurations for easy deployment:

1. Build and push Docker images
2. Deploy using Docker Compose or Kubernetes
3. Configure environment variables for production
4. Set up monitoring and logging

### Environment-Specific Configurations

- **Development**: Local Docker Compose setup
- **Staging**: Production-like environment for testing
- **Production**: Optimized for performance and security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join the community discussions

## 🗺️ Roadmap

- [ ] Phase 1: Foundation & Setup ✅
- [ ] Phase 2: Core Backend Infrastructure
- [ ] Phase 3: Job Description Processing
- [ ] Phase 4: Resume Processing
- [ ] Phase 5: Cover Letter Generation
- [ ] Phase 6: Frontend Development
- [ ] Phase 7: Integration & Testing
- [ ] Phase 8: Deployment & Launch

---

**LaudatorAI** - Your AI advocate in the job market 🚀
