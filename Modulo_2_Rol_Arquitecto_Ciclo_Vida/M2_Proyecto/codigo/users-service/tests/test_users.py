"""
Tests para Users Service
========================
Ejecutar con: pytest tests/test_users.py -v
Cobertura con: pytest tests/test_users.py --cov --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db, User
import os

# =================================================================
# CONFIGURACIÓN DE TESTS
# =================================================================

# Base de datos de prueba en memoria
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override de la dependency de DB para tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# =================================================================
# FIXTURES
# =================================================================

@pytest.fixture
def test_user():
    """Crear usuario de prueba y retornar token"""
    from passlib.context import CryptContext
    from jose import jwt
    from datetime import datetime, timedelta
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    db = TestingSessionLocal()
    
    # Crear usuario
    user = User(
        email="test@example.com",
        password_hash=pwd_context.hash("Test123!"),
        name="Test User",
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Generar token
    JWT_SECRET = os.getenv("JWT_SECRET", "test-secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    
    token_data = {
        "sub": user.id,
        "email": user.email,
        "role": "user",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    yield {"user": user, "token": token, "db": db}
    
    # Cleanup
    db.query(User).delete()
    db.commit()
    db.close()

@pytest.fixture(autouse=True)
def cleanup_database():
    """Limpiar base de datos después de cada test"""
    yield
    db = TestingSessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()

# =================================================================
# TESTS DE HEALTH CHECK
# =================================================================

def test_health_check():
    """Test de endpoint /health"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "users-service"
    assert "timestamp" in data

# =================================================================
# TESTS DE GET PROFILE
# =================================================================

def test_get_profile_success(test_user):
    """Test obtener perfil con token válido"""
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["is_admin"] == False
    assert "id" in data
    assert "created_at" in data

def test_get_profile_without_token():
    """Test obtener perfil sin token - debe fallar"""
    response = client.get("/me")
    assert response.status_code == 403  # Forbidden sin header

def test_get_profile_invalid_token():
    """Test obtener perfil con token inválido"""
    response = client.get(
        "/me",
        headers={"Authorization": "Bearer invalid-token-xyz"}
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_get_profile_inactive_user(test_user):
    """Test obtener perfil de usuario inactivo"""
    # Desactivar usuario
    db = test_user["db"]
    user = test_user["user"]
    user.is_active = False
    db.commit()
    
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    
    assert response.status_code == 401
    assert "User not found or inactive" in response.json()["detail"]

# =================================================================
# TESTS DE UPDATE PROFILE
# =================================================================

def test_update_profile_name_only(test_user):
    """Test actualizar solo el nombre"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"name": "Updated Name"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "test@example.com"  # Email no cambió

def test_update_profile_email_only(test_user):
    """Test actualizar solo el email"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"email": "newemail@example.com"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["name"] == "Test User"  # Nombre no cambió

def test_update_profile_both_fields(test_user):
    """Test actualizar nombre y email"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={
            "name": "New Name",
            "email": "new@example.com"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "new@example.com"

def test_update_profile_no_fields(test_user):
    """Test actualizar sin proporcionar campos - debe fallar"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={}
    )
    
    assert response.status_code == 400
    assert "At least one field" in response.json()["detail"]

def test_update_profile_duplicate_email(test_user):
    """Test actualizar a email ya existente - debe fallar"""
    db = test_user["db"]
    
    # Crear otro usuario
    other_user = User(
        email="other@example.com",
        password_hash="hash",
        name="Other User",
        is_active=True
    )
    db.add(other_user)
    db.commit()
    
    # Intentar actualizar al email del otro usuario
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"email": "other@example.com"}
    )
    
    assert response.status_code == 400
    assert "already in use" in response.json()["detail"]

def test_update_profile_invalid_email(test_user):
    """Test actualizar con email inválido"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"email": "invalid-email"}
    )
    
    assert response.status_code == 422  # Validation error

def test_update_profile_empty_name(test_user):
    """Test actualizar con nombre vacío - debe fallar"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"name": "   "}
    )
    
    assert response.status_code == 422  # Validation error

def test_update_profile_name_too_short(test_user):
    """Test actualizar con nombre muy corto"""
    response = client.put(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={"name": "A"}
    )
    
    assert response.status_code == 422

# =================================================================
# TESTS DE DELETE ACCOUNT
# =================================================================

def test_delete_account_success(test_user):
    """Test eliminar cuenta exitosamente"""
    response = client.delete(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    
    assert response.status_code == 204
    
    # Verificar que el usuario está inactivo
    db = test_user["db"]
    user = db.query(User).filter(User.id == test_user["user"].id).first()
    assert user.is_active == False

def test_delete_account_without_token():
    """Test eliminar cuenta sin token"""
    response = client.delete("/me")
    assert response.status_code == 403

def test_delete_account_twice(test_user):
    """Test eliminar cuenta dos veces"""
    # Primera eliminación
    response1 = client.delete(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    assert response1.status_code == 204
    
    # Segunda eliminación - debe fallar porque usuario está inactivo
    response2 = client.delete(
        "/me",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    assert response2.status_code == 401  # Usuario inactivo

# =================================================================
# TESTS DE STATS
# =================================================================

def test_get_stats_no_reservations(test_user):
    """Test obtener estadísticas sin reservas"""
    response = client.get(
        "/stats",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == test_user["user"].id
    assert data["total_reservations"] == 0
    assert data["active_reservations"] == 0
    assert "member_since" in data

# =================================================================
# TESTS DE AUTORIZACIÓN
# =================================================================

def test_expired_token():
    """Test con token expirado"""
    from jose import jwt
    from datetime import datetime, timedelta
    
    JWT_SECRET = os.getenv("JWT_SECRET", "test-secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    
    # Token expirado hace 1 hora
    token_data = {
        "sub": 1,
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    expired_token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401

# =================================================================
# RESUMEN DE COBERTURA
# =================================================================

"""
Tests implementados: 18
Cobertura esperada: ~92%

Categorías cubiertas:
✓ Health check
✓ Get profile (éxito, sin token, token inválido, usuario inactivo)
✓ Update profile (nombre, email, ambos, sin campos, duplicado, inválido)
✓ Delete account (éxito, sin token, doble delete)
✓ Stats
✓ Autorización (token expirado)

Para ejecutar:
    pytest tests/test_users.py -v
    pytest tests/test_users.py --cov=main --cov-report=html
"""