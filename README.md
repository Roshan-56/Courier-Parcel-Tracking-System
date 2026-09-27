The link of the Website is : https://courier-parcel-tracking-system.onrender.com/
<<<<<<< HEAD
# 📦 Courier & Parcel Tracking System

A simple courier/parcel tracking web app built with **Flask + SQLite (SQLAlchemy)**.

- **Public tracking page** — anyone can enter a tracking number and view the parcel's status timeline (no login needed).
- **Staff area** (login required) — create shipments (with an auto-generated unique tracking number), add tracking events that build a status timeline, and view a dashboard with per-status counts and a shipments-per-day chart.

Status lifecycle: **Booked → In Transit → Out for Delivery → Delivered**

---

## ✅ Prerequisites

You only need **Python 3.9 or newer** installed on Windows.

- Download it from <https://www.python.org/downloads/>
- During installation, **check the box "Add Python to PATH"**.

That's it — no database server, no Node, nothing else to install.

---

## 🚀 Setup (one command)

1. Unzip this folder anywhere.
2. Double-click **`setup.bat`** (or run it from a terminal).

That single command will:

1. create a virtual environment (`venv`),
2. install the pinned dependencies from `requirements.txt`,
3. create the SQLite database and **automatically load demo data** on first run,
4. start the app.

When it finishes, open your browser at:

> **http://127.0.0.1:5000**

To stop the server, press **CTRL+C** in the terminal window.

---

## 🔑 Demo login accounts

| Username   | Password       | Name          |
|------------|----------------|---------------|
| `admin`    | `admin123`     | Alex Morgan   |
| `dispatch` | `dispatch123`  | Priya Sharma  |

Click **Staff Login** in the top-right to sign in.

---

## 👀 What you should see (demo data)

On first launch the database is seeded automatically with:

- **25 shipments** spread across all four statuses (Booked, In Transit, Out for Delivery, Delivered), each with a realistic multi-step tracking history.
- **2 staff accounts** (see the table above).

Things to try:

- **Public tracking** — on the home page, enter a demo tracking number such as
  `CPX-1000DEMO`, `CPX-1007DEMO`, or `CPX-1015DEMO` and click **Track** to see the timeline.
  (Demo tracking numbers run from `CPX-1000DEMO` to `CPX-1024DEMO`.)
- **Dashboard** — after logging in, the dashboard shows a count card for each status
  and a **Shipments Booked per Day** line chart (Chart.js).
- **Shipments** — browse/filter all shipments by status; click **Manage** to open one.
- **New Shipment** — create a parcel; a unique tracking number like `CPX-8F3K9A2Q`
  is generated automatically and a first *Booked* event is recorded.
- **Add tracking events** — on a shipment's page, add events (In Transit, Out for
  Delivery, Delivered) and watch the timeline grow. The shipment's status updates
  to match its latest event.

---

## 🗂️ Project structure

```
Courier & Parcel Tracking System/
├── app.py               # Flask app: routes, login, tracking-number generator
├── models.py            # SQLAlchemy models: Staff, Shipment, TrackingEvent
├── seed.py              # Demo data (auto-loaded on first run; idempotent)
├── requirements.txt     # Pinned dependencies
├── setup.bat            # One-command setup + run (Windows)
├── README.md
├── .gitignore
└── templates/           # Bootstrap UI (Jinja2)
    ├── base.html
    ├── index.html          # public tracking page
    ├── login.html
    ├── dashboard.html      # counts + Chart.js chart
    ├── shipments.html      # staff shipment list
    ├── new_shipment.html
    └── shipment_detail.html
```

The SQLite database file (`courier.db`) is created next to `app.py` on first run.
It is intentionally **not** committed — the demo data ships as source in `seed.py`
and is loaded automatically, so a fresh copy always has data. To reset everything,
just delete `courier.db` and start the app again.

---

## 🛠️ Running manually (optional)

If you'd rather not use `setup.bat`:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.
=======
# Courier-Parcel-Tracking-System
>>>>>>> 767bb386e7d1acc910f2b67efe3aa1ecbdd3877a
