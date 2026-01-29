import flet as ft

from datetime import datetime, date
from controllers.add_despesas_controller import AddDespesasController
from components.barra_navegacao import criar_barra_navegacao
from routes.rotas import ROTA_ADD

def criar_add_despesas_view(page):
    
    # CHAMAMOS A NOSSA CLASSE
    controller = AddDespesasController()

    # CATEGORIAS VINDAS DO CONTROLLER
    categorias = controller.obter_categorias()
    
    # DROPDOWN DE CATEGORIAS (lista suspensa de categorias)
    categoria_dropdown= ft.Dropdown(
        hint_text="Selecionar Categoria",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        width=280,
        color="black",
        bgcolor="#0a85ff",
        label_style= ft.TextStyle(color="white"),
        options=[ft.dropdown.Option(categoria, style=ft.ButtonStyle(color="white")) for categoria in categorias],
        # esta linha garante que todas as opções no dropdown têm texto branco, não apenas a opção selecionada
        value="" # valor padrão
    )

    # CAMPO PARA CATEGORIA PERSONALIZADA
    # opção o utilizador adicionar uma nova categoria caso não exista
    categoria_personalizada_field= ft.TextField(
        label="Adicionar nova categoria",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        width=280,
        height=45,
        color="black",
        visible=False # inicialmente escondido
    )

    # MONTANTE
    montante_field= ft.TextField(
        label="Montante",
        value="",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        width=280,
        height=45,
        color="black",
        suffix_text="€"

    )

    # DATA
    data_field= ft.TextField(
        label="Data",
        text_size=16,
        border_radius=12,
        focused_border_color="#0a85ff",
        width=280,
        height=45,
        color="black",
        value=date.today().strftime("%d/%m/%Y"), # formata para "01/01/2025", data portuguesa
        read_only=True # para forçar a usar o date picker
    )

    # MENSAGEM DE ERRO/SUCESSO
    texto_mensagem = ft.Text(
        " ",
        color="red",
        size=12,
        weight="w400",
        text_align=ft.TextAlign.CENTER,
        visible=False,
    )

    # CONTAINER apenas para o meu text_erro
    mensagem_container = ft.Container(
        content=texto_mensagem,
        height=35,
        margin=ft.margin.only(bottom=8),
        alignment=ft.alignment.center
    )


    # DATE PICKER -> selecionar data
    date_picker= ft.DatePicker(
        first_date=date(2020, 1, 1),
        last_date=date.today(),
    )
    page.overlay.append(date_picker)
    # camada especial sobreposta à interface do utilizador
    # é utilizada para componentes que aparecem ou flutuam acima da página, como diálogos, seletores de data ou menus
    # append() neste caso diz ao Flet para incluir o seletor de datas nesta camada de sobreposição flutuante


    # FUNÇÕES AUXILIARES
    # função de callback que é executada quando o utilizador clica no botão do calendário
    def abrir_calendario(e):
        # date_picker -> objeto | pick_date() -> metodo que abre o caledario na interface
        date_picker.open= True
        page.update()

    def data_selecionada(e):
        if date_picker.value: # se uma data foi selecionada
            data_field.value = date_picker.value.strftime("%d/%m/%Y") # formata para "dia/mês/ano"
            page.update() # atualiza a interface

    date_picker.on_change= data_selecionada
    # cria uma "ligação automática" entre o DatePicker e a função data_selecionada
    # sempre que o valor do DatePicker mudar (quando o utilizador selecionar uma data), 
    # a função data_selecionada será chamada automaticamente
    
    # Mostrar adição de categoria personalizada
    def alterar_categoria_personalizada(e):
        if categoria_dropdown.value == "Outros":
            categoria_personalizada_field.visible= True # mostra o  campo para nova categoria
        else:
            categoria_personalizada_field.visible= False # esconde campo personalizado 
            categoria_personalizada_field.value= "" # limpa o que esta escrito
        page.update()

    # ligação
    categoria_dropdown.on_change= alterar_categoria_personalizada

    # redefinir todos os campos do formulário para os valores iniciais
    def limpar_campos(e):
        categoria_dropdown.value= ""  # volta para categoria padrão "Selecionar Categoria"
        categoria_personalizada_field.value="" # limpa o texto da categoria personalizada
        categoria_personalizada_field.visible= False  # esconde campo personalizado
        montante_field.value= ""  #limpa o montante
        data_field.value= date.today().strftime("%d/%m/%Y")# volta para data atual
        page.update()


    # ADICIONAR DESPESA ATRAVÉS DO NOSSO CONTROLLER add_despesa_controller.py
    def adicionar_despesa_ui(e):
        # page.session, é um dicionário que guarda dados durante a sessão do utilizador
        # .get("user_id"), vai buscar o valor guardado com a chave "user_id"
        # retorna o ID do utilizador que está atualmente logado
        user_id= page.session.get("user_id")

        sucesso, mensagem= controller.adicionar_despesa(
            user_id= user_id,
            categoria_dropdown= categoria_dropdown.value,
            categoria_personalizada= categoria_personalizada_field.value,
            montante= montante_field.value,
            data= data_field.value
        )

        texto_mensagem.value= mensagem
        texto_mensagem.color= "green" if sucesso else "red"
        texto_mensagem.visible= True

        if sucesso:
            limpar_campos(None)

        page.update()

    #BTN ABRIR CALENDÁRIO
    data_btn= ft.ElevatedButton(
        "Escolher Data",
        icon= ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario,
        width=150,
        style= ft.ButtonStyle(
            color= "white",
            bgcolor= "#0a85ff"
        ),
    )

    # VIEW
    view = ft.View(
        ROTA_ADD,
        [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            ft.Text(
                                "Adicionar Despesa",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color="#0a85ff"
                            ),
                            padding=20,
                            alignment=ft.alignment.center
                        ),

                        # CATEGORIA
                        ft.Container(
                            content=ft.Column(
                                [
                                    categoria_dropdown,
                                    categoria_personalizada_field
                                ],
                                spacing=5
                            ),
                            padding=10,
                            alignment=ft.alignment.center
                        ),

                        # MONTANTE
                        ft.Container(
                            content=ft.Column([montante_field]),
                            padding=10,
                        ),

                        # DATA
                        ft.Container(
                            content=ft.Column(
                                [data_field, data_btn],
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=10,
                        ),

                        #MENSAGEM
                        mensagem_container,

                        # BOTÕES
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Limpar",
                                        on_click=limpar_campos,
                                        style=ft.ButtonStyle(color="white", bgcolor="#0a85ff"),
                                        width=120,
                                        height=40
                                    ),
                                    ft.ElevatedButton(
                                        "Adicionar",
                                        on_click=adicionar_despesa_ui,
                                        style=ft.ButtonStyle(color="white", bgcolor="#0a85ff"),
                                        width=120,
                                        height=40
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            ),
                            padding=20
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                ),
                expand=True,

            ),
            # MENU DE NAVEGAÇÃO
            criar_barra_navegacao(page, ROTA_ADD),
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        bgcolor="white",
        spacing= 0
    )

    return view