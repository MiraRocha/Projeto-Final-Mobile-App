from datetime import datetime 
from operator import itemgetter
from services.movimentos_service import MovimentosService

class EstatisticaCrontroller:
    def __init__(self):
        self.movimentos_service= MovimentosService()

    def despesas_por_mes(self, user_id, mes, ano):
        # retorna:
                # lista de tuplos: [(categoria, total_categoria),...]
                # total do mês
                # lista de movimentos do mês para o histórico
        movimentos = self.movimentos_service.obter_movimentos(user_id)

        despesas_mes = []
        categorias = {}
        total_mes = 0

        for movimento in movimentos:
            
            # apenas despesas e não movimentos de saldo
            if movimento.get("tipo") != "despesa":
                continue

            # timestamp -> datetime
            ts= movimento.get("timestamp")
            data= datetime.fromtimestamp(ts)

            if data.month == mes and data.year == ano:
                valor= abs(movimento.get("valor", 0)) # tornar positivo
                categoria= movimento.get("categoria", "Outros")

                despesas_mes.append(movimento)
                total_mes += valor

                if categoria in categorias:
                    categorias[categoria] += valor
                else:
                    categorias[categoria]= valor

        # ordenar categorias pelo total gasto (maior primeiro)
        categorias_ordenadas= sorted(categorias.items(), key= itemgetter(1),reverse=True)
        # Ordena o dicionário de categorias pelo valor gasto (item[1]) em ordem decrescente.
        # categories.items() -> devolve pares (categoria, valor)
        # itemgetter(1) -> diz ao sorted para ordenar pelo segundo elemento, ou seja, o valor.

        return categorias_ordenadas, total_mes, despesas_mes