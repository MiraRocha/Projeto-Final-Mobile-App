import flet as ft
from flet_lottie import Lottie
from controllers.rec_password_controller import RecPasswordController
from routes.rotas import ROTA_LOGIN, ROTA_REC_PASSWORD

def criar_rec_password_view(page):

    controller= RecPasswordController()

    campo_email= ft.TextField(
        label= "Email",
        hint_text= "Insira o seu email",
        text_size=16,
        width=280,
        border_radius=12,
        focused_border_color= "#0a85ff",
    )

    texto_mensagem= ft.Text(
        "",
        size=12,
        color= "red",
        visible= False
    )

    # ENVIAR REDEFINICAO
    def enviar_redefinicao(e):

        email= campo_email.value
        sucesso, msg= controller.recuperar_password(email)

        texto_mensagem.value= msg
        texto_mensagem.color= "green" if sucesso else "red"
        texto_mensagem.visible= True

        page.update()
    
    # VOLTAR PARA O LOGIN
    def voltar_login(e):
        page.go(ROTA_LOGIN)

    view= ft.View(
        ROTA_REC_PASSWORD,
        [
            ft.Column(
                controls=[
                    ft.Text(
                        "Recuperar Palavra-passe",
                        size=22,
                        weight="bold",
                        color="#0a85ff"
                        ),
                        
                        # LOTTIE 
                        ft.Container(
                            Lottie(
                                "https://lottie.host/9d6725e3-66c8-4994-b128-76bd8a3cc893/JYEMUJ4aDa.json",
                                width=120,
                                height=120,
                                repeat=True,
                                animate=True
                                ),
                                margin=ft.margin.only(bottom=25)
                            ),
                        campo_email,
                        texto_mensagem,

                        ft.ElevatedButton(
                            text="Enviar Email",
                            width=280,
                            height=45,
                            on_click= enviar_redefinicao,
                            style= ft.ButtonStyle(
                                color="white",
                                bgcolor= "#0a85ff"
                            )
                        ),

                        ft.TextButton(
                            "Voltar ao Login",
                            on_click= voltar_login,
                            style= ft.ButtonStyle(color= "#0a85ff")
                        )
                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing= 20
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20,
        bgcolor= "white"
    )

    return view