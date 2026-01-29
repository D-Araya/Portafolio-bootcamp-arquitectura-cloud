"""
Users Service - Servicio de Gestión de Usuarios
================================================
Este microservicio maneja:
- Consulta de perfil de usuario
- Actualización de información personal
- Eliminación de cuenta

Endpoints:
- GET /me - Obtener perfil del usuario actual
- PUT /me - Actualizar perfil
- DELETE /me - Eliminar cuenta (soft delete)
- GET /health - Health check
"""

from datetime import datetime
from typing import Optional
import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
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

# Variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/reservations")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
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
    """Modelo ORM de Usuario"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    """Decodificar y validar JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# =================================================================
# PYDANTIC MODELS
# =================================================================

class UserResponse(BaseModel):
    """Respuesta con información de usuario"""
    id: int
    email: str
    name: str
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "name": "John Doe",
                "is_admin": False,
                "created_at": "2026-01-19T10:00:00",
                "updated_at": "2026-01-19T10:00:00"
            }
        }

class UserUpdate(BaseModel):
    """Modelo para actualizar usuario"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    
    @validator('name')
    def name_not_empty(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Updated Doe",
                "email": "newemail@example.com"
            }
        }

# =================================================================
# DEPENDENCIES
# =================================================================

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde token JWT"""
    token = credentials.credentials
    payload = decode_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user

# =================================================================
# FASTAPI APP
# =================================================================

app = FastAPI(
    title="Users Service",
    description="Microservicio de gestión de usuarios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
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
    """
    Health check endpoint
    Verifica estado del servicio y conectividad
    """
    health_status = {
        "status": "healthy",
        "service": "users-service",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": ENVIRONMENT
    }
    
    # Verificar DB
    try:
        db.execute("SELECT 1")
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error(f"Database health check failed: {e}")
    
    # Verificar Redis
    if redis_client:
        try:
            redis_client.ping()
            health_status["cache"] = "connected"
        except:
            health_status["cache"] = "disconnected"
    
    return health_status

@app.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Obtener perfil del usuario actual
    
    Requiere: Token JWT válido en header Authorization
    
    Retorna: Información completa del usuario autenticado
    """
    logger.info(f"Profile accessed by user: {current_user.email}")
    return UserResponse.from_orm(current_user)

@app.put("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual
    
    - **name**: Nuevo nombre (opcional)
    - **email**: Nuevo email (opcional, debe ser único)
    
    Requiere: Token JWT válido
    Retorna: Usuario actualizado
    """
    # Validar que al menos un campo se esté actualizando
    if update_data.name is None and update_data.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )
    
    # Si se actualiza el email, verificar que no exista
    if update_data.email and update_data.email != current_user.email:
        existing_user = db.query(User).filter(
            User.email == update_data.email,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use by another user"
            )
        
        current_user.email = update_data.email
        logger.info(f"Email updated for user ID {current_user.id}: {update_data.email}")
    
    # Actualizar nombre si se proporciona
    if update_data.name:
        current_user.name = update_data.name.strip()
        logger.info(f"Name updated for user ID {current_user.id}: {update_data.name}")
    
    # Guardar cambios
    db.commit()
    db.refresh(current_user)
    
    # Invalidar caché si existe
    if redis_client:
        try:
            cache_key = f"user:profile:{current_user.id}"
            redis_client.delete(cache_key)
        except Exception as e:
            logger.warning(f"Failed to invalidate cache: {e}")
    
    return UserResponse.from_orm(current_user)

@app.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar cuenta del usuario (soft delete)
    
    La cuenta se marca como inactiva pero no se elimina de la BD.
    Esto preserva integridad referencial con reservas existentes.
    
    Requiere: Token JWT válido
    Retorna: 204 No Content
    """
    # Soft delete - marcar como inactivo
    current_user.is_active = False
    db.commit()
    
    logger.info(f"User account deactivated: {current_user.email} (ID: {current_user.id})")
    
    # Invalidar caché
    if redis_client:
        try:
            cache_key = f"user:profile:{current_user.id}"
            redis_client.delete(cache_key)
        except Exception as e:
            logger.warning(f"Failed to invalidate cache: {e}")
    
    return None

@app.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas del usuario
    
    Retorna información sobre las reservas del usuario
    """
    from sqlalchemy import func, and_
    
    # Importar modelo de Reservation (asumiendo que existe en la BD)
    # En producción, esto vendría de un módulo compartido
    class Reservation(Base):
        __tablename__ = "reservations"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer)
        status = Column(String)
        created_at = Column(DateTime)
    
    # Estadísticas básicas
    total_reservations = db.query(func.count(Reservation.id)).filter(
        Reservation.user_id == current_user.id
    ).scalar() or 0
    
    active_reservations = db.query(func.count(Reservation.id)).filter(
        and_(
            Reservation.user_id == current_user.id,
            Reservation.status == 'active'
        )
    ).scalar() or 0
    
    cancelled_reservations = db.query(func.count(Reservation.id)).filter(
        and_(
            Reservation.user_id == current_user.id,
            Reservation.status == 'cancelled'
        )
    ).scalar() or 0
    
    return {
        "user_id": current_user.id,
        "member_since": current_user.created_at.isoformat(),
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "cancelled_reservations": cancelled_reservations,
        "completed_reservations": total_reservations - active_reservations - cancelled_reservations
    }

# =================================================================
# STARTUP/SHUTDOWN EVENTS
# =================================================================

@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Users Service Starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")
    logger.info(f"Redis: {'Connected' if redis_client else 'Not available'}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Users Service shutting down...")
    if redis_client:
        redis_client.close()

# =================================================================
# MAIN
# =================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=ENVIRONMENT == "development",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )