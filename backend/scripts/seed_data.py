import sys
from pathlib import Path

# Make sure backend is in sys.path when running as a script
sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

from app.db.session import SessionLocal, engine
from app.models import Base, Region, Location, Share

def seed():
    db = SessionLocal()
    try:
        # Drop + recreate for clean dev seeding
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # Regions
        na = Region(code="NA", name="North America")
        eu = Region(code="EU", name="Europe")
        as_ = Region(code="AS", name="Asia")

        db.add_all([na, eu, as_])
        db.flush()

        # Locations
        halifax = Location(code="HFX", name="Halifax", region=na)
        tor = Location(code="NYC", name="Toronto", region=na)
        london = Location(code="LON", name="London", region=eu)
        manila = Location(code="mnl", name="Manila", region=as_)

        db.add_all([halifax, tor, london, manila])
        db.flush()

        # Shares
        share1 = Share(unc_path="\\\\hfxshare\\share1", location=halifax)
        share2 = Share(unc_path="\\\\torshare\\share2", location=tor)
        share3 = Share(unc_path="\\\\lonshare\\share3", location=london)
        share4 = Share(unc_path="\\\\mnlshare\\share4", location=manila)

        db.add_all([share1, share2, share3, share4])
        db.commit()
        print("✅ Seed data inserted successfully.")

    except Exception as e:
        print("❌ Error seeding data:", e)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
