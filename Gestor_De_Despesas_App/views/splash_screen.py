import flet as ft
from flet_lottie import Lottie
import asyncio
from routes.rotas import ROTA_LOGIN, ROTA_SPLASH
def criar_splash_view(page):

    async def esperar_e_redirecionar(): #função vai esperar sem travar a interface
        await asyncio.sleep(6) # Espera 5 segundos, mas ao contrário do time.sleep(), a animação do splash continua fluida, e a app não congela
        page.go(ROTA_LOGIN)

    # Iniciar tarefa assíncrona sem bloquear UI
    page.run_task(esperar_e_redirecionar) # pedido para o Flet correr esta função sem bloquear a interface principal

    #VIEW
    view = ft.View(
        ROTA_SPLASH, #"/"
        [
            ft.Container(
                ft.Column([
                    # LOTTIE ANIMAÇÃO
                    Lottie(
                        "https://lottie.host/01f64d6b-dc52-4030-937f-1c8dd6563f52/gfVykcUyDn.json",
                        width=250,
                        height=250,
                        repeat=True,
                        animate=True
                    ),

                    #TEXT
                    ft.Text(
                        "Gestor de Despesas", 
                        size=24, 
                        weight='w600', 
                        color='#0a85ff'
                    ),
                    #TEXT
                    ft.Text(
                    "A gerir as suas finanças...", 
                    size=14, 
                    weight='w300', 
                    color='#666666'
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10

                ),
                expand=True,
                alignment=ft.alignment.center
            ),
            
        ], 
        padding=50,
        bgcolor='white'
    )
    
    return view  #Retorna a view criada