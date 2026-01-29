import flet as ft
from controllers.saldo_controller import SaldoController


def criar_saldo_card(page, user_id, refresh_home_func=None):

    controller = SaldoController()
    editar_saldo = False

    # MOSTRAR MENSAGEM 
    def mostrar_mensagem(mensagem, cor):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=cor,
            duration=2000
        )
        page.snack_bar.open = True

    
# CARREGAR SALDO
    def carregar_dados():
        saldo_atual = controller.obter_saldo(user_id)
        texto_saldo.value = f"{saldo_atual:.2f}€"
        page.update()

    #EDITAR SALDO
    def iniciar_editar_saldo(e):
        nonlocal editar_saldo # nonlocal -> permite me chamar a variavel de fora e alterar o seu valor sem ser preciso criar um nova variavel
        if editar_saldo:
            return

        editar_saldo = True

        # valores atuais
        saldo_atual = controller.obter_saldo(user_id)

        saldo_field.value = str(saldo_atual) if saldo_atual > 0 else ""

        container_saldo.visible = False
        container_editar.visible = True
        btn_guardar.visible = True
        btn_cancelar.visible= True

        page.update()

    # CANCELAR EDITAR SALDO
    def cancelar_editar(e):
        nonlocal editar_saldo
        editar_saldo= False

        container_saldo.visible = True
        container_editar.visible = False
        btn_guardar.visible = False
        btn_cancelar.visible = False

        page.update()

    
    #GUARDAR RECEITA
    def guardar_saldo_handler(e):
        nonlocal editar_saldo

        try:
            novo_saldo = float(saldo_field.value)
        except:
            mostrar_mensagem("Por favor insira um valor válido", "red")
            return

        sucesso, mensagem = controller.guardar_saldo(user_id, novo_saldo)

        if sucesso:
            carregar_dados()

            # voltar ao modo normal
            container_saldo.visible = True
            container_editar.visible = False
            btn_guardar.visible = True
            btn_cancelar.visible= False
            editar_saldo = False

            mostrar_mensagem(mensagem, "green")

            if refresh_home_func:
                refresh_home_func()
        else:
            mostrar_mensagem(mensagem, "red")

        page.update()


    #texto do saldo
    texto_saldo= ft.Text(
        "0.00€",
        color= "white",
        size=20,
        weight="w600",
        text_align="center"
    )
    
    #campo editar receita
    saldo_field= ft.TextField(
        label="Saldo Disponível",
        value="",
        text_size=16,
        color="white",
        focused_border_color="white",
        width=200,
        height=40,
        border_radius=12,
        text_align=ft.TextAlign.CENTER,
        suffix_text="€"
    )

    #btn guardar receita
    btn_guardar= ft.ElevatedButton(
        "Guardar",
        on_click= guardar_saldo_handler,
        style= ft.ButtonStyle(
            color= "#0a85ff",
            bgcolor="white"
        ),
        width=100,
        height=35,
        visible= False
    )

    # btn cancelar edição
    btn_cancelar= ft.ElevatedButton(
        "Cancelar",
        on_click= cancelar_editar,
        style= ft.ButtonStyle(
            color= "#0a85ff",
            bgcolor="white"
        ),
        width=100,
        height=35,
        visible= False
    )

    #container para controlar a parte visivel 
    container_saldo= ft.Container(
        content= texto_saldo,
        on_click= iniciar_editar_saldo,
        padding=10,
        visible= True
    )

    container_editar= ft.Container(
        content= ft.Column([
            saldo_field,
        
        ft.Row([
            btn_guardar,
            btn_cancelar
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
        )
    ],
    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
    spacing=10 
    ),
    visible=False
    )

    # carrega a receita e o saldo ao abrir
    carregar_dados()

    #container principal do cartão
    saldo_card= ft.Container(
        height=180,
        width=300,
        border_radius=20,
        padding=10,
        alignment= ft.alignment.center,
        gradient= ft.LinearGradient(
            rotation= 0.3,
            colors= ["#0a85ff", "#2171C2"],
        ),
        content= ft.Column([
            ft.Text("Saldo Total", color="white", size=20, weight="bold"),

            #área interativa do saldo
            ft.Container(
                content= ft.Column([
                    container_saldo,
                    container_editar,
                ], 
                horizontal_alignment= ft.CrossAxisAlignment.CENTER)
            ),
        ], 
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing=10
        )
    )
    # retornar o container do cartão e a função de controlo +  atualizar a UI
    return saldo_card, carregar_dados
