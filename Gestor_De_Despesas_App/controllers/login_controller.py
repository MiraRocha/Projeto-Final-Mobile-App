from services.auth_service import AuthService

class LoginController:
    def __init__(self, page):
        self.page= page 
        self.auth_service= AuthService()

    def autenticar(self, email, password):
        # validar campos
        if not email and not password:
            return False, "Email e palavra-passe são obrigatórios!"
        
        if not email: 
            return False, "O email é obrigatório!"
        
        if not password:
            return False, "A palavra-passe é obrigatória!"
        
        #autenticar
        user= self.auth_service.login(email, password)

        if user is None:
            return False, "Credenciais inválidas ou erro no login."
        
        #guardar sessão
        user_id= user['localId']
        self.page.session.set("user_id", user_id)

        return True, None