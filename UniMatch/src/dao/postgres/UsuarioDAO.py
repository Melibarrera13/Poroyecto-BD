from src.config.postgres import get_connection

class UsuarioDAO:

    def obtener_usuario_por_id(self, id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM usuario WHERE id = %s",
            (id_usuario,)
        )
        return cursor.fetchone()

    def crear_usuario(self, nombre, email, universidad_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO usuario(nombre,email,universidad_id)
            VALUES (%s,%s,%s)
            ''',
            (nombre,email,universidad_id)
        )
        conn.commit()