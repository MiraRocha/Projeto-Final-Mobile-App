from services.auth_service import AuthService
from services.user_service import UserService

class RegistoController:
    def __init__(self, page):
        self.page= page
        self.user_service= UserService()
        self.auth_service= AuthService()

    #REGISTO
    def registar(self, nome, email, password, confirmar_password):
        #validações
        if not nome or not email or not password or not confirmar_password:
            return False, "Todos os campos devem ser preenchidos."
        
        if password != confirmar_password:
            return False, "A palavra-passe não coincide."
        
        if len(password) < 6:
            return False, "A palavra-passe deve ter pelo menos 6 caracteres."
        
        #REGISTO FIREBASE
        try:
            user= self.auth_service.register(email, password)

            if user is None:
                return False, "Erro ao criar conta. Verifique os dados."
            
            #login automático após o registo
            login_user= self.auth_service.login(email, password)

            user_id= login_user['localId']
            
            # GUARDAR NO FIRESTORE
            self.user_service.guardar_utilizador(user_id, nome, email)

            return True, None
        except Exception as e:
            erro = str(e)
            
            #Firebase devolve: "EMAIL_EXISTS" -> email já registado EM QUALQUER app Firebase
            if "EMAIL_EXISTS" in erro:
                return False, "Este email já está registado."
            if "INVALID_EMAIL" in erro:
                return False, "Email inválido."
            if "WEAK_PASSWORD" in erro:
                return False, "Palavra-passe muito fraca."

            return False, f"Erro no registo: {erro}"