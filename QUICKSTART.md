# Quick Start Guide

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Quick Test

### Using the Swagger UI (Recommended)
1. Open http://localhost:8000/docs
2. Try the endpoints interactively

### Using curl

**1. Check health:**
```bash
curl http://localhost:8000/api/v1/health
```

**2. Get available cabs:**
```bash
curl -X POST http://localhost:8000/api/v1/cabs/available ^
  -H "Content-Type: application/json" ^
  -d "{\"location\": {\"latitude\": 12.9716, \"longitude\": 77.5946, \"address\": \"MG Road, Bangalore\"}}"
```

**3. Book a ride:**
```bash
curl -X POST http://localhost:8000/api/v1/rides/book ^
  -H "Content-Type: application/json" ^
  -d "{\"pickup\": {\"latitude\": 12.9716, \"longitude\": 77.5946, \"address\": \"MG Road\"}, \"dropoff\": {\"latitude\": 12.9352, \"longitude\": 77.6245, \"address\": \"Koramangala\"}, \"cab_type\": \"SEDAN\"}"
```

**4. Assign driver (replace RIDE_ID):**
```bash
curl -X POST http://localhost:8000/api/v1/rides/RIDE_ID/assign-driver
```

## Project Structure

```
app/
├── __init__.py      # Package initializer
├── main.py          # FastAPI app & entry point
├── models.py        # Data models (Location, Driver, Ride, etc.)
├── schemas.py       # Pydantic schemas for API validation
├── services.py      # Business logic (CabBookingService)
├── routes.py        # API endpoints
└── utils.py         # Helper functions for data conversion
```

## Key Differences from Original

### Original (app.py)
- Single monolithic file
- Console-based demo
- No API endpoints
- Print statements for output

### New FastAPI Version
- Modular structure with separation of concerns
- RESTful API with proper endpoints
- Pydantic validation for requests/responses
- Automatic API documentation
- CORS support for frontend integration
- Proper error handling with HTTP status codes

## Next Steps

1. **Add Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Add Authentication**: Implement JWT-based auth
3. **Add WebSockets**: Real-time ride tracking
4. **Add Tests**: Unit and integration tests
5. **Add Frontend**: React/Vue.js frontend application
