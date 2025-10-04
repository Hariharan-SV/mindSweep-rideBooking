"""
Mock Cab Booking System
A simulated cab booking application with realistic features
"""

import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class RideStatus(Enum):
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


class CabBookingSystem:
    """Mock cab booking system"""
    
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
        
        print(f"\n🚗 Ride booked! ID: {ride_id}")
        print(f"📍 Pickup: {pickup.address}")
        print(f"📍 Dropoff: {dropoff.address}")
        print(f"💰 Estimated fare: ₹{ride.fare.total}")
        print(f"🔍 Searching for drivers...")
        
        return ride
    
    def assign_driver(self, ride_id: str) -> Driver:
        """Simulate driver assignment"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        # Simulate search time
        time.sleep(random.uniform(2, 5))
        
        # Generate random driver
        driver = Driver.generate_random(ride.pickup)
        ride.driver = driver
        ride.status = RideStatus.ACCEPTED
        ride.accepted_at = datetime.now()
        ride.eta_minutes = random.randint(3, 10)
        
        print(f"\n✅ Driver found!")
        print(f"👤 Driver: {driver.name}")
        print(f"⭐ Rating: {driver.rating}/5.0 ({driver.total_trips} trips)")
        print(f"🚙 Vehicle: {driver.vehicle_color} {driver.vehicle_model}")
        print(f"🔢 Number: {driver.vehicle_number}")
        print(f"📞 Phone: {driver.phone}")
        print(f"⏱️  ETA: {ride.eta_minutes} minutes")
        
        return driver
    
    def track_ride(self, ride_id: str) -> Ride:
        """Get current ride status"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        return ride
    
    def update_ride_status(self, ride_id: str, new_status: RideStatus):
        """Update ride status"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        ride.status = new_status
        
        if new_status == RideStatus.ARRIVING:
            print(f"\n🚗 Driver is arriving...")
        elif new_status == RideStatus.IN_PROGRESS:
            ride.started_at = datetime.now()
            print(f"\n🛣️  Ride started! Heading to destination...")
        elif new_status == RideStatus.COMPLETED:
            ride.completed_at = datetime.now()
            self._complete_ride(ride)
    
    def simulate_ride(self, ride_id: str):
        """Simulate complete ride flow"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        # Assign driver
        self.assign_driver(ride_id)
        time.sleep(2)
        
        # Driver arriving
        self.update_ride_status(ride_id, RideStatus.ARRIVING)
        print(f"⏱️  ETA: {ride.eta_minutes} minutes")
        time.sleep(3)
        
        # Start ride
        self.update_ride_status(ride_id, RideStatus.IN_PROGRESS)
        print(f"📏 Distance: {ride.distance_km} km")
        print(f"⏱️  Estimated time: {ride.duration_minutes} minutes")
        time.sleep(3)
        
        # Complete ride
        self.update_ride_status(ride_id, RideStatus.COMPLETED)
    
    def cancel_ride(self, ride_id: str, reason: str = "User cancelled"):
        """Cancel a ride"""
        ride = self.rides.get(ride_id)
        if not ride:
            raise ValueError("Ride not found")
        
        ride.status = RideStatus.CANCELLED
        
        # Calculate cancellation fee
        cancellation_fee = 0
        if ride.status in [RideStatus.ACCEPTED, RideStatus.ARRIVING]:
            cancellation_fee = 50
        
        print(f"\n❌ Ride cancelled")
        print(f"Reason: {reason}")
        if cancellation_fee > 0:
            print(f"💰 Cancellation fee: ₹{cancellation_fee}")
    
    def _complete_ride(self, ride: Ride):
        """Handle ride completion"""
        print(f"\n✅ Ride completed!")
        print(f"\n📊 Ride Summary:")
        print(f"   Ride ID: {ride.ride_id}")
        print(f"   Distance: {ride.distance_km} km")
        print(f"   Duration: {ride.duration_minutes} minutes")
        print(f"\n💰 Fare Breakdown:")
        print(f"   Base fare: ₹{ride.fare.base_fare}")
        print(f"   Distance ({ride.distance_km} km): ₹{ride.fare.distance_fare:.2f}")
        print(f"   Time ({ride.duration_minutes} min): ₹{ride.fare.time_fare:.2f}")
        if ride.fare.surge_multiplier > 1.0:
            print(f"   Surge multiplier: {ride.fare.surge_multiplier}x")
        print(f"   {'─' * 40}")
        print(f"   Total: ₹{ride.fare.total}")
        print(f"\n⭐ Rate your driver: {ride.driver.name}")
    
    def _get_surge_multiplier(self, location: Location) -> float:
        """Get surge pricing for location"""
        # Random surge between 1.0 and 2.0
        hour = datetime.now().hour
        
        # Higher surge during peak hours
        if 8 <= hour <= 10 or 17 <= hour <= 20:
            return round(random.uniform(1.2, 2.0), 1)
        else:
            return round(random.uniform(1.0, 1.3), 1)
    
    def get_ride_history(self) -> List[Ride]:
        """Get all completed rides"""
        return [
            ride for ride in self.rides.values()
            if ride.status == RideStatus.COMPLETED
        ]


def main():
    """Demo of cab booking system"""
    print("=" * 60)
    print("🚖 MOCK CAB BOOKING SYSTEM")
    print("=" * 60)
    
    # Initialize system
    system = CabBookingSystem()
    
    # Define locations (Bangalore example)
    pickup = Location(
        latitude=12.9716,
        longitude=77.5946,
        address="MG Road, Bangalore"
    )
    
    dropoff = Location(
        latitude=12.9352,
        longitude=77.6245,
        address="Koramangala, Bangalore"
    )
    
    print(f"\n📍 Pickup: {pickup.address}")
    print(f"📍 Dropoff: {dropoff.address}")
    
    # Get available cabs
    print("\n" + "─" * 60)
    print("🚗 AVAILABLE CABS")
    print("─" * 60)
    
    available = system.get_available_cabs(pickup)
    for i, cab in enumerate(available, 1):
        print(f"\n{i}. {cab['name']}")
        print(f"   Capacity: {cab['capacity']} passengers")
        print(f"   Available: {cab['available_count']} cabs")
        print(f"   ETA: {cab['eta_minutes']} min")
        if cab['surge_multiplier'] > 1.0:
            print(f"   ⚡ Surge: {cab['surge_multiplier']}x")
    
    # Get fare estimates
    print("\n" + "─" * 60)
    print("💰 FARE ESTIMATES")
    print("─" * 60)
    
    for cab_type in CabType:
        fare = system.get_fare_estimate(pickup, dropoff, cab_type)
        print(f"\n{cab_type.value['name']}: ₹{fare.total}")
        if fare.surge_multiplier > 1.0:
            print(f"  (includes {fare.surge_multiplier}x surge)")
    
    # Book a ride
    print("\n" + "─" * 60)
    print("📱 BOOKING RIDE")
    print("─" * 60)
    
    ride = system.book_ride(pickup, dropoff, CabType.SEDAN)
    
    # Simulate complete ride
    print("\n" + "─" * 60)
    print("🚗 RIDE IN PROGRESS")
    print("─" * 60)
    
    system.simulate_ride(ride.ride_id)
    
    # Show ride history
    print("\n" + "─" * 60)
    print("📜 RIDE HISTORY")
    print("─" * 60)
    
    history = system.get_ride_history()
    print(f"\nTotal completed rides: {len(history)}")


if __name__ == "__main__":
    main()