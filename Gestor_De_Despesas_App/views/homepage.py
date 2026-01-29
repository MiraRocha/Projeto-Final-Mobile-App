import flet as ft

from controllers.homepage_controller import HomepageController
from components.barra_navegacao import criar_barra_navegacao
from components.saldo_card import criar_saldo_card
from components.categorias_info import CATEGORIAS_INFO
from routes.rotas import ROTA_HOME

def criar_homepage_view(page, user_id):
    
    # CHAMAMOS A NOSSAS CLASSE 
    controller = HomepageController(page, user_id)
    movimentos = controller.get_movimentos() # chamamos a nossa função que esta dentro da nossa classe HomepageController()


    # DADOS DO UTILIZADOR
    nome= controller.get_nome()

    #TEXT NOME UTILIZADOR
    nome_utilizador= ft.Text(
        nome, 
        size=15, 
        color="#0a85ff", 
        weight="w600"
    )

    # SALDO CARD
    saldo_card_container, atualizar_saldo= criar_saldo_card(page, user_id)

    # HISTÓRICO DE MOVIMENTOS (LISTA)
    lista_movimentos= ft.Column(
        controls=[],
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll= ft.ScrollMode.AUTO
        )
    
    # LISTA DE MOVIMENTOS CONTAINER
    lista_movimentos_container = ft.Container(
        content=lista_movimentos,
        width=300,
        height=240,
        bgcolor=None         
    )

    # fazer refresh a homepage a cada atualização 
    def refresh_homepage():
        # atualizar saldo
        atualizar_saldo()

        # atualizar movimentos
        # limpa a lista na interface e carrega novamente todos os movimentos atualizados do Firebase
        lista_movimentos.controls.clear() 
        novos_movimentos = controller.get_movimentos()

        # para cada movimento obtido do Firebase, cria o card visual na lista
        for movimento in novos_movimentos:
            criar_item_movimento(movimento)

        page.update()
    
    # SALDO CARD (AGORA RECEBE refresh_homepage)
    saldo_card_container, atualizar_saldo = criar_saldo_card(
        page, 
        user_id, 
        refresh_home_func=refresh_homepage
    )

    # cria o "card" visual de um movimento do histórico na homepage
    def criar_item_movimento(movimento):

        categoria = movimento.get("categoria", "Movimento")
        # categoria -> nome da categoria (ex: "Supermercado")
        valor_formatado = movimento.get("valor_formatado", "0.00€")
        # valor_formatado -> "-15.00€" já formatado
        data_formatada = movimento.get("data_formatada", "--/--/----")
        # data_formatada -> "03/02/2026 14:20"
        movimento_id = movimento.get("id")
        # movimento_id -> ID do Firestore (usado para eliminar)
        valor_original = movimento.get("valor", 0)
        # valor_original -> número real (ex: -15.50)

        # Se for atualização de saldo -> verde + icone poupança
        if movimento.get("mov_tipo_saldo"):
            cor = "#1a9b4c"
            icone = ft.Icons.SAVINGS
        else:
            # caso contrário se for despesa vai buscar a cor e o ícone da categoria ao ficheiro categorias_info.py
            info = CATEGORIAS_INFO.get(categoria, CATEGORIAS_INFO["Outros"])
            cor = info["cor"]
            icone = info["icone"]

        item = ft.Container(
            bgcolor=cor,
            border_radius=10,
            padding=10,
            margin=ft.margin.only(bottom=8),
            ink=True,
            on_click=lambda e: confirmar_eliminar_movimento(movimento_id, valor_original),
            content=ft.Row(
                [
                    # ícone da categoria
                    ft.Icon(icone, color="white", size=22),

                    # texto principal
                    ft.Column(
                        [
                            ft.Row(
                                [   
                                    #categoria
                                    ft.Text(
                                        categoria,
                                        size=14,
                                        weight="w600",
                                        color="white"
                                    ),
                                    ft.Text(
                                        valor_formatado,
                                        size=14,
                                        weight="w600",
                                        color="white"
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            # data
                            ft.Text(
                                data_formatada,
                                size=10,
                                color="white70"
                            )
                        ],
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            )
        )

        lista_movimentos.controls.append(item)


    # cria o comportamento do BottomSheet que aparece quando clicamos num movimento para o eliminar
    def confirmar_eliminar_movimento(movimento_id, valor):
        # eliminar -> apaga o movimento e atualiza a homepage
        def eliminar(e):
            sucesso= controller.eliminar_movimento(movimento_id)
            page.overlay.remove(bottomsheet_container)
            
            if sucesso:
                refresh_homepage()

            page.update()

        # cancelar -> fecha o BottomSheet sem fazer nada
        def cancelar(e):
            page.overlay.remove(bottomsheet_container)
            page.update()
            
        # BottomSheet
        conteudo_bottomsheet= ft.Column([
            ft.Text("Confirmar eliminar",
                    size=18, 
                    weight="w600", 
                    color="white"),
            ft.Text(
                f"Tem a certeza que quer eliminar:\n{valor:.2f}€ ?",
                size=14,
                color="white",
            ),
            ft.Row([
                ft.TextButton(
                    "Cancelar", 
                    on_click= cancelar, 
                    style= ft.ButtonStyle(color="white")),
                ft.TextButton("Eliminar", 
                            on_click= eliminar, 
                            style= ft.ButtonStyle(color="red")),

            ], alignment= ft.MainAxisAlignment.END)
        ], 
        tight= True
        )
        # BOTTOMSHEET CONTAINER
        bottomsheet_container= ft.BottomSheet(
            ft.Container(
                content=conteudo_bottomsheet,
                width=320,
                height=180,
                padding=20,
                alignment=ft.alignment.center,
                bgcolor="#0a85ff",
                border_radius=15,
            ),
            open= True, # faz com que apareça imediatamente
            bgcolor="#0a85ff"
        )

        # o BottomSheet é adicionado à overlay layer, uma camada flutuante por cima da página principal
        page.overlay.append(bottomsheet_container)
        page.update()

    # PREENCHER A LISTA COM AS DESPESAS
    for movimento in movimentos:
        criar_item_movimento(movimento)

    # VIEW 
    view = ft.View(
        ROTA_HOME,
        [
            ft.Container(
                content=ft.Column(
                    controls=[
                        # TEXTO 
                        ft.Container(
                            ft.Text(
                                "Bem-vindo!",
                                size=12,
                                weight="w300",
                                color="#666666"
                            ),
                            width=300,
                            alignment=ft.alignment.center_left,
                            margin=ft.margin.only(top=20),
                            padding=0,
                        ),
                        # NOME UTILIZADOR
                        ft.Container(
                            nome_utilizador,
                            width=300,
                            alignment=ft.alignment.center_left,
                            padding=0,
                        ),
                        # SALDO CARD
                        ft.Container(height=10),
                        saldo_card_container,
                        ft.Container(height=5),
                        # TEXTO HIST. TRANS
                        ft.Container(
                            ft.Text(
                                "Histórico de transações",
                                size=12,
                                weight="w500",
                                color="#666666"
                            ),
                            width=300,
                            alignment=ft.alignment.center_left,
                            padding=0
                        ),
                        # LISTA DE MOV
                        lista_movimentos_container,
                        # ESPAÇO FLEXÍVEL 
                        ft.Container(expand=True),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand= True,
            ),
            # MENU DE NAVEGAÇÃO
            criar_barra_navegacao(page, ROTA_HOME),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor='white',
        spacing=0
    )

    return view