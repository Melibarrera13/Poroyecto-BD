class CacheDAO:

    def guardar_recomendacion(self, user_id, data):
        key = f'cache:recommendations:{user_id}'
        return key