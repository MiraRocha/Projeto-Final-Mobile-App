# iniciar do Firebase (admin + pyrebase)
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import os #biblioteca para aceder a variáveis de ambiente e funcionalidades do sistema operativo
from dotenv import load_dotenv

#carregar as chaves do ficheiro .env
load_dotenv()

class FirebaseInit:
    # o prefixo "_" indica que estas variáveis são internas/privadas ao módulo
    # variáveis iniciadas como None: só serão criadas quando forem necessárias
    _db= None # ligação ao Firestore
    _auth= None  # ligação ao Pyrebase Auth

    @staticmethod # @staticmethod -> método da classe que não usa 'self'
    # funciona como função normal, mas mantida dentro da classe por organização.
    def initialize():
        # FIREBASE ADMIN (FIRESTORE)
        try:
            firebase_admin.get_app() #get_app() -> evita dupla inicialização
            # Se já existir uma app Firebase, usa-a
            # Se não existir, lança ValueError
        except ValueError:
            #usar variável de ambiente
            caminho = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
            cred= credentials.Certificate(caminho)
            firebase_admin.initialize_app(cred)

        # GUARDAR LIGAÇÃO AO FIRESTORE
        FirebaseInit._db= firestore.client()

        # PYREBASE (Autenticação) COM VARIÁVEIS DE AMBIENTE
        #manda o mensageiro buscar cada chave
        firebaseConfig = {
            'apiKey': os.getenv('FIREBASE_API_KEY'), #os.getenv() obtém credenciais do Firebase a partir de variáveis de ambiente para manter a segurança
            'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
            'projectId': os.getenv('FIREBASE_PROJECT_ID'),
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
            'databaseURL': os.getenv('FIREBASE_DATABASE_URL'), 
            'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'), 
            'appId': os.getenv('FIREBASE_APP_ID')
        }

        # validação das variáveis necessárias
        if None in firebaseConfig.values():
            raise ValueError("Variáveis de ambiente do Firebase não encontradas!")
            # raise é uma palavra-chave em Python usada para lançar exceções manualmente.

        firebase = pyrebase.initialize_app(firebaseConfig)
        FirebaseInit._auth = firebase.auth()

    @staticmethod
    def db():
        if FirebaseInit._db is None:
            FirebaseInit.initialize()
        return FirebaseInit._db
        
    @staticmethod
    def auth():
        if FirebaseInit._auth is None:
            FirebaseInit.initialize()
        return FirebaseInit._auth