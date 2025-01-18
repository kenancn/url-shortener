# URL Shortener API

A FastAPI application that converts long URLs into short, manageable links. This service provides an easy way to create shortened URLs, track their usage statistics, and manage redirections efficiently using Redis caching.

## Overview

This URL shortener service is built with performance and scalability in mind. It uses:
- **FastAPI** for high-performance API endpoints
- **PostgreSQL** for reliable data storage
- **Redis** for caching to improve response times
- **Docker** for easy deployment and scaling

Key capabilities:
- Generate short, unique URLs from long ones
- Track click statistics for each shortened URL
- Fast redirections with caching

## Features

- URL Shortening
- Redirection
- Statistics Tracking
- Redis Caching
- PostgreSQL Database

## API Endpoints

### 1. Shorten URL
```http
POST /shorten/
```

**Request:**
```json
{
    "original_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
    "id": 1,
    "original_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "short_url": "abc123",
    "clicks": 0,
    "created_at": "2025-01-18T10:30:00",
    "updated_at": null,
    "full_url": "http://localhost:8000/abc123"
}
```

### 2. Redirect from Short URL
```http
GET /{short_url}
```
- Example: `GET /abc123`
- Response: 307 Temporary Redirect to original URL

### 3. URL Statistics
```http
GET /stats/{short_url}
```

**Response:**
```json
{
    "id": 1,
    "original_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "short_url": "abc123",
    "clicks": 5,
    "created_at": "2025-01-18T10:30:00",
    "updated_at": "2025-01-18T11:45:00",
    "full_url": "http://localhost:8000/abc123"
}
```

## Environment Variables

The following environment variables are required:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/url_shortener

# Redis Configuration
REDIS_URL=redis://localhost:6379
```

## Deployment

### Using Docker

1. Clone the repository:
```bash
git clone https://github.com/kenancn/url-shortener.git
cd url-shortener
```

2. Configure environment:
   - Copy `.env.example` to `.env`
   - Update environment variables if needed

3. Build and start services:
```bash
docker-compose up -d
```

4. Check service health:
```bash
docker-compose ps
```

### Manual Deployment

1. Prerequisites:
   - Python 3.12+
   - PostgreSQL
   - Redis

2. Clone and setup:
```bash
git clone https://github.com/kenancn/url-shortener.git
cd url-shortener
```

2. Create and activate Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Configure environment:
   - Create `.env` file with required variables
   - Start PostgreSQL and Redis services

4. Run application:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Health Checks

The application includes health checks for:
- PostgreSQL database connection
- Redis connection
- Application status

Docker Compose automatically manages service health checks and dependencies.

## Testing

To run tests:
```bash
pytest
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Technologies Used

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Pydantic
- Docker
- pytest
