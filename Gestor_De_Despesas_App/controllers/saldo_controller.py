from services.user_service import UserService
from controllers.movimentos_controller import MovimentosController

class SaldoController:
    def __init__(self):
        self.user_service= UserService()
        self.movimentos_controller= MovimentosController()

    # procurar saldo
    def obter_saldo(self, user_id):
        try:
            saldo= self.user_service.procurar_saldo(user_id)
            return  saldo
        except Exception as e:
            print(f"Erro ao obter saldo: {e}")
            return 0
        
    # atualizar saldo
    def guardar_saldo(self, user_id, novo_saldo):
        try:
            # limpar e validar
            if novo_saldo is None:
                return False, "Insira um valor."

            valor_str= str(novo_saldo).strip().replace("€", "").replace(" ", "").replace(",", ".")
            if not valor_str.replace(".", "", 1).isdigit():
                return False, "Por favor insira um valor válido."

            novo_saldo= float(valor_str)
            if novo_saldo <= 0:
                return False, "O saldo tem que ser maior que zero."

            # obter saldo anterior
            saldo_anterior= self.user_service.procurar_saldo(user_id)

            # registar movimento saldo
            sucesso, resultado= self.movimentos_controller.registar_saldo(
                user_id= user_id,
                novo_saldo= novo_saldo,
                saldo_anterior= saldo_anterior
            )

            if sucesso:
                return True, "Saldo atualizado!"
            else:
                return False, resultado

        except Exception as e:
            print(f"Erro no controller de saldo: {e}")
            return False, "Erro inesperado."

    # atualizar saldo 
    def atualizar_saldo(self, user_id, valor):
        try:
            return self.user_service.atualizar_saldo(user_id, valor)
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return False

