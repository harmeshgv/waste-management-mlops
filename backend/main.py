import math
from PIL import Image

from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text

from backend.db.db import init_db, engine
from backend.models.efficientnet_model import Model
from backend.utils.logger import logger
from contextlib import asynccontextmanager

# -----------------------------
# 🌍 Distance (Haversine)
# -----------------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


# -----------------------------
# 🧭 Route builder (greedy)
# -----------------------------
def build_route(tasks, start):
    route = []
    current = start
    remaining = tasks.copy()

    while remaining:
        next_task = min(
            remaining,
            key=lambda t: (
                -t["severity"],
                distance(current[0], current[1], t["lat"], t["lng"])
            )
        )
        route.append(next_task)
        current = (next_task["lat"], next_task["lng"])
        remaining.remove(next_task)

    return route


# -----------------------------
# 🧹 Deduplicate tasks
# -----------------------------
def deduplicate(tasks):
    unique = {}
    for t in tasks:
        key = (t["lat"], t["lng"])
        if key not in unique or t["severity"] > unique[key]["severity"]:
            unique[key] = t
    return list(unique.values())


# -----------------------------
# ⚙️ Config
# -----------------------------
severity_map = {
    "clean": 0,
    "construction-waste": 2,
    "open_litter": 3,
    "packed": 1
}

CITY_START = {
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777)
}

LOCATION_MAP = {
    "Chennai": {
        "Perumbakkam": (12.9150, 80.2290),
        "Medavakkam": (12.9180, 80.1920),
        "Sholinganallur": (12.9010, 80.2279),
        "T Nagar": (13.0418, 80.2341),
        "Velachery": (12.9791, 80.2212),
        "Tambaram": (12.9249, 80.1000),
        "Adyar": (13.0067, 80.2570),
        "Anna Nagar": (13.0850, 80.2101)
    },
    "Bangalore": {
        "Whitefield": (12.9698, 77.7500),
        "Electronic City": (12.8399, 77.6770),
        "Indiranagar": (12.9784, 77.6408),
        "Koramangala": (12.9279, 77.6271),
        "BTM Layout": (12.9166, 77.6101),
        "Yelahanka": (13.1007, 77.5963),
        "Hebbal": (13.0358, 77.5970),
        "Marathahalli": (12.9591, 77.6974)
    },
    "Mumbai": {
        "Andheri": (19.1136, 72.8697),
        "Bandra": (19.0596, 72.8295),
        "Dadar": (19.0184, 72.8429),
        "Powai": (19.1176, 72.9060),
        "Borivali": (19.2307, 72.8567),
        "Vashi": (19.0771, 72.9986),
        "Colaba": (18.9067, 72.8147),
        "Kurla": (19.0728, 72.8826)
    }
}

# -----------------------------
# 🚀 App
# -----------------------------
model_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_instance
    init_db()
    model_instance = Model()
    logger.info("✅ System initialized")
    yield


app = FastAPI(
    title="Waste Management ML API",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def dashboard():
    return FileResponse("/app/index.html")


@app.get("/health")
async def health_check():
    return {"status": "running"}


# -----------------------------
# 📸 Predict & Store
# -----------------------------
@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    locality: str = Form(...),
    city: str = Form(...)
):
    try:
        img = Image.open(file.file).convert("RGB")
    except:
        raise HTTPException(400, "Invalid image")

    prediction = model_instance.predict(img)
    label = prediction if isinstance(prediction, str) else prediction.get("label")
    severity = severity_map.get(label, 0)

    if city in LOCATION_MAP and locality in LOCATION_MAP[city]:
        lat, lng = LOCATION_MAP[city][locality]
    else:
        lat, lng = None, None

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO tasks (city, waste_type, severity, lat, lng, status)
            VALUES (:city, :waste_type, :severity, :lat, :lng, 'pending')
        """), {
            "city": city,
            "waste_type": label,
            "severity": severity,
            "lat": lat,
            "lng": lng
        })

    return {"prediction": label, "severity": severity}


# -----------------------------
# 📋 Get Tasks
# -----------------------------
@app.get("/tasks")
async def get_tasks(city: str = Query(...)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, city, waste_type, severity, lat, lng, status, created_at
            FROM tasks
            WHERE city = :city AND status = 'pending'
            ORDER BY severity DESC, created_at ASC
        """), {"city": city})

        tasks = [dict(r._mapping) for r in result]

    return {"count": len(tasks), "tasks": tasks}


# -----------------------------
# 🧭 Route
# -----------------------------
@app.get("/route")
async def get_route(city: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, waste_type, severity, lat, lng
            FROM tasks
            WHERE city = :city AND status = 'pending'
        """), {"city": city})

        tasks = [dict(r._mapping) for r in result]

    if not tasks:
        return {"route": []}

    tasks = deduplicate(tasks)

    start = CITY_START.get(city, (tasks[0]["lat"], tasks[0]["lng"]))

    ordered = build_route(tasks, start)

    return {"route": ordered}


# -----------------------------
# ✅ Complete Task
# -----------------------------
@app.post("/complete")
async def complete_task(task_id: int):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE tasks
            SET status = 'completed'
            WHERE id = :id
        """), {"id": task_id})

    return {"message": "Task completed"}
