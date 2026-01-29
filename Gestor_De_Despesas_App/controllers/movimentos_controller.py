import time
from datetime import datetime
from operator import itemgetter
from services.movimentos_service import MovimentosService

class MovimentosController:
    def __init__(self):
        self.service= MovimentosService()

    #GUARDAR MOVIMENTO DESPESA
    def registar_despesa(self, user_id, categoria, montante):
        try:                                               # caso o utilizador escreva
            montante_str = str(montante).strip()           # remove espaços à volta
            montante_str = montante_str.replace("€", "")   # remove o símbolo €
            montante_str = montante_str.replace(" ", "")   # remove espaços dentro (ex: "15 00")
            montante_str = montante_str.replace(",", ".")  # troca vírgula por ponto

            if montante_str == "":
                return False, "Insira um montante."

            # permite números decimais: remove 1 ponto e verifica se o resto são só dígitos.
            # se não for numérico (ex: letras, símbolos, dois pontos), o montante é inválido.
            if not montante_str.replace(".", "", 1).isdigit():
                return False, "Montante inválido."

            # converter para float
            montante = float(montante_str)

            # validação para não deixar o utilizador escrever  números negativos
            if montante <= 0:
                return False, "O montante deve ser maior que zero."

            movimento = {
                "tipo": "despesa",
                "categoria": categoria,
                "valor": -abs(montante), # garante que é sempre negativo
                # abs() -> retorna o valor absoluto de um número, 
                # independentemente do seu sinal
            }

            movimento_id = self.service.guardar_movimento(user_id, movimento)

            if movimento_id:
                return True, movimento_id

            return False, "Erro ao guardar despesa."

        except Exception as e:
            print(f"ERRO registar_despesa {e}")
            return False, "Erro inesperado."

    # GUARDAR MOVIMENTO DE ATUALIZAÇÃO DO SALDO
    def registar_saldo(self, user_id, novo_saldo, saldo_anterior):
        try: 
            novo_saldo_str = str(novo_saldo).strip()
            novo_saldo_str = novo_saldo_str.replace("€", "")
            novo_saldo_str = novo_saldo_str.replace(" ", "")
            novo_saldo_str = novo_saldo_str.replace(",", ".")

            saldo_anterior_str = str(saldo_anterior).strip()
            saldo_anterior_str = saldo_anterior_str.replace("€", "")
            saldo_anterior_str = saldo_anterior_str.replace(" ", "")
            saldo_anterior_str = saldo_anterior_str.replace(",", ".")

            if novo_saldo_str == "" or not novo_saldo_str.replace(".", "", 1).isdigit():
                return False, "Valor de saldo inválido."
            # verifica se o campo está vazio ou se o valor inserido não é numérico.
            # para permitir números decimais, removemos apenas um ponto, ex: "10.5" -> "105".
            # depois usamos .isdigit() para garantir que o resto da string contém só dígitos.
            # se não for um número válido, devolvemos erro.
            
            if saldo_anterior_str == "" or not saldo_anterior_str.replace(".", "", 1).isdigit():
                return False, "Erro interno: saldo inválido."
            
            novo_saldo = float(novo_saldo_str)
            saldo_anterior = float(saldo_anterior_str)

            diferenca = novo_saldo - saldo_anterior

            movimento = {
            "tipo": "saldo",
            "categoria": "Atualização de saldo",
            "valor": diferenca,
            }
            
            movimento_id = self.service.guardar_movimento(user_id, movimento)

            if movimento_id:
                return True, movimento_id

            return False, "Erro ao guardar movimento de saldo."
        except Exception as e:
            print(f"ERRO registar_saldo: {e}")
            return False, "Erro inesperado."
        

        
    # BUSCAR HISTÓRICO COMPLETO DE SALDO + DESPESAS
    def obter_movimentos(self, user_id):
        try:
            movimentos= self.service.obter_movimentos(user_id)

            # ordenar do mais recente para o mais antigo
            movimentos.sort(key=itemgetter("timestamp"), reverse=True)

            # formatar valores para UI
            for movimento in movimentos:
                # garantir número válido
                valor = movimento.get("valor", 0)
                try:
                    valor= float(valor)
                except:
                    valor= 0.0

                movimento["valor"] = valor

                # formatar valor
                if valor >= 0:
                    movimento["valor_formatado"] = f"+{valor:.2f}€"
                else:
                    movimento["valor_formatado"] = f"{valor:.2f}€" 

                # flags de tipo
                tipo= movimento.get("tipo", "")

                movimento["mov_tipo_saldo"] = tipo == "saldo"
                # mov_tipo_saldo -> True se o movimento for atualização de saldo
                movimento["mov_tipo_despesa"] = tipo == "despesa"
                # mov_tipo_despesa -> True se for despesa

                # criar data_formatada independentemente do tipo
                ts = movimento.get("timestamp")
                if ts:
                    movimento["data_formatada"] = datetime.fromtimestamp(ts).strftime("%d/%m/%Y %H:%M")
                else:
                    movimento["data_formatada"] = "--/--/---- --:--"
    
            return movimentos
        
        except Exception as e:
            print(f"ERRO obter_historico: {e}")
            return []
        
    # ELIMINAR MOVIMENTO
    def eliminar_movimento(self, user_id, movimento_id):
        try:
            return self.service.eliminar_movimento(user_id, movimento_id)
        except Exception as e:
            print(f"ERRO eliminar_movimento controller: {e}")
            return False
