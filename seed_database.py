"""
Script to populate the database with sample data for testing.
Run this script after starting the FastAPI server to add test data.
"""

import requests
import json
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:8000"

# Test credentials
TEST_CREDENTIALS = {
    "username": "testuser",
    "password": "testpass123"
}

# Login and get token
def get_token():
    """Login and get authentication token"""
    try:
        response = requests.post(
            f"{API_URL}/auth/token",
            data=TEST_CREDENTIALS
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error getting token: {e}")
        return None


# Register test user
def register_test_user():
    """Register a test user with admin role"""
    try:
        response = requests.post(
            f"{API_URL}/users/",
            json={
                "username": TEST_CREDENTIALS["username"],
                "password": TEST_CREDENTIALS["password"],
                "email": "testuser@airport.com",
                "full_name": "Test Admin User",
                "role": "admin"
            }
        )
        if response.status_code == 200:
            print("✓ Test user registered successfully")
            return True
        elif response.status_code == 400:
            print("✓ Test user already exists (using existing)")
            return True
        else:
            print(f"User registration: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error registering user: {e}")
        return False


# Create sample locations
def create_locations(token):
    """Create sample locations"""
    locations = [
        {
            "name": "Terminal 1",
            "location_type": "Terminal",
            "capacity": 5000,
            "description": "International Terminal"
        },
        {
            "name": "Terminal 2",
            "location_type": "Terminal",
            "capacity": 3500,
            "description": "Domestic Terminal"
        },
        {
            "name": "Runway 1",
            "location_type": "Runway",
            "capacity": None,
            "description": "Main runway for takeoff and landing"
        },
        {
            "name": "Cargo Terminal",
            "location_type": "Cargo",
            "capacity": 2000,
            "description": "Freight handling facility"
        }
    ]

    headers = {"Authorization": f"Bearer {token}"}
    created = 0

    for location in locations:
        try:
            response = requests.post(
                f"{API_URL}/locations/",
                json=location,
                headers=headers
            )
            if response.status_code == 200:
                created += 1
                print(f"✓ Created location: {location['name']}")
            else:
                print(f"Failed to create {location['name']}: {response.status_code}")
        except Exception as e:
            print(f"Error creating location: {e}")

    return created


# Create sample assets
def create_assets(token, location_ids):
    """Create sample assets"""
    assets = [
        {
            "asset_id": "AST-001",
            "asset_name": "X-Ray Machine",
            "category": "Security",
            "location_id": location_ids[0],
            "status": "operational",
            "manufacturer": "Smiths Detection",
            "model": "HI-SCAN 6040",
            "serial_number": "XR-2024-001"
        },
        {
            "asset_id": "AST-002",
            "asset_name": "Conveyor Belt System",
            "category": "Baggage",
            "location_id": location_ids[1],
            "status": "operational",
            "manufacturer": "Vanderlande",
            "model": "ModuSys",
            "serial_number": "CB-2024-002"
        },
        {
            "asset_id": "AST-003",
            "asset_name": "Ground Support Vehicle",
            "category": "Ground Equipment",
            "location_id": location_ids[2],
            "status": "operational",
            "manufacturer": "TLD",
            "model": "TUG 45",
            "serial_number": "GSV-2024-003"
        },
        {
            "asset_id": "AST-004",
            "asset_name": "Cargo Loader",
            "category": "Cargo",
            "location_id": location_ids[3],
            "status": "maintenance",
            "manufacturer": "JBT AeroTech",
            "model": "NeoLoader 747",
            "serial_number": "CL-2024-004"
        }
    ]

    headers = {"Authorization": f"Bearer {token}"}
    created = 0

    for asset in assets:
        try:
            response = requests.post(
                f"{API_URL}/assets/",
                json=asset,
                headers=headers
            )
            if response.status_code == 200:
                created += 1
                print(f"✓ Created asset: {asset['asset_name']}")
            else:
                print(f"Failed to create {asset['asset_name']}: {response.status_code}")
        except Exception as e:
            print(f"Error creating asset: {e}")

    return created


# Create sample maintenance records
def create_maintenance(token, asset_ids):
    """Create sample maintenance records"""
    today = datetime.now()

    maintenance_records = [
        {
            "maintenance_id": "MNT-001",
            "asset_id": asset_ids[0],
            "maintenance_type": "preventive",
            "scheduled_date": (today + timedelta(days=5)).isoformat(),
            "status": "scheduled",
            "description": "Regular preventive maintenance",
            "estimated_cost": 500.00
        },
        {
            "maintenance_id": "MNT-002",
            "asset_id": asset_ids[1],
            "maintenance_type": "inspection",
            "scheduled_date": (today + timedelta(days=3)).isoformat(),
            "status": "in_progress",
            "description": "Safety inspection and calibration",
            "estimated_cost": 300.00
        },
        {
            "maintenance_id": "MNT-003",
            "asset_id": asset_ids[3],
            "maintenance_type": "repair",
            "scheduled_date": today.isoformat(),
            "status": "in_progress",
            "description": "Hydraulic system repair",
            "estimated_cost": 1500.00,
            "actual_cost": 1200.00
        }
    ]

    headers = {"Authorization": f"Bearer {token}"}
    created = 0

    for record in maintenance_records:
        try:
            response = requests.post(
                f"{API_URL}/maintenance/",
                json=record,
                headers=headers
            )
            if response.status_code == 200:
                created += 1
                print(f"✓ Created maintenance record: {record['maintenance_id']}")
            else:
                print(f"Failed to create {record['maintenance_id']}: {response.status_code}")
        except Exception as e:
            print(f"Error creating maintenance: {e}")

    return created


# Create sample reports
def create_reports(token):
    """Create sample reports"""
    reports = [
        {
            "report_id": "RPT-001",
            "report_name": "Asset Utilization Report",
            "report_type": "Analytics",
            "description": "Monthly asset utilization summary",
            "is_public": True,
            "data_json": json.dumps({
                "total_assets": 4,
                "operational": 3,
                "maintenance": 1,
                "utilization_rate": "87%"
            })
        },
        {
            "report_id": "RPT-002",
            "report_name": "Maintenance Schedule Report",
            "report_type": "Operations",
            "description": "Upcoming maintenance schedule",
            "is_public": False,
            "data_json": json.dumps({
                "scheduled": 2,
                "in_progress": 1,
                "total_cost": 2300.00
            })
        },
        {
            "report_id": "RPT-003",
            "report_name": "System Performance Report",
            "report_type": "Performance",
            "description": "System health and performance metrics",
            "is_public": True,
            "data_json": json.dumps({
                "uptime": "99.8%",
                "response_time": "45ms",
                "error_rate": "0.2%"
            })
        }
    ]

    headers = {"Authorization": f"Bearer {token}"}
    created = 0

    for report in reports:
        try:
            response = requests.post(
                f"{API_URL}/reports/",
                json=report,
                headers=headers
            )
            if response.status_code == 200:
                created += 1
                print(f"✓ Created report: {report['report_name']}")
            else:
                print(f"Failed to create {report['report_name']}: {response.status_code}")
        except Exception as e:
            print(f"Error creating report: {e}")

    return created


# Get all resources for verification
def verify_data(token):
    """Verify created data"""
    headers = {"Authorization": f"Bearer {token}"}

    try:
        locations = requests.get(f"{API_URL}/locations/", headers=headers).json()
        assets = requests.get(f"{API_URL}/assets/", headers=headers).json()
        maintenance = requests.get(f"{API_URL}/maintenance/", headers=headers).json()
        reports = requests.get(f"{API_URL}/reports/", headers=headers).json()

        print("\n📊 Database Summary:")
        print(f"  • Locations: {len(locations)}")
        print(f"  • Assets: {len(assets)}")
        print(f"  • Maintenance Records: {len(maintenance)}")
        print(f"  • Reports: {len(reports)}")

        return locations, assets, maintenance
    except Exception as e:
        print(f"Error verifying data: {e}")
        return None, None, None


# Main execution
def main():
    print("🚀 Airport Assets Management - Database Seeding Script\n")

    # Step 1: Register test user
    print("1️⃣  Registering test user...")
    register_test_user()

    # Step 2: Get token
    print("\n2️⃣  Authenticating...")
    token = get_token()
    if not token:
        print("❌ Failed to get authentication token")
        return
    print("✓ Authentication successful")

    # Step 3: Create locations
    print("\n3️⃣  Creating locations...")
    created_locations = create_locations(token)
    print(f"Created {created_locations} locations\n")

    # Get location IDs
    headers = {"Authorization": f"Bearer {token}"}
    locations_response = requests.get(f"{API_URL}/locations/", headers=headers)
    locations = locations_response.json()
    location_ids = [loc["id"] for loc in locations]

    # Step 4: Create assets
    print("4️⃣  Creating assets...")
    created_assets = create_assets(token, location_ids)
    print(f"Created {created_assets} assets\n")

    # Get asset IDs
    assets_response = requests.get(f"{API_URL}/assets/", headers=headers)
    assets = assets_response.json()
    asset_ids = [asset["id"] for asset in assets]

    # Step 5: Create maintenance records
    print("5️⃣  Creating maintenance records...")
    created_maintenance = create_maintenance(token, asset_ids)
    print(f"Created {created_maintenance} maintenance records\n")

    # Step 6: Create reports
    print("6️⃣  Creating reports...")
    created_reports = create_reports(token)
    print(f"Created {created_reports} reports\n")

    # Step 7: Verify data
    print("7️⃣  Verifying data...")
    verify_data(token)

    print("\n✅ Database seeding completed successfully!")
    print("\nYou can now login with:")
    print(f"  Username: {TEST_CREDENTIALS['username']}")
    print(f"  Password: {TEST_CREDENTIALS['password']}")


if __name__ == "__main__":
    main()

