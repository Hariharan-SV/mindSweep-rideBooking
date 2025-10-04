"""
API routes for the cab booking system
"""

from typing import List
from fastapi import APIRouter, HTTPException, status

from app.models import CabType, Location, RideStatus
from app.schemas import (
    AvailableCabResponse,
    AvailableCabsRequest,
    BookRideRequest,
    CancelRideRequest,
    CancelRideResponse,
    FareEstimateRequest,
    FareSchema,
    RideSchema,
    UpdateRideStatusRequest,
)
from app.services import booking_service
from app.utils import convert_ride_to_schema, convert_location_to_model, convert_fare_to_schema

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Cab Booking API"}


@router.post(
    "/cabs/available",
    response_model=List[AvailableCabResponse],
    tags=["Cabs"],
    summary="Get available cabs at a location"
)
async def get_available_cabs(request: AvailableCabsRequest):
    """
    Get list of available cab types at the specified location.
    
    Returns information about each cab type including:
    - Availability count
    - ETA
    - Surge pricing
    """
    location = convert_location_to_model(request.location)
    available_cabs = booking_service.get_available_cabs(location)
    return available_cabs


@router.post(
    "/fare/estimate",
    response_model=FareSchema,
    tags=["Fare"],
    summary="Get fare estimate"
)
async def get_fare_estimate(request: FareEstimateRequest):
    """
    Calculate fare estimate for a trip.
    
    Provides breakdown of:
    - Base fare
    - Distance-based fare
    - Time-based fare
    - Surge multiplier
    - Total fare
    """
    try:
        cab_type = CabType[request.cab_type.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cab type. Must be one of: {', '.join([ct.name for ct in CabType])}"
        )
    
    pickup = convert_location_to_model(request.pickup)
    dropoff = convert_location_to_model(request.dropoff)
    
    fare = booking_service.get_fare_estimate(pickup, dropoff, cab_type)
    return convert_fare_to_schema(fare)


@router.post(
    "/rides/book",
    response_model=RideSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Rides"],
    summary="Book a new ride"
)
async def book_ride(request: BookRideRequest):
    """
    Book a new ride.
    
    Creates a ride request and starts searching for available drivers.
    Returns ride details including ride ID for tracking.
    """
    try:
        cab_type = CabType[request.cab_type.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cab type. Must be one of: {', '.join([ct.name for ct in CabType])}"
        )
    
    pickup = convert_location_to_model(request.pickup)
    dropoff = convert_location_to_model(request.dropoff)
    
    ride = booking_service.book_ride(pickup, dropoff, cab_type)
    return convert_ride_to_schema(ride)


@router.get(
    "/rides/{ride_id}",
    response_model=RideSchema,
    tags=["Rides"],
    summary="Get ride details"
)
async def get_ride(ride_id: str):
    """
    Get details of a specific ride by ID.
    
    Returns complete ride information including:
    - Current status
    - Driver details (if assigned)
    - Fare breakdown
    - Timestamps
    """
    try:
        ride = booking_service.get_ride(ride_id)
        return convert_ride_to_schema(ride)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/rides/{ride_id}/assign-driver",
    response_model=RideSchema,
    tags=["Rides"],
    summary="Assign driver to ride"
)
async def assign_driver(ride_id: str):
    """
    Assign a driver to the ride.
    
    Simulates finding and assigning a driver to the ride request.
    Updates ride status to ACCEPTED.
    """
    try:
        booking_service.assign_driver(ride_id)
        ride = booking_service.get_ride(ride_id)
        return convert_ride_to_schema(ride)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch(
    "/rides/{ride_id}/status",
    response_model=RideSchema,
    tags=["Rides"],
    summary="Update ride status"
)
async def update_ride_status(ride_id: str, request: UpdateRideStatusRequest):
    """
    Update the status of a ride.
    
    Valid status transitions:
    - SEARCHING -> ACCEPTED
    - ACCEPTED -> ARRIVING
    - ARRIVING -> IN_PROGRESS
    - IN_PROGRESS -> COMPLETED
    """
    try:
        new_status = RideStatus[request.status.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join([s.name for s in RideStatus])}"
        )
    
    try:
        ride = booking_service.update_ride_status(ride_id, new_status)
        return convert_ride_to_schema(ride)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/rides/{ride_id}/cancel",
    response_model=CancelRideResponse,
    tags=["Rides"],
    summary="Cancel a ride"
)
async def cancel_ride(ride_id: str, request: CancelRideRequest):
    """
    Cancel a ride.
    
    Cancels the ride and calculates any applicable cancellation fees.
    Cancellation fees may apply if driver has already been assigned.
    """
    try:
        result = booking_service.cancel_ride(ride_id, request.reason)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/rides/history/all",
    response_model=List[RideSchema],
    tags=["Rides"],
    summary="Get ride history"
)
async def get_ride_history():
    """
    Get all completed rides.
    
    Returns a list of all rides that have been completed.
    """
    rides = booking_service.get_ride_history()
    return [convert_ride_to_schema(ride) for ride in rides]
