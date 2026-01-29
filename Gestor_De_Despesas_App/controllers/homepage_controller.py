from services.user_service import UserService 
from controllers.saldo_controller import SaldoController
from controllers.movimentos_controller import MovimentosController

class HomepageController:
    def __init__(self, page, user_id):
        self.page = page
        self.user_id = user_id
        
        self.user_service = UserService()
        self.saldo_controller = SaldoController()
        self.movimentos_controller = MovimentosController()

    # OBTER NOME DO UTILIZADOR
    def get_nome(self):
        user = self.user_service.procurar_utilizador(self.user_id)
        if user and "nome" in user:
            return user['nome']
        return "Utilizador"
    
    # OBTER LISTA DE MOVIMENTOS, SALDO + DESPESAS
    def get_movimentos(self):
        try:
            return self.movimentos_controller.obter_movimentos(self.user_id)
        except Exception as e:
            print(f"Erro ao obter movimentos: {e}")
            return []
        
    # ATUALIZAR SALDO
    def atualizar_saldo(self):
        return self.saldo_controller.obter_saldo(self.user_id)

    # ELIMINAR MOVIMENTOS
    def eliminar_movimento(self, movimento_id):
        try:
            return self.movimentos_controller.eliminar_movimento(self.user_id, movimento_id)
        except Exception as e:
            print(f"Erro ao eliminar movimento: {e}")
            return False
    
    