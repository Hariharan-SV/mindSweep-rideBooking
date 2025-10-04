"""
Data models for the cab booking system
"""

import random
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RideStatus(str, Enum):
    """Possible ride statuses"""
    SEARCHING = "searching"
    ACCEPTED = "accepted"
    ARRIVING = "arriving"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CabType(Enum):
    """Available cab types"""
    MINI = {"name": "Mini", "base_fare": 50, "per_km": 12, "per_min": 2, "capacity": 4}
    SEDAN = {"name": "Sedan", "base_fare": 80, "per_km": 15, "per_min": 2.5, "capacity": 4}
    SUV = {"name": "SUV", "base_fare": 120, "per_km": 20, "per_min": 3, "capacity": 6}
    LUXURY = {"name": "Luxury", "base_fare": 200, "per_km": 30, "per_min": 5, "capacity": 4}


@dataclass
class Location:
    """Geographic location"""
    latitude: float
    longitude: float
    address: str
    
    def distance_to(self, other: 'Location') -> float:
        """Calculate approximate distance in km (simplified)"""
        lat_diff = abs(self.latitude - other.latitude)
        lng_diff = abs(self.longitude - other.longitude)
        return ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111  # Rough conversion


@dataclass
class Driver:
    """Driver information"""
    id: str
    name: str
    phone: str
    rating: float
    total_trips: int
    vehicle_number: str
    vehicle_model: str
    vehicle_color: str
    current_location: Location
    
    @classmethod
    def generate_random(cls, location: Location) -> 'Driver':
        """Generate a random driver near the location"""
        first_names = ["Rajesh", "Amit", "Suresh", "Vijay", "Anil", "Rahul", "Sanjay", "Manoj"]
        last_names = ["Kumar", "Sharma", "Singh", "Patel", "Reddy", "Verma", "Gupta", "Joshi"]
        
        vehicles = [
            ("Swift", "White"), ("Etios", "Silver"), ("Dzire", "Blue"),
            ("Innova", "Grey"), ("XUV", "Black"), ("Scorpio", "Red")
        ]
        
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        vehicle_model, vehicle_color = random.choice(vehicles)
        
        # Generate location near pickup
        nearby_location = Location(
            latitude=location.latitude + random.uniform(-0.01, 0.01),
            longitude=location.longitude + random.uniform(-0.01, 0.01),
            address="Driver location"
        )
        
        return cls(
            id=str(uuid.uuid4())[:8],
            name=name,
            phone=f"+91-{random.randint(7000000000, 9999999999)}",
            rating=round(random.uniform(4.0, 5.0), 1),
            total_trips=random.randint(100, 5000),
            vehicle_number=f"KA{random.randint(10,99)}{random.choice(['A','B','C'])}{random.randint(1000,9999)}",
            vehicle_model=vehicle_model,
            vehicle_color=vehicle_color,
            current_location=nearby_location
        )


@dataclass
class Fare:
    """Fare breakdown"""
    base_fare: float
    distance_fare: float
    time_fare: float
    surge_multiplier: float = 1.0
    total: float = 0.0
    
    def calculate_total(self):
        """Calculate total fare"""
        subtotal = self.base_fare + self.distance_fare + self.time_fare
        self.total = round(subtotal * self.surge_multiplier, 2)
        return self.total


@dataclass
class Ride:
    """Ride information"""
    ride_id: str
    cab_type: CabType
    pickup: Location
    dropoff: Location
    status: RideStatus
    driver: Optional[Driver] = None
    fare: Optional[Fare] = None
    created_at: datetime = field(default_factory=datetime.now)
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    eta_minutes: int = 0
    distance_km: float = 0.0
    duration_minutes: int = 0
