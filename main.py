import flet as ft
from client.user_input import UserInput


class main(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

        self.page.theme_mode = ft.ThemeMode.DARK

        self.init_helper()

    def init_helper(self):
        self.page.on_route_change = self.on_route_change
        self.page.on_view_pop = self.view_pop

        self.page.go("/user-input")


    def on_route_change(self, route):
        """Routing system of the app"""

        # All the pages on the app
        new_page = {
            "/user-input": UserInput,
        }[self.page.route](self.page)
        self.page.views.clear()

        self.page.views.append(
            ft.View(
                route=route,
                controls=[new_page]
            )
        )

        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


ft.app(
    target=main,
    assets_dir="assets",
    port=8080,
)
