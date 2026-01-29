# login, register, logout via pyrebase
from services.firebase_init import FirebaseInit

class AuthService:
    def __init__(self):
        self.auth= FirebaseInit.auth()
        self.current_user= None

    # LOGIN
    # tenta autenticar no Firebase com email e password.
    # se o login for bem-sucedido, guarda o utilizador atual e devolve o user.
    # se falhar (password errada, email inválido, etc.), devolve None.
    def login(self, email, password):
        try:
            user= self.auth.sign_in_with_email_and_password(email, password)
            self.current_user= user 
            return user
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return None
        
    # REGISTO  
    # mesma coisa que no login, mas ao registar 
    def register(self, email, password):
        try:
            user= self.auth.create_user_with_email_and_password(email, password)
            self.current_user = user 
            return user
        except Exception as e:
            print(f"Erro ao registar: {e}")
            return None

    # LOGOUT  
    def logout(self):
        try: 
            self.auth.current_user= None
            return True
        except:
            return False