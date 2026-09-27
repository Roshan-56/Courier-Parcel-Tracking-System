"""Courier & Parcel Tracking System — Flask application.

Run with:  python app.py   (or via setup.bat)
The SQLite database lives next to this file and is auto-created + auto-seeded
on first run.
"""
import os
import random
import string
from collections import Counter
from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from models import STATUS_FLOW, Shipment, Staff, TrackingEvent, db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "courier.db")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "courier-tracking-demo-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Staff, int(user_id))

    register_routes(app)

    with app.app_context():
        db.create_all()
        # Auto-seed on first run (idempotent: only when tables are empty).
        from seed import seed_if_empty

        seed_if_empty()

    return app


def generate_tracking_no():
    """Generate a unique, human-friendly tracking number, e.g. CPX-8F3K9A2Q."""
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
        candidate = f"CPX-{code}"
        exists = Shipment.query.filter_by(tracking_no=candidate).first()
        if not exists:
            return candidate


def register_routes(app):
    # ----------------------------- Public ------------------------------- #
    @app.route("/", methods=["GET", "POST"])
    def index():
        """Public landing / tracking page."""
        shipment = None
        searched = False
        tracking_no = ""
        if request.method == "POST":
            searched = True
            tracking_no = (request.form.get("tracking_no") or "").strip().upper()
            if tracking_no:
                shipment = Shipment.query.filter_by(tracking_no=tracking_no).first()
        return render_template(
            "index.html",
            shipment=shipment,
            searched=searched,
            tracking_no=tracking_no,
            status_flow=STATUS_FLOW,
        )

    @app.route("/track/<tracking_no>")
    def track(tracking_no):
        """Direct link to a shipment's public timeline."""
        shipment = Shipment.query.filter_by(
            tracking_no=tracking_no.strip().upper()
        ).first()
        return render_template(
            "index.html",
            shipment=shipment,
            searched=True,
            tracking_no=tracking_no.upper(),
            status_flow=STATUS_FLOW,
        )

    # ------------------------------ Auth -------------------------------- #
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = request.form.get("password") or ""
            staff = Staff.query.filter_by(username=username).first()
            if staff and staff.check_password(password):
                login_user(staff)
                flash(f"Welcome back, {staff.full_name}!", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard"))
            flash("Invalid username or password.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    # ---------------------------- Staff area ---------------------------- #
    @app.route("/dashboard")
    @login_required
    def dashboard():
        shipments = Shipment.query.all()

        # Counts per status (keep the canonical order).
        raw_counts = Counter(s.status for s in shipments)
        status_counts = {status: raw_counts.get(status, 0) for status in STATUS_FLOW}

        # Shipments booked per day (by created_at) for the Chart.js line chart.
        per_day = Counter(s.created_at.strftime("%Y-%m-%d") for s in shipments)
        chart_labels = sorted(per_day.keys())
        chart_values = [per_day[day] for day in chart_labels]

        return render_template(
            "dashboard.html",
            total=len(shipments),
            status_counts=status_counts,
            chart_labels=chart_labels,
            chart_values=chart_values,
        )

    @app.route("/shipments")
    @login_required
    def shipments():
        status_filter = request.args.get("status", "")
        query = Shipment.query
        if status_filter in STATUS_FLOW:
            query = query.filter_by(status=status_filter)
        all_shipments = query.order_by(Shipment.created_at.desc()).all()
        return render_template(
            "shipments.html",
            shipments=all_shipments,
            status_flow=STATUS_FLOW,
            status_filter=status_filter,
        )

    @app.route("/shipments/new", methods=["GET", "POST"])
    @login_required
    def new_shipment():
        if request.method == "POST":
            sender = (request.form.get("sender") or "").strip()
            receiver = (request.form.get("receiver") or "").strip()
            origin = (request.form.get("origin") or "").strip()
            destination = (request.form.get("destination") or "").strip()

            if not all([sender, receiver, origin, destination]):
                flash("All fields are required.", "danger")
                return render_template("new_shipment.html", form=request.form)

            shipment = Shipment(
                tracking_no=generate_tracking_no(),
                sender=sender,
                receiver=receiver,
                origin=origin,
                destination=destination,
                status="Booked",
            )
            db.session.add(shipment)
            db.session.flush()  # assign shipment.id

            # First timeline entry: Booked.
            db.session.add(
                TrackingEvent(
                    shipment_id=shipment.id,
                    status="Booked",
                    location=origin,
                    timestamp=datetime.utcnow(),
                    note="Shipment booked and label created.",
                )
            )
            db.session.commit()
            flash(
                f"Shipment created with tracking number {shipment.tracking_no}.",
                "success",
            )
            return redirect(url_for("shipment_detail", shipment_id=shipment.id))

        return render_template("new_shipment.html", form={})

    @app.route("/shipments/<int:shipment_id>")
    @login_required
    def shipment_detail(shipment_id):
        shipment = db.get_or_404(Shipment, shipment_id)
        return render_template(
            "shipment_detail.html",
            shipment=shipment,
            status_flow=STATUS_FLOW,
        )

    @app.route("/shipments/<int:shipment_id>/events", methods=["POST"])
    @login_required
    def add_event(shipment_id):
        shipment = db.get_or_404(Shipment, shipment_id)
        status = (request.form.get("status") or "").strip()
        location = (request.form.get("location") or "").strip()
        note = (request.form.get("note") or "").strip()

        if status not in STATUS_FLOW:
            flash("Please choose a valid status.", "danger")
            return redirect(url_for("shipment_detail", shipment_id=shipment.id))
        if not location:
            flash("Location is required for a tracking event.", "danger")
            return redirect(url_for("shipment_detail", shipment_id=shipment.id))

        db.session.add(
            TrackingEvent(
                shipment_id=shipment.id,
                status=status,
                location=location,
                timestamp=datetime.utcnow(),
                note=note or None,
            )
        )
        # The shipment's current status reflects its latest event.
        shipment.status = status
        db.session.commit()
        flash("Tracking event added.", "success")
        return redirect(url_for("shipment_detail", shipment_id=shipment.id))

    # Make STATUS_FLOW available to every template (for nav/badges).
    @app.context_processor
    def inject_globals():
        return {"STATUS_FLOW": STATUS_FLOW}


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
