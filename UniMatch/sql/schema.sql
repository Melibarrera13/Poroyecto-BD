CREATE TABLE universidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    universidad_id INT REFERENCES universidad(id)
);

CREATE TABLE tema (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE usuario_tema (
    usuario_id INT REFERENCES usuario(id),
    tema_id INT REFERENCES tema(id),
    PRIMARY KEY(usuario_id, tema_id)
);