import flet as ft

appName = "Nun Shark"
def main(page: ft.Page):
    page.title = appName
    userInfo = ft.TextField(icon=ft.icons.PERSON, label="Username")
    passInfo = ft.TextField(icon=ft.icons.PASSWORD, label="Password", password=True, can_reveal_password=True)

    def user_auth(_):
        if userInfo.value == "admin" and passInfo.value == "leafa":
            page.go("/main")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text('Username or Password is Incorrect!',
                        color="#ff0000"),
                bgcolor="#ffcccb")
            page.snack_bar.open = True
        passInfo.value = ""
        page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/auth":
            page.title = "AUTH"
            page.views.append(
                ft.View(
                    "/auth",
                    [ft.Column(controls=[   ft.Container(content=ft.Text(appName, size=50), alignment= ft.alignment.bottom_center, height=200),
                                            userInfo,
                                            passInfo,
                                            ft.Container(content=ft.FloatingActionButton(text="LOGIN", on_click=user_auth, expand=True), alignment=ft.alignment.center)]
                        )
                    ]
                )
            )
        elif page.route == "/main":
            page.title = "MAIN"
            page.views.append(
                ft.View(
                    "/main",
                    [ft.Column(controls=[ft.Container(ft.Row(controls=[ft.Text(f'Welcome Back, {userInfo.value}!', expand=True),
                                                                       ft.IconButton(ft.icons.LOGOUT, on_click=lambda _: page.go('/auth'))]),
                                                      bgcolor=ft.colors.BLUE),
                                        ft.Container(alignment = ft.alignment.center,
                                                    content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                            controls=[ft.FloatingActionButton(icon=ft.icons.ADD, text='Add')]))])]
                )
            )
        if page.route == "/store":
            page.title = "STORE"
            page.views.append(
                ft.View(
                    "/store",
                    [ft.IconButton(ft.icons.CHECK, on_click=lambda _: page.go("/auth"))]
                )
            )


        page.update()

    def YPRESSENTER(_: ft.KeyboardEvent):
        if _.key == 'Enter' and page.route == '/auth':
            user_auth(_)

    page.on_keyboard_event = YPRESSENTER
    page.route = "/auth"
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
