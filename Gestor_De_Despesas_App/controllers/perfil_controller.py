from services.user_service import UserService

class PerfilController:
    def __init__(self):
        self.user_service= UserService()

    def obter_perfil(self, user_id):

        # buscar dados do perfil ao firebase
        user= self.user_service.procurar_utilizador(user_id)
        return user if user else {}

    def guardar_perfil(self, user_id, nome, endereco, contacto, avatar):

        # atualiza o perfil do utilizador com os novos dados
        try:
            dados= {
                "nome": nome,
                "endereco": endereco,
                "contacto": contacto,
                "avatar": avatar
            }

            # através da nossa classe UserService() aderimos à nossa função atualizar_perfil()
            self. user_service.atualizar_perfil(user_id, dados)
            return True, "Perfil atualizado com sucesso"
        
        except Exception as e:
            print(f"Erro ao guardar perfil: {e}")
            return False, "Erro ao atualizar o perfil."
    
    # eliminar conta
    def eliminar_conta(self, user_id):
        return self.user_service.eliminar_conta(user_id)