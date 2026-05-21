```mermaid
erDiagram
    USUARIO ||--o{ USUARIO_TEMA : estudia
    TEMA ||--o{ USUARIO_TEMA : contiene
    USUARIO ||--o{ MATCH : genera
```