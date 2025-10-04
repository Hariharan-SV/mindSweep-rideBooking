"""
Simple test script to verify the API is working
Run this after starting the server with: python run.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_available_cabs():
    """Test available cabs endpoint"""
    print("\n2. Testing available cabs...")
    data = {
        "location": {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "address": "MG Road, Bangalore"
        }
    }
    response = requests.post(f"{BASE_URL}/cabs/available", json=data)
    print(f"Status: {response.status_code}")
    print(f"Available cabs: {len(response.json())}")
    for cab in response.json():
        print(f"  - {cab['name']}: {cab['available_count']} available, ETA {cab['eta_minutes']} min")
    return response.status_code == 200


def test_fare_estimate():
    """Test fare estimate endpoint"""
    print("\n3. Testing fare estimate...")
    data = {
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
    }
    response = requests.post(f"{BASE_URL}/fare/estimate", json=data)
    print(f"Status: {response.status_code}")
    fare = response.json()
    print(f"Fare estimate: ₹{fare['total']}")
    print(f"  Base fare: ₹{fare['base_fare']}")
    print(f"  Distance fare: ₹{fare['distance_fare']:.2f}")
    print(f"  Time fare: ₹{fare['time_fare']:.2f}")
    print(f"  Surge: {fare['surge_multiplier']}x")
    return response.status_code == 200


def test_book_ride():
    """Test booking a ride"""
    print("\n4. Testing ride booking...")
    data = {
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
    }
    response = requests.post(f"{BASE_URL}/rides/book", json=data)
    print(f"Status: {response.status_code}")
    ride = response.json()
    print(f"Ride booked! ID: {ride['ride_id']}")
    print(f"Status: {ride['status']}")
    print(f"Distance: {ride['distance_km']} km")
    print(f"Estimated fare: ₹{ride['fare']['total']}")
    return response.status_code == 201, ride['ride_id']


def test_assign_driver(ride_id):
    """Test driver assignment"""
    print(f"\n5. Testing driver assignment for ride {ride_id}...")
    response = requests.post(f"{BASE_URL}/rides/{ride_id}/assign-driver")
    print(f"Status: {response.status_code}")
    ride = response.json()
    driver = ride['driver']
    print(f"Driver assigned: {driver['name']}")
    print(f"Rating: {driver['rating']}/5.0")
    print(f"Vehicle: {driver['vehicle_color']} {driver['vehicle_model']}")
    print(f"Number: {driver['vehicle_number']}")
    print(f"ETA: {ride['eta_minutes']} minutes")
    return response.status_code == 200


def test_get_ride(ride_id):
    """Test getting ride details"""
    print(f"\n6. Testing get ride details for {ride_id}...")
    response = requests.get(f"{BASE_URL}/rides/{ride_id}")
    print(f"Status: {response.status_code}")
    ride = response.json()
    print(f"Ride status: {ride['status']}")
    return response.status_code == 200


def test_update_status(ride_id):
    """Test updating ride status"""
    print(f"\n7. Testing status update for ride {ride_id}...")
    data = {"status": "IN_PROGRESS"}
    response = requests.patch(f"{BASE_URL}/rides/{ride_id}/status", json=data)
    print(f"Status: {response.status_code}")
    ride = response.json()
    print(f"New status: {ride['status']}")
    return response.status_code == 200


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 Testing Cab Booking API")
    print("=" * 60)
    
    try:
        # Test basic endpoints
        if not test_health():
            print("❌ Health check failed!")
            return
        
        if not test_available_cabs():
            print("❌ Available cabs test failed!")
            return
        
        if not test_fare_estimate():
            print("❌ Fare estimate test failed!")
            return
        
        # Test ride booking flow
        success, ride_id = test_book_ride()
        if not success:
            print("❌ Ride booking failed!")
            return
        
        if not test_assign_driver(ride_id):
            print("❌ Driver assignment failed!")
            return
        
        if not test_get_ride(ride_id):
            print("❌ Get ride failed!")
            return
        
        if not test_update_status(ride_id):
            print("❌ Status update failed!")
            return
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running with: python run.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
