# Definir que página abrir
# verificar se o utilizador está utenticado
# definir rotas transição de páginas
import flet as ft
from services.auth_service import AuthService

from views.splash_screen import criar_splash_view
from views.login import criar_login_view
from views.registo_conta import criar_registo_view
from views.homepage import criar_homepage_view
from views.add_despesas import criar_add_despesas_view
from views.estatistica import criar_estatistica_view
from views.rec_password import criar_rec_password_view
from views.perfil import criar_perfil_view
from routes.rotas import ROTA_SPLASH, ROTA_LOGIN, ROTA_PERFIL, ROTA_STATS, ROTA_ADD, ROTA_HOME, ROTA_REGISTO, ROTA_REC_PASSWORD

class RouterController:
    def __init__(self, page: ft.Page):
        self.page= page
        self.auth_service = AuthService()

    # nossa função "GPS"
    def mudar_rota(self, route):
        self.page.views.clear() # limpar todas as páginas atuais

        # Splash
        if self.page.route == ROTA_SPLASH: # "/" -> é a nossa sala de entrada
            self.page.views.append(criar_splash_view(self.page))

        # Login
        elif self.page.route == ROTA_LOGIN:
            self.page.views.append(criar_login_view(self.page))

        # Registo
        elif self.page.route == ROTA_REGISTO:
            self.page.views.append(criar_registo_view(self.page))

        # Homepage
        elif self.page.route == ROTA_HOME:
            user_id = self.page.session.get("user_id")
            #verifica se está autenticado
            if user_id:
                self.page.views.append(criar_homepage_view(self.page, user_id))
            else:
                self.page.go(ROTA_LOGIN) # se não está autenticado, vai para login

        # Adicionar despesas
        elif self.page.route == ROTA_ADD:
            self.page.views.append(criar_add_despesas_view(self.page))

        # Estatística
        elif self.page.route == ROTA_STATS:
            self.page.views.append(criar_estatistica_view(self.page))

        # Recuperação de password
        elif self.page.route == ROTA_REC_PASSWORD:
            self.page.views.append(criar_rec_password_view(self.page))

        # Perfil
        elif self.page.route == ROTA_PERFIL:
            self.page.views.append(criar_perfil_view(self.page))

        self.page.update()