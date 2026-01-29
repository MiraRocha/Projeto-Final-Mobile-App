import flet as ft
from flet_lottie import Lottie
import threading
import time
from controllers.registo_controller import RegistoController
from routes.rotas import ROTA_REGISTO, ROTA_LOGIN
def criar_registo_view(page):

    # CHAMAMOS A NOSSA CLASSE
    controller = RegistoController(page)

    # CRIAR OS CAMPOS
    # campo nome
    campo_nome =ft.TextField(
        label="Nome",
        text_size=16,
        border_radius=12,
        color="black",
        focused_border_color="#0a85ff",
        hint_text="insira o seu nome",
        width=280,
        height=45,
    )

    # campo nome
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
        color="black",
        focused_border_color='#0a85ff',
        hint_text="insira a sua palavra-passe",
        width=280,
        height=45,
        password=True,
        can_reveal_password=True
    )

    # campo confirmar password
    campo_confirmar_password = ft.TextField(
        label="Confirmar palavra-passe",
        text_size=16,
        border_radius=12,
        color="black",
        focused_border_color='#0a85ff',
        hint_text="confirme a sua palavra-passe",
        width=280,
        height=45,
        password=True,
        can_reveal_password=True
    )

    # mensagem texo de erro/sucesso
    texto_mensagem= ft.Text(
        " ",
        color='red',
        size=14,
        weight="w400",
        text_align=ft.TextAlign.CENTER,
    )

    #mensagem container
    mensagem_container= ft.Container(
        content=texto_mensagem,
        height=40,
        margin=ft.margin.only(bottom=8),
        alignment=ft.alignment.center
    )

    # EVENTO BTN REGISTAR
    def func_btn_registo(e):
        nome = campo_nome.value
        email = campo_email.value
        password = campo_password.value
        confirmar_password = campo_confirmar_password.value

        # acede a nossa função registar através da nossa classe RegistoController()
        sucesso, msg = controller.registar(nome, email, password, confirmar_password)

        if not sucesso:
            texto_mensagem.value = msg
            texto_mensagem.color = "red"
            texto_mensagem.visible = True
        else:
            texto_mensagem.value = "Conta criada com sucesso!"
            texto_mensagem.color = "green"
            texto_mensagem.visible = True

        # voltar ao login após 2 segundos
            def voltar_automatico():
                time.sleep(2)
                page.go(ROTA_LOGIN)

            # executa voltar_automatico() numa thread em segundo plano (não bloqueia a app)
            threading.Thread(target=voltar_automatico, daemon=True).start()

        page.update()

    #EVENTO VOLTAR PARA O LOGIN
    def voltar_para_login(e):
        page.go(ROTA_LOGIN)

    view = ft.View(
        ROTA_REGISTO,
        [   
            #container para expandir e centralizar o conteudo
            ft.Container(
                content=ft.Column(
                    controls=[
                        # LOTTIE 
                        ft.Container(
                        Lottie(
                            "https://lottie.host/37bda325-757c-4878-ad68-afe87d58f8a3/AfixS7M8Nt.json",
                            width=120,
                            height=110,
                            repeat=True,
                            animate=True
                            ),
                            margin=ft.margin.only(bottom=25, top=30)
                        ),

                        #TEXT 
                        ft.Text(
                            "Registo de conta",
                            size=24,
                            weight='w600',
                            color='#0a85ff',
                            text_align=ft.TextAlign.CENTER,
                        ),
                        
                        #CAMPO NOME
                        ft.Container(
                            campo_nome,
                            margin=ft.margin.only(bottom=15)
                        ),

                        #CAMPO EMAIL
                        ft.Container(
                            campo_email,
                            margin=ft.margin.only(bottom=15),
                        ),

                        #CAMPO PASSWORD
                        ft.Container(
                            campo_password,
                            margin=ft.margin.only(bottom=15),
                        ),
                        
                        #CAMPO CONFIRMAR PASSWORD
                        ft.Container(
                            campo_confirmar_password,
                            margin=ft.margin.only(bottom=15)
                        ),
                        
                        # MENSAGEM DE ERRO
                        mensagem_container,

                        #BTN REGISTAR
                        ft.Container(
                            ft.ElevatedButton(
                                text="Registar",
                                width=280,
                                height=50,
                                style=ft.ButtonStyle(
                                    color="white",
                                    bgcolor="#0a85ff",
                                ),
                                on_click= func_btn_registo
                            ),
                            margin=ft.margin.only(bottom=20)
                        ),
                        #TEXT + BUTTONTEXT
                        ft.Container(
                            ft.Row([
                                ft.Text("Já tem uma conta?", color="#666666", size=14),
                                ft.TextButton(
                                    text="Faça login",
                                    style=ft.ButtonStyle(color="#0a85ff"),
                                    on_click=voltar_para_login #evento de click
                                ),
                            ],
                            width=280,
                            alignment='center',
                        ),
                    ),

                ],
                horizontal_alignment='center',
                ),
                #horizontal_alignment=ft.CrossAxisAlignment.CENTER -> com menos conteúdo não funciona
                expand=True,  #estica para ocupar todo o espaço disponível
                alignment=ft.alignment.center 
            )
        ],
        padding=0,
        bgcolor='white',
    )

    return view