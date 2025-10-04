"""
Business logic for the cab booking system
"""

import random
import time
from datetime import datetime
from typing import Dict, List

from app.models import (
    CabType, Driver, Fare, Location, Ride, RideStatus
)


class CabBookingService:
    """Service for cab booking operations"""
    
    def __init__(self):
        self.rides: Dict[str, Ride] = {}
        self.surge_areas = {}  # Track surge pricing by area
    
    def get_available_cabs(self, location: Location) -> List[Dict]:
        """Get available cab types at location"""
        available_cabs = []
        
        for cab_type in CabType:
            # Random availability
            available_count = random.randint(2, 10)
            eta = random.randint(2, 15)
            
            # Check for surge pricing
            surge = self._get_surge_multiplier(location)
            
            available_cabs.append({
                "type": cab_type.name,
                "name": cab_type.value["name"],
                "capacity": cab_type.value["capacity"],
                "available_count": available_count,
                "eta_minutes": eta,
                "surge_multiplier": surge
            })
        
        return available_cabs
    
    def get_fare_estimate(
        self,
        pickup: Location,
        dropoff: Location,
        cab_type: CabType
    ) -> Fare:
        """Calculate fare estimate"""
        distance = pickup.distance_to(dropoff)
        
        # Estimate time based on distance (assume 30 km/h average)
        duration = (distance / 30) * 60  # in minutes
        
        cab_rates = cab_type.value
        
        fare = Fare(
            base_fare=cab_rates["base_fare"],
            distance_fare=distance * cab_rates["per_km"],
            time_fare=duration * cab_rates["per_min"],
            surge_multiplier=self._get_surge_multiplier(pickup)
        )
        
        fare.calculate_total()
        return fare
    
    def book_ride(
        self,
        pickup: Location,
        dropoff: Location,
        cab_type: CabType
    ) -> Ride:
        """Book a new ride"""
        import uuid
        ride_id = str(uuid.uuid4())[:8].upper()
        
        distance = pickup.distance_to(dropoff)
        duration = int((distance / 30) * 60)  # Estimated duration
        
        ride = Ride(
            ride_id=ride_id,
            cab_type=cab_type,
            pickup=pickup,
            dropoff=dropoff,
            status=RideStatus.SEARCHING,
            distance_km=round(distance, 2),
            duration_minutes=duration,
            fare=self.get_fare_estimate(pickup, dropoff, cab_type)
        )
        
        self.rides[ride_id] = ride
        return ride
    
    def assign_driver(self, ride_id: str) -> Driver:
        """Simulate driver assignment"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        # Generate random driver
        driver = Driver.generate_random(ride.pickup)
        ride.driver = driver
        ride.status = RideStatus.ACCEPTED
        ride.accepted_at = datetime.now()
        ride.eta_minutes = random.randint(3, 10)
        
        return driver
    
    def get_ride(self, ride_id: str) -> Ride:
        """Get ride by ID"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        return ride
    
    def update_ride_status(self, ride_id: str, new_status: RideStatus) -> Ride:
        """Update ride status"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        ride.status = new_status
        
        if new_status == RideStatus.IN_PROGRESS:
            ride.started_at = datetime.now()
        elif new_status == RideStatus.COMPLETED:
            ride.completed_at = datetime.now()
        
        return ride
    
    def cancel_ride(self, ride_id: str, reason: str = "User cancelled") -> dict:
        """Cancel a ride"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        ride.status = RideStatus.CANCELLED
        
        # Calculate cancellation fee
        cancellation_fee = 0
        if ride.status in [RideStatus.ACCEPTED, RideStatus.ARRIVING]:
            cancellation_fee = 50
        
        return {
            "ride_id": ride_id,
            "status": "cancelled",
            "reason": reason,
            "cancellation_fee": cancellation_fee
        }
    
    def get_ride_history(self) -> List[Ride]:
        """Get all completed rides"""
        return [
            ride for ride in self.rides.values()
            if ride.status == RideStatus.COMPLETED
        ]
    
    def _get_surge_multiplier(self, location: Location) -> float:
        """Get surge pricing for location"""
        # Random surge between 1.0 and 2.0
        hour = datetime.now().hour
        
        # Higher surge during peak hours
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            return round(random.uniform(1.2, 2.0), 1)
        else:
            return round(random.uniform(1.0, 1.3), 1)


# Singleton instance
booking_service = CabBookingService()
