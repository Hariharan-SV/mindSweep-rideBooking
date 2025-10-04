"""
Utility functions for data conversion
"""

from app.models import Location, Ride, Fare, Driver
from app.schemas import (
    LocationSchema,
    RideSchema,
    FareSchema,
    DriverSchema,
)


def convert_location_to_model(schema: LocationSchema) -> Location:
    """Convert LocationSchema to Location model"""
    return Location(
        latitude=schema.latitude,
        longitude=schema.longitude,
        address=schema.address
    )


def convert_location_to_schema(model: Location) -> LocationSchema:
    """Convert Location model to LocationSchema"""
    return LocationSchema(
        latitude=model.latitude,
        longitude=model.longitude,
        address=model.address
    )


def convert_fare_to_schema(model: Fare) -> FareSchema:
    """Convert Fare model to FareSchema"""
    return FareSchema(
        base_fare=model.base_fare,
        distance_fare=model.distance_fare,
        time_fare=model.time_fare,
        surge_multiplier=model.surge_multiplier,
        total=model.total
    )


def convert_driver_to_schema(model: Driver) -> DriverSchema:
    """Convert Driver model to DriverSchema"""
    return DriverSchema(
        id=model.id,
        name=model.name,
        phone=model.phone,
        rating=model.rating,
        total_trips=model.total_trips,
        vehicle_number=model.vehicle_number,
        vehicle_model=model.vehicle_model,
        vehicle_color=model.vehicle_color,
        current_location=convert_location_to_schema(model.current_location)
    )


def convert_ride_to_schema(model: Ride) -> RideSchema:
    """Convert Ride model to RideSchema"""
    return RideSchema(
        ride_id=model.ride_id,
        cab_type=model.cab_type.name,
        pickup=convert_location_to_schema(model.pickup),
        dropoff=convert_location_to_schema(model.dropoff),
        status=model.status.value,
        driver=convert_driver_to_schema(model.driver) if model.driver else None,
        fare=convert_fare_to_schema(model.fare) if model.fare else None,
        created_at=model.created_at,
        accepted_at=model.accepted_at,
        started_at=model.started_at,
        completed_at=model.completed_at,
        eta_minutes=model.eta_minutes,
        distance_km=model.distance_km,
        duration_minutes=model.duration_minutes
    )
