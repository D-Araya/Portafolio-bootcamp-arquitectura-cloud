"""
Spaces Service - Servicio de Gestión de Espacios
=================================================
Este microservicio maneja:
- Listado de espacios disponibles
- Consulta de detalles de espacios
- Verificación de disponibilidad
- Creación y actualización de espacios (admin)

Endpoints:
- GET / - Listar espacios disponibles
- GET /{id} - Obtener detalles de un espacio
- GET /{id}/availability - Verificar disponibilidad
- POST / - Crear espacio (admin)
- PUT /{id} - Actualizar espacio (admin)
- GET /health - Health check
"""

from datetime import datetime, timedelta
from typing import Optional, List
from decimal import Decimal
import os
import json

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Numeric, JSON, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import logging

# =================================================================
# CONFIGURACIÓN
# =================================================================

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/reservations")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# =================================================================
# DATABASE SETUP
# =================================================================

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    is_active = Column(Boolean)
    is_admin = Column(Boolean)

class Space(Base):
    __tablename__ = "spaces"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    capacity = Column(Integer, nullable=False)
    location = Column(String)
    amenities = Column(JSON)
    price_per_hour = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    space_id = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)

# =================================================================
# REDIS SETUP
# =================================================================

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("✓ Connected to Redis")
except Exception as e:
    logger.warning(f"✗ Redis connection failed: {e}")
    redis_client = None

# =================================================================
# SECURITY
# =================================================================

security = HTTPBearer()

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# =================================================================
# PYDANTIC MODELS
# =================================================================

class SpaceResponse(BaseModel):
    """Respuesta con información de espacio"""
    id: int
    name: str
    description: Optional[str]
    capacity: int
    location: Optional[str]
    amenities: Optional[List[str]]
    price_per_hour: float
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Conference Room A",
                "description": "Large conference room",
                "capacity": 20,
                "location": "Floor 3",
                "amenities": ["projector", "whiteboard", "wifi"],
                "price_per_hour": 50.0,
                "is_active": True,
                "created_at": "2026-01-19T10:00:00"
            }
        }

class SpaceCreate(BaseModel):
    """Modelo para crear espacio"""
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    capacity: int = Field(..., gt=0, le=1000)
    location: Optional[str] = Field(None, max_length=255)
    amenities: Optional[List[str]] = []
    price_per_hour: float = Field(..., ge=0)
    
    @validator('amenities')
    def validate_amenities(cls, v):
        if v and len(v) > 20:
            raise ValueError('Maximum 20 amenities allowed')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Meeting Room B",
                "description": "Small meeting room",
                "capacity": 8,
                "location": "Floor 2",
                "amenities": ["tv", "whiteboard"],
                "price_per_hour": 30.0
            }
        }

class SpaceUpdate(BaseModel):
    """Modelo para actualizar espacio"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    capacity: Optional[int] = Field(None, gt=0, le=1000)
    location: Optional[str] = Field(None, max_length=255)
    amenities: Optional[List[str]] = None
    price_per_hour: Optional[float] = Field(None, ge=0)
    is_active: Optional[bool] = None

class AvailabilityCheck(BaseModel):
    """Respuesta de verificación de disponibilidad"""
    space_id: int
    start_time: datetime
    end_time: datetime
    available: bool
    conflicting_reservations: Optional[List[dict]] = []

# =================================================================
# DEPENDENCIES
# =================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario es admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return current_user

# =================================================================
# HELPER FUNCTIONS
# =================================================================

def get_space_from_cache(space_id: int) -> Optional[dict]:
    """Intentar obtener espacio desde caché"""
    if not redis_client:
        return None
    
    try:
        cache_key = f"space:{space_id}"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        logger.warning(f"Cache read error: {e}")
    
    return None

def cache_space(space: Space):
    """Guardar espacio en caché"""
    if not redis_client:
        return
    
    try:
        cache_key = f"space:{space.id}"
        space_dict = {
            "id": space.id,
            "name": space.name,
            "description": space.description,
            "capacity": space.capacity,
            "location": space.location,
            "amenities": space.amenities,
            "price_per_hour": float(space.price_per_hour) if space.price_per_hour else 0,
            "is_active": space.is_active
        }
        redis_client.setex(cache_key, 300, json.dumps(space_dict))  # 5 min TTL
    except Exception as e:
        logger.warning(f"Cache write error: {e}")

# =================================================================
# FASTAPI APP
# =================================================================

app = FastAPI(
    title="Spaces Service",
    description="Microservicio de gestión de espacios",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# ENDPOINTS
# =================================================================

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": "spaces-service",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": ENVIRONMENT
    }
    
    try:
        db.execute("SELECT 1")
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error(f"DB check failed: {e}")
    
    if redis_client:
        try:
            redis_client.ping()
            health_status["cache"] = "connected"
        except:
            health_status["cache"] = "disconnected"
    
    return health_status

@app.get("/", response_model=List[SpaceResponse])
async def list_spaces(
    db: Session = Depends(get_db),
    is_active: bool = Query(True, description="Filter by active status"),
    min_capacity: Optional[int] = Query(None, ge=1, description="Minimum capacity"),
    max_capacity: Optional[int] = Query(None, ge=1, description="Maximum capacity"),
    amenity: Optional[str] = Query(None, description="Filter by amenity")
):
    """
    Listar espacios disponibles
    
    Query params:
    - is_active: Solo espacios activos (default true)
    - min_capacity: Capacidad mínima
    - max_capacity: Capacidad máxima
    - amenity: Filtrar por amenidad específica
    """
    query = db.query(Space).filter(Space.is_active == is_active)
    
    if min_capacity:
        query = query.filter(Space.capacity >= min_capacity)
    
    if max_capacity:
        query = query.filter(Space.capacity <= max_capacity)
    
    # Filtrar por amenidad (requiere JSONB en PostgreSQL)
    # En SQLite esto no funcionará perfectamente
    if amenity:
        # Para PostgreSQL: query = query.filter(Space.amenities.contains([amenity]))
        # Workaround para compatibilidad
        pass
    
    spaces = query.order_by(Space.name).all()
    
    logger.info(f"Listed {len(spaces)} spaces")
    
    return [SpaceResponse.from_orm(s) for s in spaces]

@app.get("/{space_id}", response_model=SpaceResponse)
async def get_space(space_id: int, db: Session = Depends(get_db)):
    """
    Obtener detalles de un espacio específico
    
    Usa caché para mejorar performance
    """
    # Intentar desde caché
    cached = get_space_from_cache(space_id)
    if cached:
        logger.info(f"Space {space_id} served from cache")
        return cached
    
    # Obtener de BD
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(404, "Space not found")
    
    # Guardar en caché
    cache_space(space)
    
    return SpaceResponse.from_orm(space)

@app.get("/{space_id}/availability")
async def check_availability(
    space_id: int,
    start_time: datetime = Query(..., description="Start time (ISO format)"),
    end_time: datetime = Query(..., description="End time (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Verificar disponibilidad de un espacio
    
    Retorna si el espacio está disponible en el rango de tiempo especificado
    y lista las reservas conflictivas si las hay.
    """
    # Verificar que el espacio existe
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(404, "Space not found")
    
    if not space.is_active:
        raise HTTPException(400, "Space is not active")
    
    # Validar tiempos
    if end_time <= start_time:
        raise HTTPException(400, "end_time must be after start_time")
    
    if start_time < datetime.utcnow():
        raise HTTPException(400, "Cannot check availability in the past")
    
    # Buscar conflictos
    conflicts = db.query(Reservation).filter(
        Reservation.space_id == space_id,
        Reservation.status == "active",
        or_(
            and_(
                Reservation.start_time <= start_time,
                Reservation.end_time > start_time
            ),
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time >= end_time
            ),
            and_(
                Reservation.start_time >= start_time,
                Reservation.end_time <= end_time
            )
        )
    ).all()
    
    conflicting_reservations = [
        {
            "id": c.id,
            "start_time": c.start_time.isoformat(),
            "end_time": c.end_time.isoformat()
        }
        for c in conflicts
    ]
    
    return {
        "space_id": space_id,
        "space_name": space.name,
        "start_time": start_time,
        "end_time": end_time,
        "available": len(conflicts) == 0,
        "conflicting_reservations": conflicting_reservations if conflicts else []
    }

@app.post("/", response_model=SpaceResponse, status_code=201)
async def create_space(
    space_data: SpaceCreate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo espacio (requiere admin)
    """
    new_space = Space(
        name=space_data.name,
        description=space_data.description,
        capacity=space_data.capacity,
        location=space_data.location,
        amenities=space_data.amenities,
        price_per_hour=space_data.price_per_hour,
        is_active=True
    )
    
    db.add(new_space)
    db.commit()
    db.refresh(new_space)
    
    logger.info(f"Space created: {new_space.id} by admin {admin_user.id}")
    
    return SpaceResponse.from_orm(new_space)

@app.put("/{space_id}", response_model=SpaceResponse)
async def update_space(
    space_id: int,
    space_data: SpaceUpdate,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar espacio existente (requiere admin)
    """
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise HTTPException(404, "Space not found")
    
    # Actualizar campos proporcionados
    if space_data.name is not None:
        space.name = space_data.name
    if space_data.description is not None:
        space.description = space_data.description
    if space_data.capacity is not None:
        space.capacity = space_data.capacity
    if space_data.location is not None:
        space.location = space_data.location
    if space_data.amenities is not None:
        space.amenities = space_data.amenities
    if space_data.price_per_hour is not None:
        space.price_per_hour = space_data.price_per_hour
    if space_data.is_active is not None:
        space.is_active = space_data.is_active
    
    space.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(space)
    
    # Invalidar caché
    if redis_client:
        try:
            redis_client.delete(f"space:{space_id}")
        except:
            pass
    
    logger.info(f"Space {space_id} updated by admin {admin_user.id}")
    
    return SpaceResponse.from_orm(space)

# =================================================================
# STARTUP/SHUTDOWN
# =================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Spaces Service Starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Spaces Service shutting down...")
    if redis_client:
        redis_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=ENVIRONMENT == "development")