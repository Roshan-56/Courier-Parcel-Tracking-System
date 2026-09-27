"""Demo data for the Courier & Parcel Tracking System.

`seed_if_empty()` is called automatically on first run (see app.create_app).
It is idempotent: it only inserts data when the main tables are empty, so
re-running the app never duplicates rows.

You can also run it directly to (re)seed:  python seed.py
"""
import random
from datetime import datetime, timedelta

from models import STATUS_FLOW, Shipment, Staff, TrackingEvent, db

# Demo staff accounts (username, full name, password).
DEMO_STAFF = [
    ("admin", "Alex Morgan", "admin123"),
    ("dispatch", "Priya Sharma", "dispatch123"),
]

CITIES = [
    "New York, NY",
    "Chicago, IL",
    "Los Angeles, CA",
    "Houston, TX",
    "Seattle, WA",
    "Atlanta, GA",
    "Denver, CO",
    "Miami, FL",
    "Boston, MA",
    "Phoenix, AZ",
]

SENDERS = [
    "Acme Supplies Co.",
    "TechHub Electronics",
    "Green Valley Farms",
    "Riverside Books",
    "Nova Fashion House",
    "Peak Outdoor Gear",
    "Sunrise Bakery",
    "BlueWave Cosmetics",
    "Ironclad Tools",
    "Meadow Toys",
]

RECEIVERS = [
    "Jordan Lee",
    "Casey Nguyen",
    "Sam Patel",
    "Taylor Brooks",
    "Morgan Diaz",
    "Riley Cooper",
    "Jamie Foster",
    "Avery Reed",
    "Drew Bennett",
    "Quinn Rivera",
    "Harper Simmons",
    "Rowan Clarke",
]

# Notes keyed by status, used to build a believable timeline.
STATUS_NOTES = {
    "Booked": [
        "Shipment booked and label created.",
        "Order received at origin facility.",
    ],
    "In Transit": [
        "Departed origin sorting center.",
        "Arrived at regional hub.",
        "In transit to destination city.",
        "Processed through distribution center.",
    ],
    "Out for Delivery": [
        "Loaded onto delivery vehicle.",
        "Out for delivery with local courier.",
    ],
    "Delivered": [
        "Delivered — left at front door.",
        "Delivered and signed for by recipient.",
    ],
}


def _tracking_no(seq):
    """Deterministic, readable tracking number for seeded rows."""
    return f"CPX-{1000 + seq:04d}DEMO"


def seed_if_empty():
    """Populate demo data only if there are no shipments yet."""
    if Staff.query.first() is None:
        for username, full_name, password in DEMO_STAFF:
            staff = Staff(username=username, full_name=full_name)
            staff.set_password(password)
            db.session.add(staff)
        db.session.commit()

    if Shipment.query.first() is not None:
        return  # already seeded

    rng = random.Random(42)  # deterministic demo data
    now = datetime.utcnow()

    # How far through the lifecycle each of the 25 shipments has progressed.
    # Spread across all four statuses for a realistic dashboard.
    progress_plan = (
        ["Booked"] * 5
        + ["In Transit"] * 8
        + ["Out for Delivery"] * 4
        + ["Delivered"] * 8
    )
    rng.shuffle(progress_plan)

    for seq, final_status in enumerate(progress_plan):
        origin, destination = rng.sample(CITIES, 2)
        # created_at spread over the last ~14 days so the daily chart has shape.
        created_at = now - timedelta(
            days=rng.randint(0, 13), hours=rng.randint(0, 23)
        )

        shipment = Shipment(
            tracking_no=_tracking_no(seq),
            sender=rng.choice(SENDERS),
            receiver=rng.choice(RECEIVERS),
            origin=origin,
            destination=destination,
            status=final_status,
            created_at=created_at,
        )
        db.session.add(shipment)
        db.session.flush()  # get shipment.id

        # Build the timeline up to (and including) the final status.
        stop_index = STATUS_FLOW.index(final_status)
        event_time = created_at
        for step in range(stop_index + 1):
            status = STATUS_FLOW[step]
            note = rng.choice(STATUS_NOTES[status])
            # Location: origin for early steps, destination near the end.
            if status == "Booked":
                location = origin
            elif status == "Delivered":
                location = destination
            elif status == "Out for Delivery":
                location = destination
            else:  # In Transit
                location = rng.choice(CITIES)

            db.session.add(
                TrackingEvent(
                    shipment_id=shipment.id,
                    status=status,
                    location=location,
                    timestamp=event_time,
                    note=note,
                )
            )
            # Each subsequent scan happens some hours later.
            event_time = event_time + timedelta(hours=rng.randint(6, 30))

    db.session.commit()
    print(
        f"Seeded {len(progress_plan)} shipments with tracking histories "
        f"and {len(DEMO_STAFF)} staff accounts."
    )


if __name__ == "__main__":
    # Allow standalone (re)seeding.
    from app import app

    with app.app_context():
        db.create_all()
        seed_if_empty()
