"""
Pydantic schemas for request/response validation
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    """Location schema"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: str


class DriverSchema(BaseModel):
    """Driver response schema"""
    id: str
    name: str
    phone: str
    rating: float
    total_trips: int
    vehicle_number: str
    vehicle_model: str
    vehicle_color: str
    current_location: LocationSchema
    
    class Config:
        from_attributes = True


class FareSchema(BaseModel):
    """Fare schema"""
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: float = 1.0
    total: float
    
    class Config:
        from_attributes = True


class RideSchema(BaseModel):
    """Ride response schema"""
    ride_id: str
    cab_type: str
    pickup: LocationSchema
    dropoff: LocationSchema
    status: str
    driver: Optional[DriverSchema] = None
    fare: Optional[FareSchema] = None
    created_at: datetime
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    eta_minutes: int = 0
    distance_km: float = 0.0
    duration_minutes: int = 0
    
    class Config:
        from_attributes = True


class BookRideRequest(BaseModel):
    """Request to book a ride"""
    pickup: LocationSchema
    dropoff: LocationSchema
    cab_type: str = Field(..., description="Cab type: MINI, SEDAN, SUV, or LUXURY")


class FareEstimateRequest(BaseModel):
    """Request for fare estimate"""
    pickup: LocationSchema
    dropoff: LocationSchema
    cab_type: str = Field(..., description="Cab type: MINI, SEDAN, SUV, or LUXURY")


class AvailableCabsRequest(BaseModel):
    """Request for available cabs"""
    location: LocationSchema


class UpdateRideStatusRequest(BaseModel):
    """Request to update ride status"""
    status: str = Field(..., description="New status: ARRIVING, IN_PROGRESS, COMPLETED")


class CancelRideRequest(BaseModel):
    """Request to cancel a ride"""
    reason: str = "User cancelled"


class AvailableCabResponse(BaseModel):
    """Available cab information"""
    type: str
    name: str
    capacity: int
    available_count: int
    eta_minutes: int
    surge_multiplier: float


class CancelRideResponse(BaseModel):
    """Cancel ride response"""
    ride_id: str
    status: str
    reason: str
    cancellation_fee: float


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
