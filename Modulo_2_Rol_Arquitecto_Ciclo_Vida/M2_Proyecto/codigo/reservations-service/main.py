"""
Reservations Service - Servicio de Gestión de Reservas
=======================================================
Este microservicio maneja:
- Creación de reservas con validación de disponibilidad
- Listado de reservas del usuario
- Consulta de detalles de reserva
- Cancelación de reservas

Endpoints:
- POST / - Crear nueva reserva
- GET / - Listar reservas del usuario
- GET /{id} - Obtener detalles de reserva
- DELETE /{id} - Cancelar reserva
- GET /health - Health check
"""

from datetime import datetime, timedelta
from typing import Optional, List
from decimal import Decimal
import os

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, and_, or_
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
    name = Column(String)
    is_active = Column(Boolean)

class Space(Base):
    __tablename__ = "spaces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_active = Column(Boolean)
    price_per_hour = Column(Numeric(10, 2))

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="active")
    total_price = Column(Numeric(10, 2))
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# =================================================================
# PYDANTIC MODELS
# =================================================================

class ReservationCreate(BaseModel):
    """Modelo para crear reserva"""
    space_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        
        # Validar duración mínima (30 minutos)
        if 'start_time' in values:
            duration = (v - values['start_time']).total_seconds()
            if duration < 1800:  # 30 minutos
                raise ValueError('Minimum reservation duration is 30 minutes')
        
        return v
    
    @validator('start_time')
    def not_in_past(cls, v):
        if v < datetime.utcnow():
            raise ValueError('Cannot create reservation in the past')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "space_id": 1,
                "start_time": "2026-01-20T10:00:00",
                "end_time": "2026-01-20T12:00:00",
                "notes": "Team meeting"
            }
        }

class ReservationResponse(BaseModel):
    """Respuesta con información de reserva"""
    id: int
    user_id: int
    space_id: int
    start_time: datetime
    end_time: datetime
    status: str
    total_price: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ReservationWithDetails(BaseModel):
    """Respuesta con detalles completos incluyendo espacio"""
    id: int
    user_id: int
    space_id: int
    space_name: str
    start_time: datetime
    end_time: datetime
    duration_hours: float
    status: str
    total_price: Optional[float]
    notes: Optional[str]
    created_at: datetime

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
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user

# =================================================================
# HELPER FUNCTIONS
# =================================================================

def check_availability(db: Session, space_id: int, start_time: datetime, end_time: datetime, exclude_id: int = None) -> bool:
    """Verificar si un espacio está disponible en un rango de tiempo"""
    query = db.query(Reservation).filter(
        Reservation.space_id == space_id,
        Reservation.status == "active",
        or_(
            # El inicio de la nueva reserva está dentro de una existente
            and_(
                Reservation.start_time <= start_time,
                Reservation.end_time > start_time
            ),
            # El fin de la nueva reserva está dentro de una existente
            and_(
                Reservation.start_time < end_time,
                Reservation.end_time >= end_time
            ),
            # La nueva reserva engloba completamente una existente
            and_(
                Reservation.start_time >= start_time,
                Reservation.end_time <= end_time
            )
        )
    )
    
    if exclude_id:
        query = query.filter(Reservation.id != exclude_id)
    
    conflict = query.first()
    return conflict is None

# =================================================================
# FASTAPI APP
# =================================================================

app = FastAPI(
    title="Reservations Service",
    description="Microservicio de gestión de reservas",
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
    """Health check"""
    health_status = {
        "status": "healthy",
        "service": "reservations-service",
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

@app.post("/", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    reservation_data: ReservationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear nueva reserva
    
    Validaciones:
    - Espacio debe existir y estar activo
    - No debe haber conflictos de horario
    - Duración mínima 30 minutos
    - No se puede reservar en el pasado
    """
    # Verificar que el espacio existe y está activo
    space = db.query(Space).filter(Space.id == reservation_data.space_id).first()
    if not space or not space.is_active:
        raise HTTPException(404, "Space not found or inactive")
    
    # Verificar disponibilidad
    if not check_availability(db, reservation_data.space_id, 
                             reservation_data.start_time, 
                             reservation_data.end_time):
        raise HTTPException(
            409, 
            "Space is not available for the selected time range"
        )
    
    # Crear reserva
    new_reservation = Reservation(
        user_id=current_user.id,
        space_id=reservation_data.space_id,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time,
        notes=reservation_data.notes,
        status="active"
    )
    
    # El trigger de BD calculará total_price automáticamente
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    logger.info(f"Reservation created: ID {new_reservation.id} by user {current_user.id}")
    
    return ReservationResponse.from_orm(new_reservation)

@app.get("/", response_model=List[ReservationResponse])
async def list_reservations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, regex="^(active|cancelled|completed)$"),
    limit: int = Query(50, le=100)
):
    """
    Listar reservas del usuario actual
    
    Query params:
    - status: Filtrar por estado (active, cancelled, completed)
    - limit: Máximo de resultados (default 50, max 100)
    """
    query = db.query(Reservation).filter(Reservation.user_id == current_user.id)
    
    if status:
        query = query.filter(Reservation.status == status)
    
    reservations = query.order_by(Reservation.start_time.desc()).limit(limit).all()
    
    return [ReservationResponse.from_orm(r) for r in reservations]

@app.get("/{reservation_id}", response_model=ReservationWithDetails)
async def get_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de una reserva específica
    
    Solo el propietario puede ver sus reservas
    """
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()
    
    if not reservation:
        raise HTTPException(404, "Reservation not found")
    
    # Obtener información del espacio
    space = db.query(Space).filter(Space.id == reservation.space_id).first()
    
    # Calcular duración en horas
    duration = (reservation.end_time - reservation.start_time).total_seconds() / 3600
    
    return {
        "id": reservation.id,
        "user_id": reservation.user_id,
        "space_id": reservation.space_id,
        "space_name": space.name if space else "Unknown",
        "start_time": reservation.start_time,
        "end_time": reservation.end_time,
        "duration_hours": round(duration, 2),
        "status": reservation.status,
        "total_price": float(reservation.total_price) if reservation.total_price else None,
        "notes": reservation.notes,
        "created_at": reservation.created_at
    }

@app.delete("/{reservation_id}", status_code=204)
async def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancelar una reserva
    
    Restricciones:
    - Solo el propietario puede cancelar
    - No se pueden cancelar reservas ya canceladas
    - No se pueden cancelar reservas pasadas
    """
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()
    
    if not reservation:
        raise HTTPException(404, "Reservation not found")
    
    if reservation.status == "cancelled":
        raise HTTPException(400, "Reservation is already cancelled")
    
    if reservation.status == "completed":
        raise HTTPException(400, "Cannot cancel completed reservations")
    
    # No permitir cancelar si ya pasó
    if reservation.end_time < datetime.utcnow():
        raise HTTPException(400, "Cannot cancel past reservations")
    
    # Cancelar
    reservation.status = "cancelled"
    db.commit()
    
    logger.info(f"Reservation {reservation_id} cancelled by user {current_user.id}")
    
    return None

# =================================================================
# ENDPOINTS ADICIONALES
# =================================================================

@app.get("/upcoming/count")
async def get_upcoming_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Contar reservas futuras del usuario"""
    from sqlalchemy import func
    
    count = db.query(func.count(Reservation.id)).filter(
        Reservation.user_id == current_user.id,
        Reservation.status == "active",
        Reservation.start_time > datetime.utcnow()
    ).scalar()
    
    return {"upcoming_reservations": count}

# =================================================================
# STARTUP/SHUTDOWN
# =================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Reservations Service Starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Reservations Service shutting down...")
    if redis_client:
        redis_client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=ENVIRONMENT == "development")