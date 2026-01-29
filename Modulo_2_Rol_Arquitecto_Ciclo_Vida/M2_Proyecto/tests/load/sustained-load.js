/**
 * K6 Load Test - Carga Sostenida
 * ================================
 * Este script prueba el sistema bajo carga constante
 * 
 * Ejecutar:
 *   k6 run sustained-load.js
 * 
 * Con output HTML:
 *   k6 run --out json=results.json sustained-load.js
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// =================================================================
// CONFIGURACIÓN
// =================================================================

const BASE_URL = __ENV.BASE_URL || 'http://localhost';

// Métricas personalizadas
const errorRate = new Rate('errors');
const loginDuration = new Trend('login_duration');
const reservationDuration = new Trend('reservation_duration');
const successfulReservations = new Counter('successful_reservations');

// Opciones del test
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up a 50 usuarios
    { duration: '5m', target: 100 },  // Aumentar a 100 usuarios
    { duration: '5m', target: 100 },  // Mantener 100 usuarios
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<200'],  // 95% de requests bajo 200ms
    'http_req_failed': ['rate<0.01'],    // Menos de 1% de errores
    'errors': ['rate<0.01'],             // Tasa de error personalizada
  },
};

// =================================================================
// HELPERS
// =================================================================

/**
 * Generar email aleatorio para testing
 */
function randomEmail() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(7);
  return `user_${timestamp}_${random}@loadtest.com`;
}

/**
 * Generar nombre aleatorio
 */
function randomName() {
  const names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie', 'Diana'];
  const surnames = ['Doe', 'Smith', 'Johnson', 'Williams', 'Brown', 'Davis'];
  return `${names[Math.floor(Math.random() * names.length)]} ${surnames[Math.floor(Math.random() * surnames.length)]}`;
}

/**
 * Obtener fecha futura aleatoria
 */
function getRandomFutureDate() {
  const now = new Date();
  const daysAhead = Math.floor(Math.random() * 30) + 1; // 1-30 días
  const futureDate = new Date(now.getTime() + daysAhead * 24 * 60 * 60 * 1000);
  
  // Set hora entre 9:00 y 17:00
  const hour = Math.floor(Math.random() * 8) + 9;
  futureDate.setHours(hour, 0, 0, 0);
  
  return futureDate;
}

/**
 * Registrar y obtener token
 */
function registerAndLogin() {
  const email = randomEmail();
  const password = 'LoadTest123!';
  const name = randomName();
  
  // Registrar
  const registerRes = http.post(
    `${BASE_URL}/api/auth/register`,
    JSON.stringify({
      email: email,
      password: password,
      name: name
    }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'Register' }
    }
  );
  
  if (registerRes.status === 201) {
    const body = JSON.parse(registerRes.body);
    return body.access_token;
  }
  
  // Si falla registro, intentar login (usuario ya existe)
  const loginRes = http.post(
    `${BASE_URL}/api/auth/login`,
    JSON.stringify({
      email: email,
      password: password
    }),
    {
      headers: { 'Content-Type': 'application/json' },
      tags: { name: 'Login' }
    }
  );
  
  if (loginRes.status === 200) {
    const body = JSON.parse(loginRes.body);
    loginDuration.add(loginRes.timings.duration);
    return body.access_token;
  }
  
  errorRate.add(1);
  return null;
}

// =================================================================
// ESCENARIOS DE PRUEBA
// =================================================================

export default function() {
  // Obtener token
  const token = registerAndLogin();
  
  if (!token) {
    errorRate.add(1);
    sleep(1);
    return;
  }
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
  
  // =======================
  // Grupo 1: Listar Espacios
  // =======================
  group('List Spaces', () => {
    const res = http.get(`${BASE_URL}/api/spaces`, {
      headers: headers,
      tags: { name: 'ListSpaces' }
    });
    
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'response time < 200ms': (r) => r.timings.duration < 200,
      'has spaces': (r) => {
        try {
          const body = JSON.parse(r.body);
          return Array.isArray(body) && body.length > 0;
        } catch {
          return false;
        }
      }
    });
    
    if (!success) errorRate.add(1);
  });
  
  sleep(0.5);
  
  // =======================
  // Grupo 2: Verificar Disponibilidad
  // =======================
  group('Check Availability', () => {
    const spaceId = 1; // Asumimos que el espacio 1 existe
    const startDate = getRandomFutureDate();
    const endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000); // +2 horas
    
    const res = http.get(
      `${BASE_URL}/api/spaces/${spaceId}/availability?start_time=${startDate.toISOString()}&end_time=${endDate.toISOString()}`,
      {
        headers: headers,
        tags: { name: 'CheckAvailability' }
      }
    );
    
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'has availability info': (r) => {
        try {
          const body = JSON.parse(r.body);
          return 'available' in body;
        } catch {
          return false;
        }
      }
    });
    
    if (!success) errorRate.add(1);
  });
  
  sleep(0.5);
  
  // =======================
  // Grupo 3: Crear Reserva
  // =======================
  group('Create Reservation', () => {
    const spaceId = Math.floor(Math.random() * 3) + 1; // Espacios 1-3
    const startDate = getRandomFutureDate();
    const endDate = new Date(startDate.getTime() + 2 * 60 * 60 * 1000);
    
    const res = http.post(
      `${BASE_URL}/api/reservations`,
      JSON.stringify({
        space_id: spaceId,
        start_time: startDate.toISOString(),
        end_time: endDate.toISOString(),
        notes: `Load test reservation at ${new Date().toISOString()}`
      }),
      {
        headers: headers,
        tags: { name: 'CreateReservation' }
      }
    );
    
    reservationDuration.add(res.timings.duration);
    
    const success = check(res, {
      'status is 201 or 409': (r) => r.status === 201 || r.status === 409, // 409 = conflict, aceptable
      'response time < 500ms': (r) => r.timings.duration < 500,
    });
    
    if (res.status === 201) {
      successfulReservations.add(1);
    }
    
    if (!success && res.status !== 409) {
      errorRate.add(1);
    }
  });
  
  sleep(0.5);
  
  // =======================
  // Grupo 4: Listar Mis Reservas
  // =======================
  group('List My Reservations', () => {
    const res = http.get(`${BASE_URL}/api/reservations`, {
      headers: headers,
      tags: { name: 'ListReservations' }
    });
    
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'is array': (r) => {
        try {
          return Array.isArray(JSON.parse(r.body));
        } catch {
          return false;
        }
      }
    });
    
    if (!success) errorRate.add(1);
  });
  
  sleep(1);
  
  // =======================
  // Grupo 5: Ver Perfil
  // =======================
  group('Get Profile', () => {
    const res = http.get(`${BASE_URL}/api/users/me`, {
      headers: headers,
      tags: { name: 'GetProfile' }
    });
    
    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'has user info': (r) => {
        try {
          const body = JSON.parse(r.body);
          return 'email' in body && 'name' in body;
        } catch {
          return false;
        }
      }
    });
    
    if (!success) errorRate.add(1);
  });
  
  // Pausa entre iteraciones
  sleep(Math.random() * 2 + 1); // 1-3 segundos
}

// =================================================================
// SETUP Y TEARDOWN
// =================================================================

export function setup() {
  console.log('='.repeat(60));
  console.log('Starting Load Test - Sustained Load');
  console.log(`Target: ${BASE_URL}`);
  console.log(`Duration: ~14 minutes`);
  console.log(`Max VUs: 100`);
  console.log('='.repeat(60));
}

export function teardown(data) {
  console.log('='.repeat(60));
  console.log('Load Test Completed');
  console.log('Check results above for detailed metrics');
  console.log('='.repeat(60));
}

// =================================================================
// RESUMEN
// =================================================================

/**
 * Este test simula usuarios reales que:
 * 1. Se registran o hacen login
 * 2. Listan espacios disponibles
 * 3. Verifican disponibilidad
 * 4. Crean reservas
 * 5. Listan sus reservas
 * 6. Consultan su perfil
 * 
 * Métricas clave:
 * - http_req_duration p95 < 200ms (SLA)
 * - Error rate < 1%
 * - Throughput total del sistema
 * 
 * Resultados esperados:
 * ✓ 95% de requests bajo 200ms
 * ✓ Menos de 1% de errores
 * ✓ Sistema estable durante toda la prueba
 */