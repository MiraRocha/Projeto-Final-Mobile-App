import time
from datetime import datetime
from services.firebase_init import FirebaseInit
from services.user_service import UserService

class MovimentosService:
    def __init__(self):
        self.db= FirebaseInit.db()
        self.user_service = UserService()

    # GUARDAR UM MOVIMENTO DE DESPESA OU SALDO
    def guardar_movimento(self, user_id, movimento):
        try:
            # garantir timestamp
            movimento["timestamp"]= time.time()

            # garantir data formatada para UI
            movimento["data_formatada"] = datetime.now().strftime("%d/%m/%Y")

            # guardar movimento no firestore
            resultado, ref= self.db.collection("movimentos").document(user_id).collection("registos").add(movimento)
            movimento_id= ref.id

            # atualizar saldo automaticamente
            valor = movimento.get("valor", 0)
            saldo_atual = self.user_service.procurar_saldo(user_id)

            # NOVO SALDO = saldo atual + valor (despesa é negativa, saldo é positivo)
            novo_saldo = saldo_atual + valor

            # gravar novo saldo no Firebase
            self.user_service.guardar_saldo(user_id, novo_saldo)

            return movimento_id
        except Exception as e:
            print(f"Erro ao guardar movimento: {e}")
            return False
        
    #OBTER MOVIMENTOS
    def obter_movimentos(self, user_id):
        try:
            docs= (
                self.db.collection("movimentos")
                .document(user_id)
                .collection("registos")
                .order_by("timestamp", direction="DESCENDING")
                .stream()
            )

            movimentos= [] # lista vazia para guardar movimentos

            # percorremos todos os documentos do firebase
            for doc in docs:
                item= doc.to_dict() # convertemos o documento em um dicionario Python
                item["id"]= doc.id # adiciona manualmente o ID do documento ao dicionario
                movimentos.append(item) 

            return movimentos
        
        except Exception as e:
            print(f"Erro ao obter movimentos: {e}")
            return []
        
    def eliminar_movimento(self, user_id, movimento_id):
        # elimina um movimento
        # se a despesa for valor negativo repõem ao saldo
        # assume que cada movimento tem 'valor' e opcionalmente 'tipo'
        try:    
            doc_ref= self.db.collection("movimentos").document(user_id).collection("registos").document(movimento_id)
            doc = doc_ref.get()
            if not doc.exists:
                print("Movimento não encontrado.")
                return False
            
            movimento= doc.to_dict()
            valor= float(movimento.get("valor", 0))
            tipo= movimento.get("tipo", "")

            # apagar o documento
            doc_ref.delete()

            # ROLLBACK DO SALDO
            saldo_atual = self.user_service.procurar_saldo(user_id)

            if tipo == "despesa" or valor < 0:
                # eliminar despesa -> REPOR saldo (somar)
                novo_saldo = saldo_atual + abs(valor)

            elif tipo == "saldo" and valor > 0:
                # eliminar atualização de saldo -> VOLTAR AO SALDO ANTERIOR (subtrair)
                novo_saldo = saldo_atual - valor

            else:
                # fallback seguro
                novo_saldo = saldo_atual

            # atualizar saldo no Firebase
            self.user_service.guardar_saldo(user_id, novo_saldo)

            return True
        except Exception as e:
            print(f"Erro ao eliminar movimento: {e}")
            return False