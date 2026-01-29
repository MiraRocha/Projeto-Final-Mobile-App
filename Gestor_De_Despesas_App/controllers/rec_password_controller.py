from services.firebase_init import FirebaseInit

class RecPasswordController:
    def __init__(self):
        self.auth= FirebaseInit.auth()

    def recuperar_password(self, email):
        try: 
            if not email:
                return False, "Insira o email."
                
            self.auth.send_password_reset_email(email)
            return True, "Email de recuperação enviado!"

        except Exception as e:
            print(f"Erro ao enviar recuperação: {e}")
            return False, "Email inválido ou não registado."
            