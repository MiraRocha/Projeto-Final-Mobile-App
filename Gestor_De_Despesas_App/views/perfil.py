import flet as ft

from controllers.perfil_controller import PerfilController
from components.barra_navegacao import criar_barra_navegacao
from routes.rotas import ROTA_HOME, ROTA_LOGIN, ROTA_PERFIL

def criar_perfil_view(page):

    controller= PerfilController()
    user_id= page.session.get("user_id")

    dados= controller.obter_perfil(user_id)

    # campos carregados do Firebase
    # campo nome
    nome_field= ft.TextField(
        label= "Nome",
        value= dados.get("nome", ""),
        text_size=16,
        border_radius=12,
        width=280,
        height=40,
        color="black",
        focused_border_color="#0a85ff",
    )

    # campo endereço
    endereco_field= ft.TextField(
        label= "Endereço",
        value= dados.get("endereco", ""),
        text_size=16,
        border_radius=12,
        width=280,
        height=40,
        color="black",
        focused_border_color="#0a85ff",
    )

    # campo email
    email_field= ft.TextField(
        label= "Email",
        value= dados.get("email", ""),
        read_only= True,
        text_size=16,
        border_radius=12,
        width=280,
        height=40,
        color="black",
        focused_border_color="#0a85ff",
    )

    # campo contacto
    contacto_field= ft.TextField(
        label= "Contacto",
        value= dados.get("contacto", ""),
        text_size=16,
        border_radius=12,
        width=280,
        height=40,
        color="black",
        focused_border_color="#0a85ff",
    )

    # avatares disponíveis
    AVATARES = [
        "avatar_fem_1",
        "avatar_fem_2",
        "avatar_fem_3",
        "avatar_fem_4",
        "avatar_fem_5",
        "avatar_masc_1",
        "avatar_masc_2",
        "avatar_masc_3",
        "avatar_masc_4",
        "avatar_masc_5",
    ]

    avatar_selecionado= dados.get("avatar", "avatar_fem_1")


    def avatar_path(a):
        return f"assets/{a}.png"
    
    # Avatar grande
    avatar_img= ft.Image(
        src= avatar_path(avatar_selecionado),
        width=90,
        height=90,
        border_radius =45,
        fit= ft.ImageFit.COVER # COVER faz a imagem preencher todo o espaço, cortando o excesso sem distorcer
    )

    # Flag para mostrar/ocultar grelha
    mostrar_grelha = False

    # Container que vai conter a grelha
    grelha_container= ft.Container(padding=5, visible=False,)
    
    def alternar_grelha(e):
        nonlocal mostrar_grelha
        mostrar_grelha=  not mostrar_grelha
        grelha_container.visible= mostrar_grelha
        page.update()

    # Selecionar avatar
    def selecionar_avatar(a):
        nonlocal avatar_selecionado
        avatar_selecionado = a
        avatar_img.src = avatar_path(a)
        atualizar_grelha()
        grelha_container.visible = False # fecha a grelha
        page.update()

    # FIX para lambda capturar o avatar certo
    def make_handler(a):
        return lambda e: selecionar_avatar(a)

    # Grelha avatares
    # gera os mini-avatares com borda
    avatar_grid = ft.Row(wrap=True, spacing=10, alignment=ft.MainAxisAlignment.CENTER)

    def atualizar_grelha():
        avatar_grid.controls.clear()
        for avatar in AVATARES:
            is_selecionado = avatar == avatar_selecionado
            avatar_grid.controls.append(
                ft.Container(
                    content=ft.Image(
                        src=avatar_path(avatar),
                        width=55,
                        height=55,
                        fit=ft.ImageFit.COVER
                    ),
                    width=60,
                    height=60,
                    border_radius=30,
                    border=ft.border.all(3, "#0a85ff") if is_selecionado else None,
                    on_click= make_handler(avatar),
                )
            )
        grelha_container.content = avatar_grid
    
    # inicializa a grelhas mas escondida
    atualizar_grelha()
    
    # Guardar Perfil
    def guardar(e):
        sucesso, msg= controller.guardar_perfil(
            user_id,
            nome_field.value,
            endereco_field.value,
            contacto_field.value,
            avatar_selecionado
        )
        page.update()

    # Logout
    def logout(e):
        page.session.clear()
        page.go(ROTA_LOGIN)

    # Eliminar conta
    def confirmar_eliminar_conta(e):
        page.overlay.append(bottomsheet)
        bottomsheet.open= True
        page.update()

    # Cancelar
    def cancelar(e):
        bottomsheet.open= False
        page.update()

    def eliminar_definitivo(e):
        
        sucesso, msg = controller.eliminar_conta(user_id)
        page.overlay.remove(bottomsheet)

        if sucesso:
            page.session.clear()
            page.go(ROTA_LOGIN)
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(msg),
                bgcolor="red",
                open=True
            )
        page.update()

    # BottomSheet
    bottomsheet= ft.BottomSheet(
        content= ft.Container(
            padding=20,
            content= ft.Column([
                ft.Text(
                    "Eliminar conta?",
                    size= 18,
                    weight= "bold",
                    color= "white"
                ),

                ft.Text(
                    "Esta ação é irreversível. Todos os seus dados serão apagados.",
                    color="white70"
                ),
                ft.Row([
                    ft.TextButton(
                        "Cancelar",
                        on_click= cancelar,
                        style= ft.ButtonStyle(
                            color= "white"
                        )
                    ),

                    ft.TextButton(
                        "Eliminar", 
                        on_click=eliminar_definitivo, 
                        style=ft.ButtonStyle(
                            color="red"
                            )
                        )
                ], 
                alignment= ft.MainAxisAlignment.END
                )
            ])
        ),
        bgcolor="#0a85ff",
        open=False
    )
    # adicionar bottomsheet ao overlay (mantém-o disponível)
    page.overlay.append(bottomsheet)

    # BOTÃO ELIMINAR
    btn_eliminar = ft.ElevatedButton(
        "Eliminar Conta",
        bgcolor="red",
        color="white",
        on_click=confirmar_eliminar_conta,
        width=200
    )

    view = ft.View(
    ROTA_PERFIL,
    controls=[
        ft.Column(
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[

                ft.Container(
                    expand=True,
                    padding=10,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                        controls=[
                            ft.Text("Perfil", size=22, weight="bold", color="#0a85ff"),

                            ft.Container(padding=6),

                            avatar_img,

                            ft.TextButton(
                                "Escolher Avatar",
                                on_click=alternar_grelha,
                                style=ft.ButtonStyle(color="#0a85ff"),
                            ),
                            # grelha container
                            grelha_container,
                            
                            # campos field
                            nome_field,
                            endereco_field,
                            email_field,
                            contacto_field,
                        ],
                    ),
                ),
                # BOTÕES FIXOS NO FUNDO
                ft.Container(
                    bgcolor="white",
                    padding=10,
                    content=ft.Column(
                        spacing=8,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Atualizar Perfil",
                                        width=120,
                                        on_click=guardar,
                                        style=ft.ButtonStyle(color="white", bgcolor="#0a85ff"),
                                    ),
                                    ft.ElevatedButton(
                                        "Terminar Sessão",
                                        width=120,
                                        on_click=logout,
                                        style=ft.ButtonStyle(color="white", bgcolor="#0a85ff"),
                                    ),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),

                            btn_eliminar,
                        ],
                    ),
                ),
                # BARRA DE NAVEGAÇÃO
                criar_barra_navegacao(page, ROTA_HOME),
            ],
        )
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    bgcolor="white",
    spacing=0
)


    return view
