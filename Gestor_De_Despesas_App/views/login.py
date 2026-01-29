import flet as ft
from flet_lottie import Lottie
from controllers.login_controller import LoginController
from routes.rotas import ROTA_HOME, ROTA_REGISTO, ROTA_LOGIN, ROTA_REC_PASSWORD

def criar_login_view(page):

    # CHAMAMOS A NOSSA CLASSE
    controller = LoginController(page)

    # CRIAR OS CAMPOS
    # campo email 
    campo_email = ft.TextField(
        label="Email", 
        text_size=16,
        border_radius=12,
        color="black",
        focused_border_color="#0a85ff",
        hint_text="insira o seu email",
        width=280,
        height=45,

    )

    # campo password
    campo_password = ft.TextField(
        label="Palavra-passe", 
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        hint_text="insira a sua palavra-passe",
        width=280,
        height=45,
        color="black",
        password=True,
        can_reveal_password=True
    )

    # texto erro
    texto_erro = ft.Text(
        " ",
        color="red",
        size=12,
        weight="w400",
        text_align=ft.TextAlign.CENTER,
        visible=False,
    )

    # mensagem erro container
    mensagem_erro = ft.Container(
        content=texto_erro,
        height=35,
        margin=ft.margin.only(bottom=8),
        alignment=ft.alignment.center
    )

    # LOGIN BTN
    def func_btn_entrar(e):
        email = campo_email.value
        password = campo_password.value
        
        # acede a nossa função autenticar através da nossa classe LoginController()
        sucesso, msg= controller.autenticar(email, password)
        
        if not sucesso:
            texto_erro.value = msg
            texto_erro.visible = True
            campo_email.border_color = "red" if "Email" in msg else None
            campo_password.border_color = "red" if "palavra-passe" in msg else None
        else:
            texto_erro.visible = False
            page.go(ROTA_HOME)
        
        page.update()

    # evento click -> mudar rota para registo ao clicar em "Registe-se"
    def ir_para_registo(e):
        page.go(ROTA_REGISTO)

    def ir_para_rec_password(e):
        page.go(ROTA_REC_PASSWORD)

    #VIEW
    view = ft.View(
    ROTA_LOGIN,
    [
        ft.Column([

            # LOTTIE 
            ft.Container(
                Lottie(
                    "https://lottie.host/f41bf524-5ae6-465c-b0cc-29de62921ae0/7Y5Kykubbw.json",
                    width=120,
                    height=110,
                    repeat=True,
                    animate=True
                ),
                margin=ft.margin.only(bottom=25)
            ),

            # TEXT 
            ft.Text("Gestor de despesas", 
                    size=24,
                    weight='w600', 
                    color='#0a85ff',
                ),

            # TEXT
            ft.Text("Descomplique as suas despesas", 
                    size=12,
                    weight='w300', 
                    color='#0a85ff'
                ),

            # TEXT 
            ft.Container(
                ft.Text("Bem-vindo", 
                        size=18,
                        weight='w400', 
                        color='#0a85ff',
                    ),
                margin=ft.margin.only(top=30, bottom=30)
            ),

            # CAMPO EMAIL
            ft.Container(
                campo_email, 
                margin=ft.margin.only(bottom=15)
            ),

            # CAMPO PASSWORD
            ft.Container(
                campo_password,  
                margin=ft.margin.only(bottom=10)
            ),

            # MENSAGEM DE ERRO
            mensagem_erro,

            # TEXTBUTTON ESQUECEU PASSWORD
            ft.Container(
                ft.Row([
                    ft.TextButton(
                        text="Esqueceu a sua palavra-passe?",
                        style=ft.ButtonStyle(color="#0a85ff"),
                        on_click= ir_para_rec_password
                        )
                    ],
                    alignment="center",
                ),
                width=280,
                margin=ft.margin.only(bottom=15)
            ),

            # BOTÃO ENTRAR
            ft.Container(
                ft.ElevatedButton(
                    text="Entrar",
                    width=280,
                    height=50,
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor="#0a85ff",
                    ),
                    on_click=func_btn_entrar  # criar evento
                ),
            ),

            # TEXTBUTTON REGISTAR
            ft.Container(
                ft.Row([
                    ft.Text("Não tem uma conta?", color="#666666", size=14),
                    ft.TextButton(
                        text="Registe-se",
                        style=ft.ButtonStyle(color="#0a85ff"),
                        on_click=ir_para_registo, #evento de click
                    ),
                ],
                    width=280,
                    alignment="center",
            
                ),
                margin=ft.margin.only(bottom=10)
            ),
        ], 

        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE
        # permite fazer scroll suave quando o conteúdo não cabe no ecrã, adaptando-se automaticamente ao dispositivo
        )
    ],
    padding=10,
    bgcolor='white'
)   

    return view