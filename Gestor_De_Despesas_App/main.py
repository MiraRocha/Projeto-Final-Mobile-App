import flet as ft
from controllers.router_controller import RouterController
from routes.rotas import ROTA_SPLASH

def main(page: ft.Page):
    page.window_width = 520
    page.window_height = 690
    page.padding = 0
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    router = RouterController(page)

    page.on_route_change = router.mudar_rota
    page.go(ROTA_SPLASH) #navegar entre as páginas


if __name__ == "__main__":
    ft.app(target=main)
