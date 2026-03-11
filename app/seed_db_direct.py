"""
Direct database seeding script - inserts data directly into database
"""

from database import SessionLocal, engine
from models import Base, User, Location, Asset, Maintenance, Report
from datetime import datetime, timedelta
import json

# Create tables
Base.metadata.create_all(bind=engine)

def seed_database():
    print("\n Seeding Database Directly...\n")

    db = SessionLocal()

    try:
        # =========================
        # 1. Create / Get Users
        # =========================
        print("Creating users...")

        users_data = [
            {
                "username": "testuser",
                "email": "testuser@airport.com",
                "full_name": "Test Admin User",
                "password": "testpass123",
                "role": "admin",
                "is_active": True
            },
            {
                "username": "manager1",
                "email": "manager1@airport.com",
                "full_name": "Operations Manager",
                "password": "manager123",
                "role": "manager",
                "is_active": True
            },
            {
                "username": "tech1",
                "email": "tech1@airport.com",
                "full_name": "Maintenance Technician",
                "password": "tech123",
                "role": "technician",
                "is_active": True
            },
            {
                "username": "viewer1",
                "email": "viewer1@airport.com",
                "full_name": "Report Viewer",
                "password": "viewer123",
                "role": "viewer",
                "is_active": True
            }
        ]

        user_ids = {}

        for user_data in users_data:
            user = db.query(User).filter(User.username == user_data["username"]).first()

            if not user:
                user = User(**user_data)
                db.add(user)
                db.flush()
                print(f"Created user: {user.username} ({user.role})")
            else:
                user.role = user_data["role"]
                print(f"Updated user: {user.username} ({user.role})")

            user_ids[user.username] = user.id

        # Default admin for asset creation
        admin_user_id = user_ids["testuser"]
        # =========================
        # 2. Locations
        # =========================
        print("\nCreating locations...")

        locations_data = [
            {"name": "Terminal 1", "location_type": "Terminal", "capacity": 5000, "description": "International Terminal"},
            {"name": "Terminal 2", "location_type": "Terminal", "capacity": 3500, "description": "Domestic Terminal"},
            {"name": "Runway 1", "location_type": "Runway", "capacity": None, "description": "Main runway for takeoff and landing"},
            {"name": "Cargo Terminal", "location_type": "Cargo", "capacity": 2000, "description": "Freight handling facility"},
        ]

        location_ids = []

        for loc_data in locations_data:
            location = db.query(Location).filter(Location.name == loc_data["name"]).first()
            if not location:
                location = Location(**loc_data)
                db.add(location)
                db.flush()
                print(f"Created location: {loc_data['name']}")
            else:
                print(f"Location exists: {loc_data['name']}")
            location_ids.append(location.id)

        # =========================
        # 3. Assets
        # =========================
        print("\nCreating assets...")

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
            asset = db.query(Asset).filter(Asset.asset_id == asset_data["asset_id"]).first()
            if not asset:
                asset = Asset(**asset_data, created_by=admin_user_id)
                db.add(asset)
                db.flush()
                print(f"Created asset: {asset_data['asset_name']}")
            else:
                print(f"Asset exists: {asset_data['asset_name']}")
            asset_ids.append(asset.id)

        # =========================
        # 4. Maintenance
        # =========================
        print("\nCreating maintenance records...")

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
            maintenance = db.query(Maintenance).filter(
                Maintenance.maintenance_id == maint_data["maintenance_id"]
            ).first()

            if not maintenance:
                maintenance = Maintenance(**maint_data, assigned_to=admin_user_id)
                db.add(maintenance)
                print(f"Created maintenance: {maint_data['maintenance_id']}")
            else:
                print(f"Maintenance exists: {maint_data['maintenance_id']}")

        # =========================
        # 5. Reports
        # =========================
        print("\nCreating reports...")

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
            }
        ]

        for report_data in reports_data:
            report = db.query(Report).filter(
                Report.report_id == report_data["report_id"]
            ).first()

            if not report:
                report = Report(**report_data, generated_by=admin_user_id)
                db.add(report)
                print(f"Created report: {report_data['report_name']}")
            else:
                print(f"Report exists: {report_data['report_name']}")

        # =========================
        # Commit Everything Once
        # =========================
        db.commit()

        print("\n Database Summary:")
        print(f"Locations: {db.query(Location).count()}")
        print(f"Assets: {db.query(Asset).count()}")
        print(f"Maintenance Records: {db.query(Maintenance).count()}")
        print(f"Reports: {db.query(Report).count()}")
        print(f"Users: {db.query(User).count()}")

        print("\n Database seeding completed successfully!")
        print("\nTest Credentials:")
        print("Username: testuser")
        print("Password: testpass123")
        print("Role: admin")

    except Exception as e:
        db.rollback()
        print(f"\n Error during seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()