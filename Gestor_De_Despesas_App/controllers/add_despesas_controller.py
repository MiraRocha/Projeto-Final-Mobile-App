from services.user_service import UserService
from controllers.movimentos_controller import MovimentosController

class AddDespesasController:
    def __init__(self):
        self.movimentos_controller= MovimentosController()
        self.user_service = UserService()

    # OBTER A LISTA DAS CATEGORIAS FIXA
    def obter_categorias(self):
        return ["Supermercado", "Restaurante", "Transporte", "Netflix",
                "Educação", "Saúde", "Lazer", "Gym", "Outros"]
    
    # VALIDAR E REGISTAR DESPESA
    def adicionar_despesa(self, user_id, categoria_dropdown, categoria_personalizada, montante, data):
        try:
            # validar montante
            if not montante:
                return False, "Insira um montante."
            try:
                # se o utilizador escrever com "," o replace vai substituir po "." para não haver erros
                montante= float(str(montante).replace(",", "."))
            except:
                return False, "Montante inválido."

            if montante <= 0:
                return False, "O montante deve ser maior que zero."

            # validar categoria
            if categoria_dropdown == "":
                return False, "Escolha uma categoria."

            if categoria_dropdown == "Outros":
                if not (categoria_personalizada and categoria_personalizada.strip()): # strip() -> para remover todos os espaços em branco
                    return False, "Insira uma categoria."
                categoria = categoria_personalizada.strip()
            else:
                categoria = categoria_dropdown

            # data já vem formatada do UI
            if not data:
                return False, "Data inválida."


            # verificar saldo disponível
            saldo_atual = self.user_service.procurar_saldo(user_id)
            if saldo_atual is None:
                return False, "Utilizador não encontrado."

            if montante > saldo_atual:
                return False, "Saldo insuficiente."

            # REGISTAR DESPESA (E ATUALIZAR SALDO AUTOMATICAMENTE)
            # a função registar_despesas() devolve um tuplo com dois valores -> estado de operação e mensagem correspondente
            # então temos de ter duas variáveis, uma para saber se o registo foi bem-sucedido, e outra para guardar a mensagem de erro ou sucesso.
            sucesso, resultado = self.movimentos_controller.registar_despesa(
                user_id, categoria, montante)
            
            if not sucesso:
                return False, resultado
            
            # se deu erro -> devolvemos o erro para o UI mostrar ao utilizador

            # se deu certo -> devolvemos a mensagem de confirmação

            return True, "Despesa adicionada com sucesso!"

        except Exception as e:
            print(f"ERRO adicionar_despesa: {e}")
            return False, "Erro inesperado."
