class RecommendationDAO:

    def buscar_matches_por_tema(self, tema):
        query = '''
        MATCH (u:Usuario)-[:ESTUDIA]->(t:Tema {nombre:$tema})
        RETURN u
        '''
        return query