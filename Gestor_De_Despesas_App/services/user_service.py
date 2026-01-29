# guardar/procurar utilizadores + receita + saldo
import time
from firebase_admin import auth
from services.firebase_init import FirebaseInit

class UserService:
    def __init__(self):
        self.db = FirebaseInit.db()

    #GUARDAR UTILIZADOR
    def guardar_utilizador(self, user_id, nome, email):
        try:
            self.db.collection("users").document(user_id).set({  #document()-> escolhe o ficheiro, set() ->guarda este conteudo
                "nome": nome,
                "email": email,
                "data_registo": time.time(),
            })
            return True
        except Exception as e:
            print(f"Erro ao guardar utilizador: {e}")
            return False

    #PROCURAR UTILIZADOR
    def procurar_utilizador(self, user_id):
        try:
            doc = self.db.collection("users").document(user_id).get()
            return doc.to_dict() if doc.exists else None  #to_dict() -> converte um documento do Firestore para um dicionário Python
        except Exception as e:
            print(f"Erro ao procurar utilizador: {e}")
            return None

    #GUARDAR RECEITA
    def guardar_saldo(self, user_id, saldo):
        try:
            #acedemos à nossa coleção da base de dados e fazemos um update()
            self.db.collection("users").document(user_id).update({
                "saldo_atual": float(saldo)  
            })
            return True
        except Exception as e:
            print(f"Erro ao guardar saldo: {e}")
            return False

    #PROCURAR RECEITA
    def procurar_saldo(self, user_id):
        try:
            doc = self.db.collection("users").document(user_id).get()  #acedemos à nossa coleção "users", ao seu documento especifico onde vamos buscar os dados do documento
            if not doc.exists:
                return 0

            data = doc.to_dict()  #convertemos para um dicionario Python
            
            saldo_atual = float(data.get('saldo_atual', 0))

            return saldo_atual
        
        except Exception as e:
            print(f"Erro ao procurar saldo: {e}")
            return 0

    #ATUALIZAR SALDO
    def atualizar_saldo(self, user_id, valor_despesa):
        try:
            #impedimos valores negativos
            if valor_despesa <= 0:
                return False

            doc = self.db.collection("users").document(user_id).get()  #vamos buscar os dados do utilizador na nossa base de dados
            if not doc.exists:
                return False

            data = doc.to_dict()  # voltamos a converter num dicionario
            saldo = data.get('saldo_atual', 0)  #procuramos o saldo se não existir retorna valor padrão 0

            if valor_despesa > saldo:  #impedimos que as despesas sejam maiores que o saldo atual
                print("Saldo insuficiente")
                return False

            #calculamos o nosso saldo atual -> o valor da despesa que irá sair 
            novo_saldo = saldo - valor_despesa

            self.db.collection("users").document(user_id).update({  #fazemos update à nossa base de dados para que o saldo atualize 
                "saldo_atual": novo_saldo
            })
            return True
        except Exception as e:
            print(f"Erro ao atualizar saldo: {e}")
            return False
    
    # ATUALIZAR PERFIL   
    def atualizar_perfil(self, user_id, dados):
        # atualliza os campos do perfil no Firestore
        # só atualiza os campos enviados no dicionário
        try:
            self.db.collection("users").document(user_id).update(dados)
            return True

        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
            return False
        
    # ELIMINAR CONTA
    def eliminar_conta(self, user_id):
        try:
            # Apagar subcoleção "movimentos" do utilizador
            movimentos_ref = (self.db.collection("users").document(user_id).collection("movimentos"))
            for documento in movimentos_ref.stream():
                documento.reference.delete()

            # Apagar documento principal do utilizador
            self.db.collection("users").document(user_id).delete()

            # (Não elimina do Authentication, mais seguro)
            return True, "Conta eliminada com sucesso."

        except Exception as e:
            print(f"Erro ao eliminar conta: {e}")
            return False, "Erro ao eliminar conta."

