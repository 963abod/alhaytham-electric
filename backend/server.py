from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import List

import bcrypt
import jwt
from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALG = "HS256"
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "adnan_homs")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

ROOT_DIR = Path(__file__).parent
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
api = APIRouter(prefix="/api")
security = HTTPBearer()
logger = logging.getLogger(__name__)

def hash_pw(p: str) -> str:
    return bcrypt.hashpw(p.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_pw(p: str, h: str) -> bool:
    return bcrypt.checkpw(p.encode("utf-8"), h.encode("utf-8"))

def create_token() -> str:
    payload = {
        "sub": ADMIN_USERNAME,
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

async def require_admin(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[JWT_ALG])
        if payload.get("role") != "admin":
            raise ValueError
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="غير مصرح")
      class LoginIn(BaseModel):
    username: str
    password: str

class WhyPoint(BaseModel):
    title: str
    text: str = ""

class SettingsIn(BaseModel):
    site_name: str
    tagline: str
    description: str
    about_text: str
    phone: str
    whatsapp: str
    area_text: str
    footer_text: str = ""
    why_points: List[WhyPoint] = []

class ServiceIn(BaseModel):
    title: str
    description: str = ""
    icon: str = "Zap"

class ProductIn(BaseModel):
    name: str
    description: str = ""
    image: str = ""

class WorkIn(BaseModel):
    title: str = ""
    image: str

class SocialIn(BaseModel):
    platform: str
    url: str

@api.post("/auth/login")
async def login(data: LoginIn):
    admin = await db.admins.find_one({"username": data.username})
    if not admin or not verify_pw(data.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")
    return {"token": create_token(), "username": data.username}

@api.get("/auth/me")
async def me(admin=Depends(require_admin)):
    return {"username": admin["sub"], "role": "admin"}
@api.get("/content")
async def get_content():
    settings = await db.settings.find_one({"key": "main"}, {"_id": 0})
    services = await db.services.find({}, {"_id": 0}).to_list(200)
    products = await db.products.find({}, {"_id": 0}).to_list(200)
    works = await db.works.find({}, {"_id": 0}).to_list(200)
    social = await db.social_links.find({}, {"_id": 0}).to_list(50)

    return {
        "settings": settings,
        "services": services,
        "products": products,
        "works": works,
        "social_links": social,
    }

@api.put("/admin/settings")
async def update_settings(data: SettingsIn, admin=Depends(require_admin)):
    doc = data.model_dump()
    doc["key"] = "main"
    await db.settings.update_one({"key": "main"}, {"$set": doc}, upsert=True)
    return doc

async def _create(collection: str, doc: dict):
    doc["id"] = str(uuid.uuid4())
    await db[collection].insert_one(doc)
    doc.pop("_id", None)
    return doc

async def _update(collection: str, item_id: str, doc: dict):
    res = await db[collection].update_one({"id": item_id}, {"$set": doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="العنصر غير موجود")
    doc["id"] = item_id
    return doc

async def _delete(collection: str, item_id: str):
    res = await db[collection].delete_one({"id": item_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="العنصر غير موجود")
    return {"deleted": True}

@api.post("/admin/services")
async def create_service(data: ServiceIn, admin=Depends(require_admin)):
    return await _create("services", data.model_dump())

@api.put("/admin/services/{item_id}")
async def update_service(item_id: str, data: ServiceIn, admin=Depends(require_admin)):
    return await _update("services", item_id, data.model_dump())

@api.delete("/admin/services/{item_id}")
async def delete_service(item_id: str, admin=Depends(require_admin)):
    return await _delete("services", item_id)
@api.post("/admin/products")
async def create_product(data: ProductIn, admin=Depends(require_admin)):
    return await _create("products", data.model_dump())

@api.put("/admin/products/{item_id}")
async def update_product(item_id: str, data: ProductIn, admin=Depends(require_admin)):
    return await _update("products", item_id, data.model_dump())

@api.delete("/admin/products/{item_id}")
async def delete_product(item_id: str, admin=Depends(require_admin)):
    return await _delete("products", item_id)

@api.post("/admin/works")
async def create_work(data: WorkIn, admin=Depends(require_admin)):
    return await _create("works", data.model_dump())

@api.put("/admin/works/{item_id}")
async def update_work(item_id: str, data: WorkIn, admin=Depends(require_admin)):
    return await _update("works", item_id, data.model_dump())

@api.delete("/admin/works/{item_id}")
async def delete_work(item_id: str, admin=Depends(require_admin)):
    return await _delete("works", item_id)

@api.post("/admin/social-links")
async def create_social(data: SocialIn, admin=Depends(require_admin)):
    return await _create("social_links", data.model_dump())

@api.put("/admin/social-links/{item_id}")
async def update_social(item_id: str, data: SocialIn, admin=Depends(require_admin)):
    return await _update("social_links", item_id, data.model_dump())

@api.delete("/admin/social-links/{item_id}")
async def delete_social(item_id: str, admin=Depends(require_admin)):
    return await _delete("social_links", item_id)

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

@api.post("/admin/upload")
async def upload_image(
    file: UploadFile = File(...),
    admin=Depends(require_admin)
):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="صيغة الصورة غير مدعومة")

    name = f"{uuid.uuid4().hex}{ext}"
    content = await file.read()
    (UPLOAD_DIR / name).write_bytes(content)

    return {"url": f"/api/uploads/{name}"}
DEFAULT_SETTINGS = {
    "key": "main",
    "site_name": "ورشة الهيثم للكهرباء",
    "tagline": "طاقة أقوى، حلول أذكى، وخدمة تعتمد عليها",
    "description": "تنفيذ وصيانة حلول الكهرباء والطاقة الشمسية، وتوفير مستلزمات الطاقة الشمسية في حمص وضواحيها.",
    "about_text": "ورشة الهيثم للكهرباء ورشة متخصصة في تنفيذ وصيانة الأعمال الكهربائية وأنظمة الطاقة الشمسية، مع توفير منتجات ومستلزمات الطاقة الشمسية بجودة موثوقة في حمص وضواحيها.",
    "phone": "0982506890",
    "whatsapp": "963982506890",
    "area_text": "نخدم مدينة حمص وضواحيها",
    "footer_text": "© 2026 ورشة الهيثم للكهرباء — جميع الحقوق محفوظة",
    "why_points": [
        {"title": "خبرة في الكهرباء والطاقة الشمسية", "text": "سنوات من العمل الميداني في التنفيذ والصيانة."},
        {"title": "منتجات وحلول متكاملة", "text": "من الألواح إلى البطاريات والإنفرترات، كل ما تحتاجه في مكان واحد."},
        {"title": "خدمة في حمص وضواحيها", "text": "استجابة سريعة وخدمة ميدانية داخل حمص وما حولها."},
    ],
}

DEFAULT_SERVICES = [
    {"title": "صيانة الأعطال الكهربائية", "description": "تشخيص وإصلاح الأعطال الكهربائية المنزلية والتجارية بسرعة ودقة.", "icon": "Wrench"},
    {"title": "تركيب لوحات الكهرباء", "description": "تصميم وتركيب لوحات التوزيع الكهربائية وفق معايير السلامة.", "icon": "CircuitBoard"},
    {"title": "تركيب أنظمة الطاقة الشمسية", "description": "دراسة وتركيب أنظمة طاقة شمسية متكاملة للمنازل والمنشآت.", "icon": "Sun"},
    {"title": "صيانة أنظمة الطاقة الشمسية", "description": "فحص دوري وصيانة شاملة للألواح والأنظمة لضمان أفضل أداء.", "icon": "SunMedium"},
    {"title": "تركيب البطاريات والإنفرترات", "description": "تركيب وبرمجة البطاريات والإنفرترات بمختلف الاستطاعات.", "icon": "BatteryCharging"},
]

DEFAULT_PRODUCTS = [
    {"name": "ألواح شمسية", "description": "ألواح شمسية عالية الكفاءة باستطاعات متعددة.", "image": "https://images.unsplash.com/photo-1724041875334-0a6397111c7e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwxfHxzb2xhciUyMHBhbmVscyUyMGluc3RhbGxhdGlvbnxlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85"},
    {"name": "بطاريات ليثيوم", "description": "بطاريات ليثيوم طويلة العمر لتخزين الطاقة بكفاءة.", "image": "https://images.unsplash.com/photo-1780445392417-68b9dccc45f2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTN8MHwxfHNlYXJjaHw0fHxpbnZlcnRlciUyMGJhdHRlcnklMjBzb2xhcnxlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85"},
    {"name": "كابلات", "description": "كابلات كهربائية وشمسية بمقاطع وجودات متنوعة.", "image": "https://images.unsplash.com/photo-1635335874521-7987db781153?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxlbGVjdHJpY2FsJTIwd2lyaW5nJTIwd29ya3xlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85"},
    {"name": "بطاريات", "description": "بطاريات تخزين بأنواع وسعات مختلفة تناسب جميع الأنظمة.", "image": "https://images.unsplash.com/photo-1780445392417-68b9dccc45f2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTN8MHwxfHNlYXJjaHw0fHxpbnZlcnRlciUyMGJhdHRlcnklMjBzb2xhcnxlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85"},
    {"name": "إنفرترات", "description": "إنفرترات باستطاعات متعددة مع ضمان وجودة عالية.", "image": "https://images.unsplash.com/photo-1758101755915-462eddc23f57?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxlbGVjdHJpY2FsJTIwd2lyaW5nJTIwd29ya3xlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85"},
]
DEFAULT_WORKS = [
    {
        "title": "تركيب نظام طاقة شمسية",
        "image": "https://images.unsplash.com/photo-1668097613572-40b7c11c8727?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwyfHxzb2xhciUyMHBhbmVscyUyMGluc3RhbGxhdGlvbnxlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85",
    },
    {
        "title": "تنفيذ لوحة كهربائية",
        "image": "https://images.unsplash.com/photo-1635335874521-7987db781153?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxlbGVjdHJpY2FsJTIwd2lyaW5nJTIwd29ya3xlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85",
    },
    {
        "title": "ألواح شمسية",
        "image": "https://images.unsplash.com/photo-1724041875334-0a6397111c7e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwxfHxzb2xhciUyMHBhbmVscyUyMGluc3RhbGxhdGlvbnxlbnwwfHx8fDE3ODY2NzE2ODh8MA&ixlib=rb-4.1.0&q=85",
    },
    {
        "title": "إنارة داخلية",
        "image": "https://images.unsplash.com/photo-1642976975710-1d8890dbf5ab?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBtb2Rlcm4lMjBob3VzZSUyMGxpZ2h0aW5nfGVufDB8fHx8MTc4NjY3MTY4OHww&ixlib=rb-4.1.0&q=85",
    },
]

async def seed_admin():
    existing = await db.admins.find_one({"username": ADMIN_USERNAME})

    if existing is None:
        await db.admins.insert_one({
            "username": ADMIN_USERNAME,
            "password_hash": hash_pw(ADMIN_PASSWORD),
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Admin user seeded")

    elif not verify_pw(ADMIN_PASSWORD, existing["password_hash"]):
        await db.admins.update_one(
            {"username": ADMIN_USERNAME},
            {"$set": {"password_hash": hash_pw(ADMIN_PASSWORD)}},
        )
        logger.info("Admin password updated from env")
      async def seed_content():
    if await db.settings.count_documents({"key": "main"}) == 0:
        await db.settings.insert_one(dict(DEFAULT_SETTINGS))

    if await db.services.count_documents({}) == 0:
        await db.services.insert_many([
            {**s, "id": str(uuid.uuid4())} for s in DEFAULT_SERVICES
        ])

    if await db.products.count_documents({}) == 0:
        await db.products.insert_many([
            {**p, "id": str(uuid.uuid4())} for p in DEFAULT_PRODUCTS
        ])

    if await db.works.count_documents({}) == 0:
        await db.works.insert_many([
            {**w, "id": str(uuid.uuid4())} for w in DEFAULT_WORKS
        ])


@app.on_event("startup")
async def startup():
    await seed_admin()
    await seed_content()


app.include_router(api)
app.mount(
    "/api/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
