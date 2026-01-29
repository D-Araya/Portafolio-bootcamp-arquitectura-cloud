"""
Auth Service - Servicio de Autenticación
=========================================
Este microservicio maneja:
- Registro de usuarios
- Autenticación (login)
- Emisión y validación de tokens JWT
- Refresh de tokens

Endpoints:
- POST /register - Registrar nuevo usuario
- POST /login - Autenticar y obtener token
- POST /refresh - Renovar token
- POST /validate - Validar token (uso interno)
- GET /health - Health check
"""

from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
import redis
import logging

# =================================================================
# CONFIGURACIÓN
# =================================================================

# Logging
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
JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", "1440"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# =================================================================
# DATABASE SETUP
# =================================================================

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Usuario (ORM)
class User(Base):
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    """Hash una contraseña con bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña contra hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
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
# PYDANTIC MODELS (Request/Response)
# =================================================================

class UserRegister(BaseModel):
    """Modelo para registro de usuario"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=2, max_length=255)
    
    @validator('password')
    def password_strength(cls, v):
        """Validar fortaleza de contraseña"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "name": "John Doe"
            }
        }

class UserLogin(BaseModel):
    """Modelo para login"""
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }

class Token(BaseModel):
    """Modelo de respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = JWT_EXPIRATION_MINUTES * 60

class UserResponse(BaseModel):
    """Modelo de usuario en respuesta"""
    id: int
    email: str
    name: str
    is_admin: bool = False
    
    class Config:
        orm_mode = True

class AuthResponse(BaseModel):
    """Respuesta completa de autenticación"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int = JWT_EXPIRATION_MINUTES * 60

# =================================================================
# DEPENDENCIES
# =================================================================

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Dependency para obtener usuario actual desde token"""
    payload = decode_access_token(token)
    user_id: int = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    return user

# =================================================================
# FASTAPI APP
# =================================================================

app = FastAPI(
    title="Auth Service",
    description="Microservicio de autenticación para el sistema de reservas",
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
    Verifica conectividad a base de datos y redis
    """
    health_status = {
        "status": "healthy",
        "service": "auth-service",
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

@app.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registrar nuevo usuario
    
    - **email**: Email único del usuario
    - **password**: Contraseña (min 8 caracteres, 1 mayúscula, 1 número, 1 especial)
    - **name**: Nombre completo del usuario
    
    Retorna: Usuario creado y token de acceso
    """
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Crear nuevo usuario
    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
        is_active=True,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.email} (ID: {new_user.id})")
    
    # Crear token de acceso
    access_token = create_access_token(
        data={"sub": new_user.id, "email": new_user.email, "role": "user"}
    )
    
    return AuthResponse(
        user=UserResponse.from_orm(new_user),
        access_token=access_token
    )

@app.post("/login", response_model=AuthResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Autenticar usuario y obtener token
    
    - **email**: Email del usuario
    - **password**: Contraseña
    
    Retorna: Usuario y token de acceso
    """
    # Buscar usuario
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        logger.warning(f"Failed login attempt for: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Crear token
    access_token = create_access_token(
        data={
            "sub": user.id,
            "email": user.email,
            "role": "admin" if user.is_admin else "user"
        }
    )
    
    logger.info(f"Successful login: {user.email}")
    
    return AuthResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token
    )

@app.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Renovar token de acceso
    
    Requiere: Token válido en el header Authorization
    Retorna: Nuevo token con tiempo de expiración extendido
    """
    access_token = create_access_token(
        data={
            "sub": current_user.id,
            "email": current_user.email,
            "role": "admin" if current_user.is_admin else "user"
        }
    )
    
    logger.info(f"Token refreshed for user: {current_user.email}")
    
    return Token(access_token=access_token)

@app.post("/validate")
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Validar token y obtener información de usuario
    
    Este endpoint es usado internamente por otros servicios
    para validar tokens JWT
    
    Requiere: Token válido en el header Authorization
    Retorna: Información del usuario
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    }

@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtener información del usuario actual
    
    Requiere: Token válido en el header Authorization
    Retorna: Información del usuario autenticado
    """
    return UserResponse.from_orm(current_user)

# =================================================================
# STARTUP/SHUTDOWN EVENTS
# =================================================================

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("=" * 60)
    logger.info("Auth Service Starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'configured'}")
    logger.info(f"Redis: {'Connected' if redis_client else 'Not available'}")
    logger.info("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    logger.info("Auth Service shutting down...")
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