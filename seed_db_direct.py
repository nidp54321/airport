"""
Direct database seeding script - inserts data directly into database
"""

from app.database import SessionLocal, engine
from app.models import Base, User, Location, Asset, Maintenance, Report
from app.auth import get_password_hash
from datetime import datetime, timedelta
import json

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_database():
    print("\n🌱 Seeding Database Directly...\n")
    
    try:
        # 1. Create test user with admin role
        print("1️⃣  Creating test user...")
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if not existing_user:
            test_user = User(
                username="testuser",
                email="testuser@airport.com",
                full_name="Test Admin User",
                hashed_password=get_password_hash("testpass123"),
                role="admin",
                is_active=True
            )
            db.add(test_user)
            db.commit()
            print("✓ Test user created (admin)")
        else:
            # Update existing user to be admin
            existing_user.role = "admin"
            db.commit()
            print("✓ Test user updated to admin role")

        # 2. Create locations
        print("\n2️⃣  Creating locations...")
        locations_data = [
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
        
        location_ids = []
        for loc_data in locations_data:
            existing = db.query(Location).filter(Location.name == loc_data["name"]).first()
            if not existing:
                location = Location(**loc_data)
                db.add(location)
                db.commit()
                location_ids.append(location.id)
                print(f"✓ Created location: {loc_data['name']}")
            else:
                location_ids.append(existing.id)
                print(f"✓ Location exists: {loc_data['name']}")

        # 3. Create assets
        print("\n3️⃣  Creating assets...")
        assets_data = [
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
        
        asset_ids = []
        for asset_data in assets_data:
            existing = db.query(Asset).filter(Asset.asset_id == asset_data["asset_id"]).first()
            if not existing:
                asset = Asset(**asset_data, created_by=existing_user.id if existing_user else None)
                db.add(asset)
                db.commit()
                asset_ids.append(asset.id)
                print(f"✓ Created asset: {asset_data['asset_name']}")
            else:
                asset_ids.append(existing.id)
                print(f"✓ Asset exists: {asset_data['asset_name']}")

        # 4. Create maintenance records
        print("\n4️⃣  Creating maintenance records...")
        today = datetime.now()
        maintenance_data = [
            {
                "maintenance_id": "MNT-001",
                "asset_id": asset_ids[0],
                "maintenance_type": "preventive",
                "scheduled_date": today + timedelta(days=5),
                "status": "scheduled",
                "description": "Regular preventive maintenance",
                "estimated_cost": 500.00
            },
            {
                "maintenance_id": "MNT-002",
                "asset_id": asset_ids[1],
                "maintenance_type": "inspection",
                "scheduled_date": today + timedelta(days=3),
                "status": "in_progress",
                "description": "Safety inspection and calibration",
                "estimated_cost": 300.00
            },
            {
                "maintenance_id": "MNT-003",
                "asset_id": asset_ids[3],
                "maintenance_type": "repair",
                "scheduled_date": today,
                "status": "in_progress",
                "description": "Hydraulic system repair",
                "estimated_cost": 1500.00,
                "actual_cost": 1200.00
            }
        ]
        
        for maint_data in maintenance_data:
            existing = db.query(Maintenance).filter(Maintenance.maintenance_id == maint_data["maintenance_id"]).first()
            if not existing:
                maintenance = Maintenance(**maint_data, assigned_to=existing_user.id if existing_user else None)
                db.add(maintenance)
                db.commit()
                print(f"✓ Created maintenance: {maint_data['maintenance_id']}")
            else:
                print(f"✓ Maintenance exists: {maint_data['maintenance_id']}")

        # 5. Create reports
        print("\n5️⃣  Creating reports...")
        reports_data = [
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
        
        for report_data in reports_data:
            existing = db.query(Report).filter(Report.report_id == report_data["report_id"]).first()
            if not existing:
                report = Report(**report_data, generated_by=existing_user.id if existing_user else None)
                db.add(report)
                db.commit()
                print(f"✓ Created report: {report_data['report_name']}")
            else:
                print(f"✓ Report exists: {report_data['report_name']}")

        # 6. Verify
        print("\n6️⃣  Database Summary:")
        print(f"  • Locations: {db.query(Location).count()}")
        print(f"  • Assets: {db.query(Asset).count()}")
        print(f"  • Maintenance Records: {db.query(Maintenance).count()}")
        print(f"  • Reports: {db.query(Report).count()}")
        print(f"  • Users: {db.query(User).count()}")

        print("\n✅ Database seeding completed successfully!")
        print("\nTest Credentials:")
        print("  Username: testuser")
        print("  Password: testpass123")
        print("  Role: admin")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

