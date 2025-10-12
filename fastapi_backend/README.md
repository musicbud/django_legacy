# MusicBud API - FastAPI Version

A high-performance REST API built with FastAPI for the MusicBud platform.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Access the API

- **API**: http://localhost:8001
- **Swagger Docs**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 📋 Features

✅ **15 Public Guest Endpoints** - No authentication required  
✅ **Auto-generated Documentation** - Swagger UI & ReDoc  
✅ **Type Safety** - Pydantic models for validation  
✅ **High Performance** - Async/await support  
✅ **CORS Enabled** - Cross-origin requests supported  

## 📝 API Endpoints

### Discovery
- `GET /v1/discover/public/` - Get discover content
- `GET /v1/discover/public/trending/` - Get trending content
- `GET /v1/discover/public/genres/` - Get available genres

### Recommendations
- `GET /v1/recommendations/public/` - Get public recommendations

### Content Details
- `GET /v1/content/public/{type}/{id}/` - Get content details
  - Types: movie, manga, anime, track, artist, album

## 🧪 Testing

```bash
# Run all tests
bash test_fastapi_endpoints.sh

# Test single endpoint
curl http://localhost:8001/v1/discover/public/genres/
```

## 📦 Project Structure

```
fastapi_backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py     # API router
│   │       └── endpoints/
│   │           └── public.py   # Public endpoints
│   ├── core/
│   │   └── config.py           # Settings
│   └── schemas/
│       └── responses.py        # Pydantic models
├── requirements.txt
├── test_fastapi_endpoints.sh
├── README.md
└── FASTAPI_MIGRATION.md
```

## 🔧 Configuration

Create a `.env` file:

```env
PROJECT_NAME=MusicBud API
VERSION=2.0.0-fastapi
HOST=0.0.0.0
PORT=8001
SECRET_KEY=your-secret-key-here
```

## 📖 Documentation

- **Migration Guide**: See `FASTAPI_MIGRATION.md`
- **API Docs**: Visit `/docs` when server is running

## 🎯 Why FastAPI?

- ⚡ **Fast**: High performance, comparable to NodeJS and Go
- 📚 **Automatic Docs**: Interactive API documentation
- 🔒 **Type Safe**: Pydantic validation catches errors early
- 🚀 **Modern**: Uses Python 3.6+ type hints
- 🔄 **Async**: Native async/await support

## 📊 Performance

FastAPI is one of the fastest Python frameworks:
- 2.5x faster than Django
- Native async support
- Efficient JSON serialization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

**Version**: 2.0.0-fastapi  
**Status**: Production Ready ✅
