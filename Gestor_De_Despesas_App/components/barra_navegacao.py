import flet as ft
from routes.rotas import ROTA_HOME, ROTA_ADD, ROTA_STATS, ROTA_PERFIL

def criar_barra_navegacao(page, pagina_atual=ROTA_HOME): 

    #CORES DINAMICAS
    def obter_cor_icone(rota_icone):
        return "#0a85ff" if pagina_atual == rota_icone else "#666666"

    # Funções de navegação
    def ir_para(rota):
        page.go(rota)

    barra_de_navegacao = ft.Container(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.HOME,
                        icon_size=28,
                        icon_color=obter_cor_icone(ROTA_HOME),
                        on_click= lambda e: ir_para(ROTA_HOME),
                        tooltip="Home"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.BAR_CHART,
                        icon_size=28,
                        icon_color= obter_cor_icone(ROTA_STATS),
                        on_click= lambda e: ir_para(ROTA_STATS),
                        tooltip="Estatística"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.WALLET,
                        icon_size=28,
                        icon_color= obter_cor_icone(ROTA_ADD),
                        on_click= lambda e: ir_para(ROTA_ADD),
                        tooltip="Despesas"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.PERSON,
                        icon_size=28,
                        icon_color=obter_cor_icone(ROTA_PERFIL),
                        on_click= lambda e: ir_para(ROTA_PERFIL),
                        tooltip="Perfil"
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            width=300,
            alignment=ft.alignment.center_left,
        ),
        bgcolor="white", 
        padding=5,
        border=ft.border.only(top=ft.border.BorderSide(1, "#e0e0e0")),  #LINHA NO TOPO
    )

    return barra_de_navegacao