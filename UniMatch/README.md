# 🎓 UniMatch 2.0 — Plataforma Global de Match Académico

<div align="center">

![UniMatch Banner](https://img.shields.io/badge/UniMatch-2.0-4F46E5?style=for-the-badge&logo=graduation-cap)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?style=for-the-badge&logo=redis)
![Neo4j](https://img.shields.io/badge/Neo4j-5.x-008CC1?style=for-the-badge&logo=neo4j)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)

**Trabajo Práctico — Bases de Datos II**
*Persistencia Políglota · Arquitectura DAO · Matching Académico Inteligente*

</div>

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Problema y Solución](#-problema-y-solución)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Persistencia Políglota](#-persistencia-políglota)
- [Algoritmo de Matching](#-algoritmo-de-matching)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Capa DAO](#-capa-dao)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Ejemplos de Consultas](#-ejemplos-de-consultas)
- [Diagramas](#-diagramas)
- [Decisiones Técnicas](#-decisiones-técnicas)
- [Equipo](#-equipo)

---

## 🎯 Descripción del Proyecto

**UniMatch 2.0** es una plataforma de matching académico global inspirada en Tinder, diseñada para conectar estudiantes universitarios de todo el mundo según temas de estudio específicos, nivel académico, idioma, horarios y objetivos de aprendizaje.

A diferencia de las plataformas actuales que agrupan por institución, UniMatch conecta por **conocimiento compartido**, generando comunidades de aprendizaje colaborativo trans-institucionales e internacionales.

### Funcionalidades Principales

| Funcionalidad | Descripción | Base de Datos |
|--------------|-------------|---------------|
| Registro y perfil | Gestión completa de usuarios | PostgreSQL |
| Matching académico | Compatibilidad multi-criterio | PostgreSQL + Neo4j |
| Recomendaciones | Colaboración por grafo | Neo4j |
| Chat en tiempo real | Mensajería entre estudiantes | PostgreSQL |
| Sesiones | Autenticación y tokens | Redis |
| Rankings | Temas más populares | Redis |
| Comunidades | Grupos temáticos | Neo4j |

---

## 🔍 Problema y Solución

### Problema

Las plataformas de estudio actuales presentan las siguientes limitaciones críticas:

- **Agrupación institucional**: Solo conectan personas de la misma universidad
- **Falta de matching inteligente**: No evalúan compatibilidad académica real
- **Sin análisis temporal**: No consideran compatibilidad horaria entre zonas
- **Sin recomendaciones**: No sugieren compañeros por afinidad temática
- **Sin grafo de conocimiento**: No modelan relaciones entre temas académicos

### Solución UniMatch 2.0

```
Problema                          Solución UniMatch
─────────────────────────────────────────────────────
Agrupación por institución   →   Matching por tema exacto
Sin compatibilidad real      →   Algoritmo ponderado 5 criterios
Sin análisis horario         →   Compatibilidad de disponibilidad
Sin recomendaciones          →   Grafo Neo4j con Cypher
Datos homogéneos             →   Persistencia políglota
```

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     CAPA DE PRESENTACIÓN                     │
│              API REST (FastAPI / Endpoints simulados)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                      CAPA DE SERVICIOS                       │
│   MatchingService │ RecommendationService │ ChatService       │
└──────┬────────────────────┬──────────────────────┬──────────┘
       │                    │                      │
┌──────▼──────┐   ┌─────────▼──────┐   ┌──────────▼──────────┐
│  DAO Layer  │   │   DAO Layer    │   │     DAO Layer        │
│ PostgreSQL  │   │     Neo4j      │   │      Redis           │
└──────┬──────┘   └─────────┬──────┘   └──────────┬──────────┘
       │                    │                      │
┌──────▼──────┐   ┌─────────▼──────┐   ┌──────────▼──────────┐
│ PostgreSQL  │   │     Neo4j      │   │       Redis          │
│  Base de    │   │  Grafo de      │   │   Cache/Sesiones/    │
│  Datos      │   │  Relaciones    │   │   Rankings           │
│ Relacional  │   │  Académicas    │   │                      │
└─────────────┘   └────────────────┘   └─────────────────────┘
```

Ver diagrama completo en [`diagrams/arquitectura_general.md`](diagrams/arquitectura_general.md)

---

## 🗄️ Persistencia Políglota

UniMatch implementa **persistencia políglota** usando tres motores de bases de datos, cada uno optimizado para el tipo de dato que maneja:

### PostgreSQL — Datos Relacionales y Transaccionales

**¿Por qué?** Los datos estructurados con relaciones formales (usuarios, universidades, matches) requieren consistencia ACID, integridad referencial y consultas complejas con JOINs.

```sql
-- Ejemplo: Match académico con score calculado
SELECT u.nombre, u.apellido, u.nivel_academico,
       m.score_compatibilidad, m.estado
FROM matches m
JOIN usuarios u ON u.id_usuario = m.id_usuario2
WHERE m.id_usuario1 = 15
  AND m.estado = 'aceptado'
ORDER BY m.score_compatibilidad DESC;
```

### Redis — Cache, Sesiones y Rankings en Tiempo Real

**¿Por qué?** Los datos temporales, tokens de sesión y rankings que se consultan miles de veces por segundo necesitan acceso en microsegundos. Redis almacena esto en memoria con TTL automático.

```
session:user:15        → {user_id, email, token}     TTL: 3600s
cache:recs:15          → [user_id, score, ...]        TTL: 300s
ranking:topics:global  → ZSET [(tema, score), ...]    Sin TTL
token:reset:abc123     → {user_id, expires_at}        TTL: 900s
```

### Neo4j — Grafo de Relaciones Académicas

**¿Por qué?** Las recomendaciones colaborativas y relaciones entre temas son inherentemente un problema de grafos. Neo4j permite consultas como "amigos de amigos que estudian temas relacionados" con rendimiento O(log n) vs O(n³) en SQL.

```cypher
// Recomendación: usuarios que estudian temas relacionados al mío
MATCH (yo:Usuario {id: 15})-[:ESTUDIA]->(t:Tema)<-[:RELACIONADO_CON]-(t2:Tema)
      <-[:ESTUDIA]-(otro:Usuario)
WHERE NOT (yo)-[:MATCH]->(otro)
RETURN otro, COUNT(t2) AS temas_comunes
ORDER BY temas_comunes DESC
LIMIT 10
```

---

## 🧮 Algoritmo de Matching

El score de compatibilidad se calcula con una función ponderada de 5 criterios:

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Tema exacto | 40% | ¿Estudian exactamente el mismo tema? |
| Nivel similar | 20% | ¿Están en el mismo nivel académico? |
| Objetivo compatible | 15% | ¿Buscan lo mismo (tutor, par, grupo)? |
| Idioma compartido | 10% | ¿Comparten idioma de preferencia? |
| Compatibilidad horaria | 15% | ¿Tienen horarios que se solapan? |

```python
def calcular_score(usuario1, usuario2):
    score = 0.0
    score += 0.40 * calcular_tema(usuario1, usuario2)
    score += 0.20 * calcular_nivel(usuario1, usuario2)
    score += 0.15 * calcular_objetivo(usuario1, usuario2)
    score += 0.10 * calcular_idioma(usuario1, usuario2)
    score += 0.15 * calcular_horario(usuario1, usuario2)
    return round(score * 100, 2)  # Retorna 0-100
```

Ver implementación completa en [`src/services/MatchingService.py`](src/services/MatchingService.py)

---

## 📁 Estructura del Repositorio

```
UniMatch/
│
├── README.md                          # Este archivo
│
├── docs/
│   ├── problema.md                    # Análisis del problema
│   ├── arquitectura.md                # Decisiones de arquitectura
│   ├── algoritmo_matching.md          # Explicación del algoritmo
│   ├── decisiones_tecnicas.md         # Por qué cada tecnología
│   ├── seguridad.md                   # Consideraciones de seguridad
│   └── dao_explicacion.md             # Patrón DAO explicado
│
├── diagrams/
│   ├── DER_postgresql.md              # DER completo en Mermaid
│   ├── neo4j_graph.md                 # Diagrama grafo Neo4j
│   ├── arquitectura_general.md        # Arquitectura del sistema
│   ├── diagrama_clases.md             # Diagrama de clases DAO
│   └── diagrama_secuencia.md          # Flujo de matching
│
├── sql/
│   ├── schema.sql                     # DDL completo PostgreSQL
│   ├── inserts.sql                    # Datos de ejemplo
│   ├── indexes.sql                    # Índices optimizados
│   ├── triggers.sql                   # Triggers automáticos
│   └── queries.sql                    # Consultas de negocio
│
├── neo4j/
│   ├── graph_schema.cypher            # Constraints y schema
│   ├── inserts.cypher                 # Nodos y relaciones ejemplo
│   └── recommendations.cypher        # Algoritmos de recomendación
│
├── redis/
│   ├── cache_examples.md              # Ejemplos de uso
│   └── redis_structure.md            # Estructura de claves
│
├── src/
│   ├── config/
│   │   ├── postgres.py                # Conexión PostgreSQL
│   │   ├── redis_client.py            # Conexión Redis
│   │   └── neo4j_client.py            # Conexión Neo4j
│   │
│   ├── dao/
│   │   ├── postgres/
│   │   │   ├── UsuarioDAO.py
│   │   │   ├── TemaDAO.py
│   │   │   ├── MatchDAO.py
│   │   │   ├── MensajeDAO.py
│   │   │   └── HorarioDAO.py
│   │   ├── redis/
│   │   │   ├── SessionDAO.py
│   │   │   ├── CacheDAO.py
│   │   │   └── RankingDAO.py
│   │   └── neo4j/
│   │       ├── GraphUserDAO.py
│   │       ├── GraphTopicDAO.py
│   │       └── RecommendationDAO.py
│   │
│   ├── services/
│   │   ├── MatchingService.py
│   │   ├── RecommendationService.py
│   │   └── ChatService.py
│   │
│   └── main.py
│
├── api/
│   └── endpoints.md                   # Documentación de endpoints
│
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
│
└── requirements.txt
```

---

## 🔧 Capa DAO

El patrón **Data Access Object (DAO)** separa la lógica de negocio del acceso a datos. Cada DAO encapsula todas las operaciones sobre una entidad específica en una base de datos concreta.

### DAOs PostgreSQL

| DAO | Responsabilidad | Métodos Principales |
|-----|----------------|---------------------|
| `UsuarioDAO` | CRUD de usuarios | `crear`, `obtener_por_id`, `buscar_por_tema`, `actualizar` |
| `TemaDAO` | Gestión de temas | `crear`, `buscar`, `obtener_populares`, `obtener_alias` |
| `MatchDAO` | Gestión de matches | `crear_match`, `obtener_matches`, `actualizar_estado` |
| `MensajeDAO` | Chat entre usuarios | `enviar`, `obtener_conversacion`, `marcar_leido` |
| `HorarioDAO` | Disponibilidad | `registrar`, `obtener_por_usuario`, `buscar_solapamiento` |

### DAOs Redis

| DAO | Responsabilidad |
|-----|----------------|
| `SessionDAO` | Sesiones activas con TTL |
| `CacheDAO` | Cache de recomendaciones |
| `RankingDAO` | Rankings de temas populares |

### DAOs Neo4j

| DAO | Responsabilidad |
|-----|----------------|
| `GraphUserDAO` | Nodos de usuario en grafo |
| `GraphTopicDAO` | Nodos de tema y relaciones |
| `RecommendationDAO` | Algoritmos de recomendación Cypher |

Ver implementación en [`src/dao/`](src/dao/) y explicación en [`docs/dao_explicacion.md`](docs/dao_explicacion.md)

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Docker Desktop 4.x+
- Docker Compose 2.x+
- Python 3.11+

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/UniMatch.git
cd UniMatch

# 2. Levantar infraestructura con Docker
cd docker
docker-compose up -d

# 3. Esperar que los servicios estén listos (aprox 30s)
docker-compose ps

# 4. Inicializar base de datos PostgreSQL
docker exec -i unimatch_postgres psql -U unimatch -d unimatch_db < ../sql/schema.sql
docker exec -i unimatch_postgres psql -U unimatch -d unimatch_db < ../sql/inserts.sql
docker exec -i unimatch_postgres psql -U unimatch -d unimatch_db < ../sql/indexes.sql
docker exec -i unimatch_postgres psql -U unimatch -d unimatch_db < ../sql/triggers.sql

# 5. Inicializar Neo4j
cat ../neo4j/graph_schema.cypher | docker exec -i unimatch_neo4j cypher-shell -u neo4j -p unimatch2024
cat ../neo4j/inserts.cypher | docker exec -i unimatch_neo4j cypher-shell -u neo4j -p unimatch2024

# 6. Instalar dependencias Python
pip install -r requirements.txt

# 7. Ejecutar la aplicación
python src/main.py
```

### Servicios y Puertos

| Servicio | Puerto | URL |
|----------|--------|-----|
| PostgreSQL | 5432 | `localhost:5432` |
| Redis | 6379 | `localhost:6379` |
| Neo4j Browser | 7474 | `http://localhost:7474` |
| Neo4j Bolt | 7687 | `bolt://localhost:7687` |

### Credenciales por Defecto

```
PostgreSQL: unimatch / unimatch2024 / DB: unimatch_db
Redis: sin contraseña (desarrollo)
Neo4j: neo4j / unimatch2024
```

---

## 💡 Ejemplos de Consultas

### PostgreSQL — Top matches de un usuario

```sql
SELECT
    u.nombre || ' ' || u.apellido AS compañero,
    u.universidad_nombre,
    m.score_compatibilidad,
    m.estado,
    ARRAY_AGG(DISTINCT t.nombre) AS temas_comunes
FROM matches m
JOIN usuarios u ON u.id_usuario = m.id_usuario2
JOIN usuario_temas ut ON ut.id_usuario = u.id_usuario
JOIN temas t ON t.id_tema = ut.id_tema
WHERE m.id_usuario1 = 1
GROUP BY u.id_usuario, m.score_compatibilidad, m.estado
ORDER BY m.score_compatibilidad DESC
LIMIT 5;
```

### Neo4j — Recomendación por camino de grafo

```cypher
MATCH (yo:Usuario {id_usuario: 1})-[:ESTUDIA]->(t:Tema)
      <-[:ESTUDIA]-(candidato:Usuario)
WHERE NOT (yo)-[:MATCH]-(candidato)
  AND yo <> candidato
WITH candidato, COLLECT(t.nombre) AS temas_comunes,
     COUNT(t) AS score
ORDER BY score DESC
LIMIT 10
RETURN candidato.nombre, candidato.nivel, temas_comunes, score
```

### Redis — Cache de recomendaciones

```python
# Guardar recomendaciones en cache por 5 minutos
cache_dao.set_recomendaciones(
    user_id=1,
    recomendaciones=[{"id": 5, "score": 87.5}, {"id": 12, "score": 82.1}],
    ttl=300
)

# Consultar ranking de temas populares
top_temas = ranking_dao.obtener_top_temas(limite=10)
```

---

## 📊 Diagramas

| Diagrama | Archivo |
|----------|---------|
| DER PostgreSQL (Mermaid) | [`diagrams/DER_postgresql.md`](diagrams/DER_postgresql.md) |
| Grafo Neo4j | [`diagrams/neo4j_graph.md`](diagrams/neo4j_graph.md) |
| Arquitectura General | [`diagrams/arquitectura_general.md`](diagrams/arquitectura_general.md) |
| Diagrama de Clases DAO | [`diagrams/diagrama_clases.md`](diagrams/diagrama_clases.md) |
| Diagrama de Secuencia | [`diagrams/diagrama_secuencia.md`](diagrams/diagrama_secuencia.md) |

---

## ⚙️ Decisiones Técnicas

| Decisión | Justificación |
|----------|--------------|
| PostgreSQL para datos base | ACID, integridad referencial, JOINs complejos |
| Redis para sesiones | Acceso O(1), TTL nativo, volumen de lectura alto |
| Neo4j para recomendaciones | Traversal de grafos nativo, consultas de vecinos eficientes |
| Python como backend | Drivers oficiales para las tres DBs, ecosistema de IA |
| Docker Compose | Reproducibilidad del entorno, aislamiento de servicios |
| Patrón DAO | Separación de responsabilidades, testabilidad, intercambiabilidad |

Ver análisis completo en [`docs/decisiones_tecnicas.md`](docs/decisiones_tecnicas.md)

---

## 👥 Equipo

**Materia**: Bases de Datos II
**Carrera**: Ingeniería en Sistemas / Licenciatura en Informática
**Año**: 2024

---

<div align="center">

*UniMatch 2.0 — Conectando mentes, no instituciones* 🌍

</div>
