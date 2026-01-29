import flet as ft
from datetime import datetime

from controllers.estatistica_controller import EstatisticaCrontroller
from components.barra_navegacao import criar_barra_navegacao
from components.categorias_info import CATEGORIAS_INFO
from routes.rotas import ROTA_STATS


def criar_estatistica_view(page):

    # CHAMAMOS A NOSSA CLASSE
    controller = EstatisticaCrontroller()

    # Estado inicial: mês/ano atual
    hoje = datetime.now()
    ano_atual = hoje.year

    # Dropdown MÊS
    dropdown_meses = ft.Dropdown(
        label="Mês",
        hint_text="Mês",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        color="black",
        bgcolor="#0a85ff",
        label_style= ft.TextStyle(color="#0a85ff"),
        value="",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 12 + 1)], # gera automaticamente as opções do dropdown (meses 1 a 12), 12 + 1 -> “inclusivo até 12”
        width=150,
    )

    # Dropdown ANO
    dropdown_anos = ft.Dropdown(
        label="Ano",
        hint_text="Ano",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        color="black",
        bgcolor="#0a85ff",
        label_style= ft.TextStyle(color="#0a85ff"),
        value="",
        options=[ft.dropdown.Option(str(ano_atual - i)) for i in range(0, 4)], # gera os últimos 4 anos, começando pelo ano atual (ex: 2026, 2025, 2024, 2023) 
        width=150,
    )

    # PieChart

    normal_radius = 60
    hover_radius = 80

    normal_title_style = ft.TextStyle(
        size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
    )

    hover_title_style = ft.TextStyle(
        size=16,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
    )

    # cria um badge circular com um ícone (usado no gráfico)
    # o size define o diâmetro e o border_radius torna-o um círculo
    def badge(icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.Colors.BLUE),
            border_radius=size / 2, # arredonda o quadrado até virar um círculo perfeito.
            bgcolor=ft.Colors.WHITE,
        )

    #gráfico
    grafico_pizza = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True,
    )
    
    # texto
    texto_total = ft.Container(
    content=ft.Text(
        "Total: 0€", 
        size=16, 
        weight="w600", 
        color="#0a85ff"
    ),
    width=300,
    alignment=ft.alignment.center_left
    )

    # histórico
    lista_historico= ft.Column(
        expand=False,
        spacing= 5,
        width=300,
        scroll= ft.ScrollMode.AUTO,
        horizontal_alignment= ft.CrossAxisAlignment.STRETCH
    )

    # histórico container
    lista_historico_container = ft.Container(
        lista_historico,
        width=300,
        height=240,
        bgcolor=None
    )
    
    # FUNÇÃO PARA CRIAR ITEM DO HISTÓRICO (COM ÍCONE E COR)
    def criar_item_historico(movimento):

        categoria= movimento["categoria"]
        valor= abs(movimento["valor"]) # as despesas vem do firebase negativas então voltamos a colocar positivo para mostrar no histórico positivo

        # acedemos as nossas CATEGORIAS INFO para ir buscar a cor e os icones
        # caso nao exista usamos a categoria "Outros"
        info= CATEGORIAS_INFO.get(categoria, CATEGORIAS_INFO["Outros"])
        cor= info["cor"]
        icone= info["icone"]

        item= ft.Container(
            bgcolor=cor,
            padding=10,
            border_radius=10,
            content=ft.Row(
                [
                    # ícone da categoria
                    ft.Icon(
                        icone,
                        color="white",
                        size=22
                    ),

                    # texto categoria + valor + data
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(categoria, color="white", weight="bold"),
                                    ft.Text(f"{valor:.2f}€", color="white", weight="bold"),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Text(
                                movimento["data_formatada"],
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

        lista_historico.controls.append(item)



    # quando o utilizador muda o mês/ano, ou quando a página abre pela primeira vez, esta função é chamada para atualizar o gráfico e o histórico
    def atualizar(e=None):

        # se o utlizador escolhe um mês -> usa-o, caso contrário usa o mês atual
        mes= int(dropdown_meses.value) if dropdown_meses.value else hoje.month

        # se o utlizador escolhe um ano -> usa-o, caso contrário usa o ano atual
        ano= int(dropdown_anos.value) if dropdown_anos.value else hoje.year

        # é assim que todas as páginas sabem quem está autenticado
        user_id= page.session.get("user_id")

        # vai buscar dados filtrados ao estatistica_controller.py
        dados, total, historico = controller.despesas_por_mes(user_id, mes, ano)

        # limpar grafico e histórico
        grafico_pizza.sections.clear()
        lista_historico.controls.clear()

        # atualizar texto do total do mês
        texto_total.content.value = f"Total: {total:.2f}€"


        for categoria, valor in dados:

            info = CATEGORIAS_INFO.get(categoria, CATEGORIAS_INFO["Outros"])
            color = info["cor"]
            icone = info["icone"]

            grafico_pizza.sections.append(
                ft.PieChartSection(
                    value=valor,
                    title=f"{valor:.0f}€",
                    title_style=normal_title_style,
                    color=color,
                    radius=normal_radius,
                    badge=badge(icone, 40),
                    badge_position=0.98,
                )
            )

        # hover efeito
        # o gráfico chama esta função sempre que passamos o rato por cima de uma fatia
        def on_grafico_evento(ev: ft.PieChartEvent): # ev.section_index diz qual a secção que está a ser "hovered"
            for indice, seccao in enumerate(grafico_pizza.sections): # o loop percorre todas as secções
                if indice == ev.section_index: # a fatia ativa fica maior e aumenta o tamanho do título
                    seccao.radius = hover_radius  
                    seccao.title_style = hover_title_style
                else:
                    seccao.radius = normal_radius # as restantes voltam ao normal
                    seccao.title_style = normal_title_style
            grafico_pizza.update() # redesenha o gráfico

        # quando o gráfico receber um evento (hover/click), usa esta função
        grafico_pizza.on_chart_event = on_grafico_evento

        # histórico
        # cada movimento do mês selecionado é desenhado com ícone e cor da categoria, graças à função criar_item_historico()
        for movimento in historico:
            criar_item_historico(movimento)

        # atualizar grárfico, lista de histórico e página
        grafico_pizza.update()
        lista_historico.update()
        page.update()

    dropdown_meses.on_change = atualizar # ao mudar o mês -> atualiza
    dropdown_anos.on_change = atualizar # ao mudar o ano -> atualiza
    page.on_ready = atualizar # ao abrir a página -> atualiza automaticamente


    # VIEW
    view = ft.View(
        ROTA_STATS,
        [
            ft.Container(
                ft.Column([
                    # TEXTO ESTATIS.
                    ft.Text("Estatísticas Mensais", size=22, weight="bold", color="#0a85ff"),
                    # GRÁFICO
                    ft.Container(grafico_pizza, height=250),

                    ft.Row([dropdown_meses, dropdown_anos], alignment="center"),
                    # TEXTO TOTAL €
                    texto_total,
                    # HISTORICO DO MÊS
                    ft.Container(
                        ft.Text("Histórico do mês", size=12, weight="bold", color="#666666"),
                        width=300,
                        alignment=ft.alignment.center_left
                    ),
                    # LISTA HIST
                    lista_historico_container
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True
            ),
            # MENU DE NAVEGAÇÃO
            criar_barra_navegacao(page, ROTA_STATS)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor='white',
        spacing=0
    )

    return view