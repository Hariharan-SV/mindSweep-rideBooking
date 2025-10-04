# Cab Booking API

A FastAPI-based mock cab booking system with realistic features.

## Features

- 🚗 Multiple cab types (Mini, Sedan, SUV, Luxury)
- 💰 Dynamic fare calculation with surge pricing
- 👤 Random driver assignment
- 📍 Location-based services
- 🔄 Real-time ride status tracking
- 📜 Ride history

## Project Structure

```
mindSweepRideBooking/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Data models (dataclasses)
│   ├── schemas.py       # Pydantic schemas for validation
│   ├── services.py      # Business logic
│   ├── routes.py        # API endpoints
│   └── utils.py         # Utility functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health status

### Cabs
- `POST /api/v1/cabs/available` - Get available cabs at a location

### Fare
- `POST /api/v1/fare/estimate` - Get fare estimate for a trip

### Rides
- `POST /api/v1/rides/book` - Book a new ride
- `GET /api/v1/rides/{ride_id}` - Get ride details
- `POST /api/v1/rides/{ride_id}/assign-driver` - Assign driver to ride
- `PATCH /api/v1/rides/{ride_id}/status` - Update ride status
- `POST /api/v1/rides/{ride_id}/cancel` - Cancel a ride
- `GET /api/v1/rides/history/all` - Get all completed rides

## Example Usage

### 1. Get Available Cabs

```bash
curl -X POST "http://localhost:8000/api/v1/cabs/available" \
  -H "Content-Type: application/json" \
  -d '{
    "location": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address": "MG Road, Bangalore"
    }
  }'
```

### 2. Get Fare Estimate

```bash
curl -X POST "http://localhost:8000/api/v1/fare/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address": "MG Road, Bangalore"
    },
    "dropoff": {
      "latitude": 12.9352,
      "longitude": 77.6245,
      "address": "Koramangala, Bangalore"
    },
    "cab_type": "SEDAN"
  }'
```

### 3. Book a Ride

```bash
curl -X POST "http://localhost:8000/api/v1/rides/book" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup": {
      "latitude": 12.9716,
      "longitude": 77.5946,
      "address": "MG Road, Bangalore"
    },
    "dropoff": {
      "latitude": 12.9352,
      "longitude": 77.6245,
      "address": "Koramangala, Bangalore"
    },
    "cab_type": "SEDAN"
  }'
```

### 4. Assign Driver

```bash
curl -X POST "http://localhost:8000/api/v1/rides/{ride_id}/assign-driver"
```

### 5. Update Ride Status

```bash
curl -X PATCH "http://localhost:8000/api/v1/rides/{ride_id}/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "IN_PROGRESS"
  }'
```

## Cab Types

- **MINI**: Base fare ₹50, ₹12/km, ₹2/min, 4 passengers
- **SEDAN**: Base fare ₹80, ₹15/km, ₹2.5/min, 4 passengers
- **SUV**: Base fare ₹120, ₹20/km, ₹3/min, 6 passengers
- **LUXURY**: Base fare ₹200, ₹30/km, ₹5/min, 4 passengers

## Ride Status Flow

1. **SEARCHING** - Looking for available drivers
2. **ACCEPTED** - Driver assigned and accepted
3. **ARRIVING** - Driver is on the way to pickup
4. **IN_PROGRESS** - Ride is in progress
5. **COMPLETED** - Ride completed successfully
6. **CANCELLED** - Ride was cancelled

## Features

### Dynamic Surge Pricing
- Peak hours (8-10 AM, 5-8 PM): 1.2x - 2.0x surge
- Off-peak hours: 1.0x - 1.3x surge

### Cancellation Policy
- Free cancellation before driver assignment
- ₹50 cancellation fee after driver assignment

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Type Checking
```bash
mypy app/
```

## License

MIT License
